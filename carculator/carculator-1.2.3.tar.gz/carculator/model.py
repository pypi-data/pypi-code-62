from .energy_consumption import EnergyConsumptionModel
from .hot_emissions import HotEmissionsModel
from .noise_emissions import NoiseEmissionsModel
import numexpr as ne
import numpy as np
import xarray as xr


DEFAULT_MAPPINGS = {
    "electric": {"BEV", "PHEV-e"},
    "combustion": {
        "ICEV-p",
        "HEV-p",
        "HEV-d",
        "PHEV-c-p",
        "ICEV-g",
        "ICEV-d",
        "PHEV-c-d",
    },
    "combustion_wo_cng": {"ICEV-p", "HEV-p", "HEV-d", "PHEV-c-p", "ICEV-d", "PHEV-c-d"},
    "pure_combustion": {"ICEV-p", "ICEV-g", "ICEV-d"},
    "petrol": {"ICEV-p", "HEV-p", "PHEV-c-p"},
    "cng": {"ICEV-g"},
    "fuel_cell": {"FCEV"},
    "hybrid": {"PHEV-c-p", "PHEV-e", "PHEV-c-d"},
    "combustion_hybrid": {"PHEV-c-p", "PHEV-c-d"},
    "electric_hybrid": {"PHEV-e"},
    "diesel": {"ICEV-d", "PHEV-c-d", "HEV-d"},
    "battery": {"BEV"},
}


def finite(array, mask_value=0):
    return np.where(np.isfinite(array), array, mask_value)


class CarModel:

    """
    This class represents the entirety of the vehicles considered, with useful attributes, such as an array that stores
    all the vehicles parameters.

    :ivar array: multi-dimensional numpy-like array that contains parameters' value(s)
    :vartype array: xarray.DataArray
    :ivar mappings: Dictionary with names correspondence
    :vartype mappings: dict
    :ivar ecm: instance of :class:`EnergyConsumptionModel` class for a given driving cycle
    :vartype ecm: coarse.energy_consumption.EnergyConsumptionModel

    """

    def __init__(self, array, mappings=None, cycle=None, gradient=None):

        self.array = array
        self.mappings = mappings or DEFAULT_MAPPINGS

        if cycle is None:
            self.ecm = EnergyConsumptionModel("WLTC")
        else:
            self.ecm = EnergyConsumptionModel(cycle=cycle, gradient=gradient)

    def __call__(self, key):
        """
        This method fixes a dimension of the `array` attribute given a powertrain technology selected.

        Set up this class as a context manager, so we can have some nice syntax

        .. code-block:: python

            with class('some powertrain') as cpm:
                cpm['something']. # Will be filtered for the correct powertrain

        On with block exit, this filter is cleared
        https://stackoverflow.com/a/10252925/164864

        :param key: A powertrain type, e.g., "FCEV"
        :type key: str
        :return: An instance of `array` filtered after the powertrain selected.

        """
        self.__cache = self.array
        self.array = self.array.sel(powertrain=key)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.array = self.__cache
        del self.__cache

    def __getitem__(self, key):
        """
        Make class['foo'] automatically filter for the parameter 'foo'
        Makes the model code much cleaner

        :param key: Parameter name
        :type key: str
        :return: `array` filtered after the parameter selected
        """

        return self.array.sel(parameter=key)

    def __setitem__(self, key, value):
        self.array.loc[{"parameter": key}] = value

    # Make it easier/more flexible to filter by powertrain types
    def __getattr__(self, key):
        if key in self.mappings:
            return self.mappings[key]
        else:
            return super().__getattr__(key)

    def set_all(self, drop_hybrids=True):
        """
        This method runs a series of other methods to obtain the tank-to-wheel energy requirement, efficiency
        of the car, costs, etc.

        :meth:`set_component_masses()`, :meth:`set_car_masses()` and :meth:`set_power_parameters()` are interdependent.
        `powertrain_mass` depends on `power`, `curb_mass` is affected by changes in `powertrain_mass`,
        `combustion engine mass` and `electric engine mass`, and `power` is a function of `curb_mass`.
        The current solution is to loop through the methods until the increment in driving mass is
        inferior to 0.1%.

        :returns: Does not return anything. Modifies ``self.array`` in place.

        """
        # TODO: Converging towards a satisfying curb mass is taking too long! Needs to be optimized.

        diff = 1.0

        while diff > 0.01:
            old_driving_mass = self["driving mass"].sum().values

            self.set_car_masses()

            self.set_power_parameters()
            self.set_component_masses()
            self.set_battery_properties()
            self.set_battery_fuel_cell_replacements()
            self.set_recuperation()
            self.set_fuel_cell_parameters()
            self.set_energy_stored_properties()

            diff = (self["driving mass"].sum().values - old_driving_mass) / self[
                "driving mass"
            ].sum()

        self.set_auxiliaries()
        self.set_ttw_efficiency()
        self.calculate_ttw_energy()
        self.adjust_cost()
        self.set_range()
        self.set_electric_utility_factor()
        self.set_electricity_consumption()
        self.set_costs()
        self.set_hot_emissions()
        self.set_noise_emissions()
        self.create_PHEV()
        if drop_hybrids==True:
            self.drop_hybrid()

    def adjust_cost(self):
        """
        This method adjusts costs of energy storage over time, to correct for the overly optimistic linear
        interpolation between years.

        """

        n_iterations = self.array.shape[-1]
        n_year = len(self.array.year.values)

        # If uncertainty is not considered, the cost factor equals 1.
        # Otherwise, a variability of +/-30% is added.

        if n_iterations == 1:
            cost_factor = 1
        else:
            if 'reference' in self.array.value.values.tolist():
                cost_factor = np.ones((n_iterations, 1))
            else:
                cost_factor = np.random.triangular(.7, 1, 1.3, (n_iterations, 1))

        # Correction of hydrogen tank cost, per kg
        self.array.loc[:, ["FCEV"], "fuel tank cost per kg", :, :] = np.reshape(
            (1.078e58 * np.exp(-6.32e-2 * self.array.year.values) + 3.43e2) * cost_factor,
            (1, 1, n_year, n_iterations),
        )

        # Correction of fuel cell stack cost, per kW
        self.array.loc[:, ["FCEV"], "fuel cell cost per kW", :, :] = np.reshape(
            (3.15e66 * np.exp(-7.35e-2 * self.array.year.values) + 2.39e1) * cost_factor,
            (1, 1, n_year, n_iterations),
        )

        # Correction of energy battery system cost, per kWh
        self.array.loc[
            :,
            ["BEV", "PHEV-e", "PHEV-c-p", "PHEV-c-d"],
            "energy battery cost per kWh",
            :,
            :,
        ] = np.reshape(
            (2.75e86 * np.exp(-9.61e-2 * self.array.year.values) + 5.059e1) * cost_factor,
            (1, 1, n_year, n_iterations),
        )

        # Correction of power battery system cost, per kW
        self.array.loc[
            :,
            ["ICEV-p","ICEV-d","ICEV-g","PHEV-c-p","PHEV-c-d", "FCEV", "HEV-p", "HEV-d"],
            "power battery cost per kW",
            :,
            :,
        ] = np.reshape(
            (8.337e40 * np.exp(-4.49e-2 * self.array.year.values) + 11.17) * cost_factor,
            (1, 1, n_year, n_iterations),
        )

        # Correction of combustion powertrain cost for ICEV-g
        self.array.loc[
            :,
            ["ICEV-g"],
            "combustion powertrain cost per kW",
            :,
            :,
        ] = np.reshape(
            (5.92e160 * np.exp(-.1819 * self.array.year.values) + 26.76) * cost_factor,
            (1, 1, n_year, n_iterations),
        )

    def adjust_fuel_mass(self):
        """
        This method adjusts the fuel mass over the years, to correct for the linear
        interpolation between years.

        """

        n_iterations = self.array.shape[-1]
        n_year = len(self.array.year.values)


        # Correction of hydrogen mass
        self.array.loc[:, ["FCEV"], "fuel mass", :, :] = np.reshape(
            (1.078e58 * np.exp(-6.32e-2 * self.array.year.values) + 3.43e2),
            (1, 1, n_year, n_iterations),
        )

        # Correction of CNG mass


    def drop_hybrid(self):
        """
        This method drops the powertrains `PHEV-c-p`, `PHEV-c-d` and `PHEV-e` as they were only used to create the
        `PHEV` powertrain.
        :returns: Does not return anything. Modifies ``self.array`` in place.
        """
        self.array = self.array.sel(
            powertrain=[
                "ICEV-p",
                "ICEV-d",
                "ICEV-g",
                "PHEV-p",
                "PHEV-d",
                "FCEV",
                "BEV",
                "HEV-p",
                "HEV-d",
            ]
        )

    def set_electricity_consumption(self):
        """
        This method calculates the total electricity consumption for BEV and plugin-hybrid vehicles
        :returns: Does not return anything. Modifies ``self.array`` in place.
        """

        for pt in self.electric:
            with self(pt) as cpm:
                cpm["electricity consumption"] = (
                    cpm["TtW energy"] / cpm["battery charge efficiency"]
                ) / 3600

    def calculate_ttw_energy(self):
        """
        This method calculates the energy required to operate auxiliary services as well
        as to move the car. The sum is stored under the parameter label "TtW energy" in :attr:`self.array`.

        """
        aux_energy = self.ecm.aux_energy_per_km(self["auxiliary power demand"])

        for pt in self.pure_combustion:
            with self(pt) as cpm:
                aux_energy.loc[{"powertrain": pt}] /= cpm["engine efficiency"]
        for pt in self.fuel_cell:
            with self(pt) as cpm:
                aux_energy.loc[{"powertrain": pt}] /= cpm["fuel cell system efficiency"]

        self["auxiliary energy"] = aux_energy

        motive_energy = self.ecm.motive_energy_per_km(
            driving_mass=self["driving mass"],
            rr_coef=self["rolling resistance coefficient"],
            drag_coef=self["aerodynamic drag coefficient"],
            frontal_area=self["frontal area"],
            ttw_efficiency=self["TtW efficiency"],
            recuperation_efficiency=self["recuperation efficiency"],
            motor_power=self["electric power"],
        ).sum(axis=-1)

        self.motive_energy = motive_energy
        self["TtW energy"] = aux_energy + motive_energy

    def set_fuel_cell_parameters(self):
        """
        Specific setup for fuel cells, which are mild hybrids.
        Must be called after :meth:`.set_power_parameters`.
        """
        for pt in self.fuel_cell:
            with self(pt):
                self["fuel cell system efficiency"] = (
                    self["fuel cell stack efficiency"]
                    / self["fuel cell own consumption"]
                )
                self["fuel cell power share"] = self["fuel cell power share"].clip(
                    min=0, max=1
                )
                self["fuel cell power"] = (
                    self["power"]
                    * self["fuel cell power share"]
                    * self["fuel cell own consumption"]
                )
                # our basic fuel cell mass is based on a car fuel cell with 800 mW/cm2 and 0.51 kg/kW
                self["fuel cell stack mass"] = (
                    0.51
                    * self["fuel cell power"]
                    * (800
                    / self["fuel cell power area density"])
                )
                self["fuel cell ancillary BoP mass"] = (
                    self["fuel cell power"]
                    * self["fuel cell ancillary BoP mass per power"]
                )
                self["fuel cell essential BoP mass"] = (
                    self["fuel cell power"]
                    * self["fuel cell essential BoP mass per power"]
                )

                self["battery power"] = self["fuel cell power"] * (
                    1 - self["fuel cell power share"]
                )
                self["battery cell mass"] = (
                    self["battery power"] / self["battery cell power density"]
                )
                self["battery BoP mass"] = self["battery cell mass"] * (
                    1 - self["battery cell mass share"]
                )

                self["oxidation energy stored"] = self["fuel mass"] * 120 / 3.6  # kWh
                self["fuel tank mass"] = (
                    self["oxidation energy stored"] * self["H2 tank mass per energy"]
                )

    def set_auxiliaries(self):
        """
        Calculates the power needed to operate the auxiliary services of the vehicle (heating, cooling).

        The demand for heat and cold are expressed as a fraction of the heating and cooling capacities

        .. note:

            Auxiliary power demand (W) = Base auxiliary power (W) +
            (Heating demand (dimensionless, between 0 and 1) * Heating power (W)) +
            (Cooling demand (dimensionless, between 0 and 1) * Cooling power (W))

        """
        self["auxiliary power demand"] = (
            self["auxilliary power base demand"]
            + self["heating thermal demand"] * self["heating energy consumption"]
            + self["cooling thermal demand"] * self["cooling energy consumption"]
        )

    def set_recuperation(self):
        self["recuperation efficiency"] = (
            self["drivetrain efficiency"] * self["battery charge efficiency"]
        )

    def set_battery_fuel_cell_replacements(self):
        """
        This methods calculates the fraction of the replacement battery needed to match the vehicle lifetime.

        .. note::
            if ``car lifetime`` = 200000 (km) and ``battery lifetime`` = 190000 (km) then ``replacement battery`` = 0.05

        .. note::
            It is debatable whether this is realistic or not. Car owners may not decide to invest in a new
            battery if the remaining lifetime of the car is only 10000 km. Also, a battery lifetime may be expressed
            in other terms, e.g., charging cycles.

        """
        # Here we assume that we can use fractions of a battery/fuel cell
        # (averaged across the fleet)
        self["battery lifetime replacements"] = finite(
            np.clip(
                (self["lifetime kilometers"] / self["battery lifetime kilometers"]) - 1,
                0,
                None,
            )
        )
        self["fuel cell lifetime replacements"] = finite(
            np.clip(
                (self["lifetime kilometers"] / self["fuel cell lifetime kilometers"])
                - 1,
                0,
                None,
            )
        )

    def set_car_masses(self):
        """
        Define ``curb mass``, ``driving mass``, and ``total cargo mass``.

            * `curb mass <https://en.wikipedia.org/wiki/Curb_weight>`__ is the mass of the vehicle and fuel, without people or cargo.
            * ``total cargo mass`` is the mass of the cargo and passengers.
            * ``driving mass`` is the ``curb mass`` plus ``total cargo mass``.

        .. note::
            driving mass = total cargo mass + driving mass

        """

        self["curb mass"] = self["glider base mass"] * (1 - self["lightweighting"])

        curb_mass_includes = [
            "fuel mass",
            "charger mass",
            "converter mass",
            "inverter mass",
            "power distribution unit mass",
            # Updates with set_components_mass
            "combustion engine mass",
            # Updates with set_components_mass
            "electric engine mass",
            # Updates with set_components_mass
            "powertrain mass",
            "fuel cell stack mass",
            "fuel cell ancillary BoP mass",
            "fuel cell essential BoP mass",
            "battery cell mass",
            "battery BoP mass",
            "fuel tank mass",
        ]
        self["curb mass"] += self[curb_mass_includes].sum(axis=2)

        self["total cargo mass"] = (
            self["average passengers"] * self["average passenger mass"]
            + self["cargo mass"]
        )
        self["driving mass"] = self["curb mass"] + self["total cargo mass"]

    def set_power_parameters(self):
        """Set electric and combustion motor powers based on input parameter ``power to mass ratio``."""
        # Convert from W/kg to kW
        self["power"] = self["power to mass ratio"] * self["curb mass"] / 1000
        self["combustion power share"] = self["combustion power share"].clip(
            min=0, max=1
        )
        self["combustion power"] = self["power"] * self["combustion power share"]
        self["electric power"] = self["power"] * (1 - self["combustion power share"])

    def set_component_masses(self):
        self["combustion engine mass"] = (
            self["combustion power"] * self["combustion mass per power"]
            + self["combustion fixed mass"]
        )
        self["electric engine mass"] = (
            self["electric power"] * self["electric mass per power"]
            + self["electric fixed mass"]
        )
        self["powertrain mass"] = (
            self["power"] * self["powertrain mass per power"]
            + self["powertrain fixed mass"]
        )

    def set_electric_utility_factor(self):
        with self("PHEV-e") as cpm:
            cpm["electric utility factor"] = (
                1 - np.exp(-0.01147 * cpm["range"])
            ) ** 1.186185

    def create_PHEV(self):
        """ PHEV-p/d is the range-weighted average between PHEV-c-p/PHEV-c-d and PHEV-e.
        """
        self.array.loc[:, "PHEV-d", :, :, :] = (
            self.array.loc[:, "PHEV-e", :, :, :]
            * self.array.loc[:, "PHEV-e", "electric utility factor", :, :]
        ) + (
            self.array.loc[:, "PHEV-c-d", :, :, :]
            * (1 - self.array.loc[:, "PHEV-e", "electric utility factor", :, :])
        )
        self.array.loc[:, "PHEV-p", :, :, :] = (
            self.array.loc[:, "PHEV-e", :, :, :]
            * self.array.loc[:, "PHEV-e", "electric utility factor", :, :]
        ) + (
            self.array.loc[:, "PHEV-c-p", :, :, :]
            * (1 - self.array.loc[:, "PHEV-e", "electric utility factor", :, :])
        )

    def set_battery_properties(self):
        pt_list = ["ICEV-p", "HEV-p", "HEV-d", "ICEV-g", "ICEV-d"]
        self.array.loc[:, pt_list, "battery power"] = self.array.loc[
            :, pt_list, "electric power"
        ]

        self.array.loc[:, pt_list, "battery cell mass"] = (
            self.array.loc[:, pt_list, "battery power"]
            / self.array.loc[:, pt_list, "battery cell power density"]
        )

        self["battery cell mass share"] = self["battery cell mass share"].clip(
            min=0, max=1
        )
        self.array.loc[:, pt_list, "battery BoP mass", :, :] = self.array.loc[
            :, pt_list, "battery cell mass",
        ] * (1 - self.array.loc[:, pt_list, "battery cell mass share", :, :])

        list_pt_el = ["BEV", "PHEV-c-p", "PHEV-c-d", "PHEV-e"]
        self.array.loc[:, list_pt_el, "battery cell mass"] = (
            self.array.loc[:, list_pt_el, "energy battery mass"]
            * self.array.loc[:, list_pt_el, "battery cell mass share"]
        )

        self.array.loc[:, list_pt_el, "battery BoP mass"] = self.array.loc[
            :, list_pt_el, "energy battery mass"
        ] * (1 - self.array.loc[:, list_pt_el, "battery cell mass share"])

    def set_range(self):

        list_pt = [
            "ICEV-p",
            "HEV-p",
            "HEV-d",
            "PHEV-c-p",
            "PHEV-c-d",
            "ICEV-d",
            "ICEV-g",
            "FCEV",
        ]
        fuel_mass = self.array.loc[:, list_pt, "fuel mass"]
        lhv = self.array.loc[:, list_pt, "LHV fuel MJ per kg"]

        energy_stored = self.array.loc[:, ["BEV", "PHEV-e"], "electric energy stored"]
        battery_DoD = self.array.loc[:, ["BEV", "PHEV-e"], "battery DoD"]

        TtW_el = self.array.loc[:, ["BEV", "PHEV-e"], "TtW energy"]
        TtW = self.array.loc[:, list_pt, "TtW energy"]

        self.array.loc[:, list_pt, "range"] = ne.evaluate(
            "(fuel_mass * lhv * 1000) / TtW"
        )
        self.array.loc[:, ["BEV", "PHEV-e"], "range"] = ne.evaluate(
            "(energy_stored * battery_DoD * 3.6 * 1000) / TtW_el"
        )

    def set_energy_stored_properties(self):

        list_combustion = ["ICEV-p", "HEV-p", "HEV-d", "PHEV-c-p", "PHEV-c-d", "ICEV-d"]
        self.array.loc[:, list_combustion, "oxidation energy stored"] = (
            self.array.loc[:, list_combustion, "fuel mass"]
            * self.array.loc[:, list_combustion, "LHV fuel MJ per kg"]
            / 3.6
        )
        self.array.loc[:, list_combustion, "fuel tank mass"] = (
            self.array.loc[:, list_combustion, "oxidation energy stored"]
            * self.array.loc[:, list_combustion, "fuel tank mass per energy"]
        )

        self.array.loc[:, "ICEV-g", "oxidation energy stored"] = (
            self.array.loc[:, "ICEV-g", "fuel mass"]
            * self.array.loc[:, "ICEV-g", "LHV fuel MJ per kg"]
            / 3.6
        )

        self.array.loc[:, "ICEV-g", "fuel tank mass"] = (
            self.array.loc[:, "ICEV-g", "oxidation energy stored"]
            * self.array.loc[:, "ICEV-g", "CNG tank mass slope"]
            + self.array.loc[:, "ICEV-g", "CNG tank mass intercept"]
        )

        for pt in self.battery:
            with self(pt) as cpm:
                cpm["electric energy stored"] = (
                    cpm["battery cell mass"] * cpm["battery cell energy density"]
                )

        for pt in self.electric_hybrid:
            with self(pt) as cpm:
                cpm["electric energy stored"] = (
                    cpm["battery cell mass"] * cpm["battery cell energy density"]
                )
                cpm["fuel tank mass"] = (
                    cpm["fuel mass"]
                    * cpm["LHV fuel MJ per kg"]
                    / 3.6
                    * cpm["fuel tank mass per energy"]
                )

        # kWh electricity/kg battery cell
        self["battery cell production energy electricity share"] = self[
            "battery cell production energy electricity share"
        ].clip(min=0, max=1)
        self["battery cell production electricity"] = (
            self["battery cell production energy"]
            * self["battery cell production energy electricity share"]
        )
        # MJ heat/kg battery cell
        self["battery cell production heat"] = (
            self["battery cell production energy"]
            - self["battery cell production electricity"]
        ) * 3.6

    def set_costs(self):
        self["glider cost"] = (
            self["glider base mass"] * self["glider cost slope"]
            + self["glider cost intercept"]
        )
        self["lightweighting cost"] = (
            self["glider base mass"]
            * self["lightweighting"]
            * self["glider lightweighting cost per kg"]
        )
        self["electric powertrain cost"] = (
            self["electric powertrain cost per kW"] * self["electric power"]
        )
        self["combustion powertrain cost"] = (
            self["combustion power"] * self["combustion powertrain cost per kW"]
        )
        self["fuel cell cost"] = self["fuel cell power"] * self["fuel cell cost per kW"]
        self["power battery cost"] = (
            self["battery power"] * self["power battery cost per kW"]
        )
        self["energy battery cost"] = (
            self["energy battery cost per kWh"]
            * self["battery cell mass"]
            * self["battery cell energy density"]
        )
        self["fuel tank cost"] = self["fuel tank cost per kg"] * self["fuel mass"]
        # Per km
        self["energy cost"] = self["energy cost per kWh"] * self["TtW energy"] / 3600

        # For battery, need to divide cost of electricity in battery by efficiency of charging
        for pt in self.battery:
            with self(pt):
                self["energy cost"] /= self["battery charge efficiency"]

        self["component replacement cost"] = (
            self["energy battery cost"] * self["battery lifetime replacements"]
            + self["fuel cell cost"] * self["fuel cell lifetime replacements"]
        )

        to_markup = [
            "combustion powertrain cost",
            "component replacement cost",
            "electric powertrain cost",
            "energy battery cost",
            "fuel cell cost",
            "fuel tank cost",
            "glider cost",
            "lightweighting cost",
            "power battery cost",
        ]

        self[to_markup] *= self["markup factor"]

        # calculate costs per km:
        self["lifetime"] = self["lifetime kilometers"] / self["kilometers per year"]
        i = self["interest rate"]
        lifetime = self["lifetime"]
        amortisation_factor = ne.evaluate("i + (i / ((1 + i) ** lifetime - 1))")

        purchase_cost_list = [
            "battery onboard charging infrastructure cost",
            "combustion exhaust treatment cost",
            "combustion powertrain cost",
            "electric powertrain cost",
            "energy battery cost",
            "fuel cell cost",
            "fuel tank cost",
            "glider cost",
            "heat pump cost",
            "lightweighting cost",
            "power battery cost",
        ]

        self["purchase cost"] = self[purchase_cost_list].sum(axis=2)

        # per km
        self["amortised purchase cost"] = (
            self["purchase cost"] * amortisation_factor / self["kilometers per year"]
        )
        # per km
        self["maintenance cost"] = (
            self["maintenance cost per glider cost"]
            * self["glider cost"]
            / self["kilometers per year"]
        )

        # simple assumption that component replacement occurs at half of life.
        km_per_year = self["kilometers per year"]
        com_repl_cost = self["component replacement cost"]
        self["amortised component replacement cost"] = ne.evaluate(
            "(com_repl_cost * ((1 - i) ** lifetime / 2) * amortisation_factor / km_per_year)"
        )

        self["total cost per km"] = (
            self["energy cost"]
            + self["amortised purchase cost"]
            + self["maintenance cost"]
            + self["amortised component replacement cost"]
        )

    def set_ttw_efficiency(self):
        _ = lambda array: np.where(array == 0, 1, array)
        # TODO> check if battery charge efficiency should be added
        self["TtW efficiency"] = (
            _(self["battery discharge efficiency"])
            * _(self["fuel cell system efficiency"])
            * self["drivetrain efficiency"]
            * self["engine efficiency"]
        )

    def set_hot_emissions(self):
        """
        Calculate hot pollutant emissions based on ``driving cycle``.
        The driving cycle is passed to the :class:`HotEmissionsModel` class and :meth:`get_emissions_per_powertrain`
        return emissions per substance per second of driving cycle.
        :return: Does not return anything. Modifies ``self.array`` in place.
        """
        hem = HotEmissionsModel(self.ecm.cycle, self.ecm.cycle_name)

        list_direct_emissions = [
            "Hydrocarbons direct emissions, urban",
            "Hydrocarbons direct emissions, suburban",
            "Hydrocarbons direct emissions, rural",
            "Carbon monoxide direct emissions, urban",
            "Carbon monoxide direct emissions, suburban",
            "Carbon monoxide direct emissions, rural",
            "Nitrogen oxides direct emissions, urban",
            "Nitrogen oxides direct emissions, suburban",
            "Nitrogen oxides direct emissions, rural",
            "Particulate matters direct emissions, urban",
            "Particulate matters direct emissions, suburban",
            "Particulate matters direct emissions, rural",
            "Methane direct emissions, urban",
            "Methane direct emissions, suburban",
            "Methane direct emissions, rural",
            "NMVOC direct emissions, urban",
            "NMVOC direct emissions, suburban",
            "NMVOC direct emissions, rural",
            "Lead direct emissions, urban",
            "Lead direct emissions, suburban",
            "Lead direct emissions, rural",
            "Sulfur dioxide direct emissions, urban",
            "Sulfur dioxide direct emissions, suburban",
            "Sulfur dioxide direct emissions, rural",
            "Dinitrogen oxide direct emissions, urban",
            "Dinitrogen oxide direct emissions, suburban",
            "Dinitrogen oxide direct emissions, rural",
            "Ammonia direct emissions, urban",
            "Ammonia direct emissions, suburban",
            "Ammonia direct emissions, rural",
            "Benzene direct emissions, urban",
            "Benzene direct emissions, suburban",
            "Benzene direct emissions, rural",
        ]

        # Year index for EURO 6-d pollution class, starts in 2020
        self.array.loc[
            :, ["ICEV-d", "PHEV-c-d", "HEV-d"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        y >= 2020]
        ] = hem.get_emissions_per_powertrain("diesel", euro_class=6.3)

        # Year index for EURO 6-d-TEMP pollution class, starts in 2019, ends before 2020
        self.array.loc[
            :, ["ICEV-d", "PHEV-c-d", "HEV-d"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        2019 <= y < 2020]
        ] = hem.get_emissions_per_powertrain("diesel", euro_class=6.2)

        # Year index for EURO 6-c pollution class, starts in 2017, ends in 2018
        self.array.loc[
            :, ["ICEV-d", "PHEV-c-d", "HEV-d"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        2017 <= y < 2019]
        ] = hem.get_emissions_per_powertrain("diesel", euro_class=6.1)

        # Year index for EURO 6-ab pollution class, starts in 2015, ends in 2017
        self.array.loc[
            :, ["ICEV-d", "PHEV-c-d", "HEV-d"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        2015 <= y < 2017]
        ] = hem.get_emissions_per_powertrain("diesel", euro_class=6.0)

        # Year index for EURO 5 pollution class, starts in 2011, ends in 2014
        self.array.loc[
            :, ["ICEV-d", "PHEV-c-d", "HEV-d"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        2011 <= y < 2015]
        ] = hem.get_emissions_per_powertrain("diesel", euro_class=5)

        # Year index for EURO 4 pollution class, starts in 2006, ends in 2010
        self.array.loc[
            :, ["ICEV-d", "PHEV-c-d", "HEV-d"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        2006 <= y < 2011]
        ] = hem.get_emissions_per_powertrain("diesel", euro_class=4)

        # Year index for EURO 3 pollution class, starts in 2001, ends in 2005
        self.array.loc[
            :, ["ICEV-d", "PHEV-c-d", "HEV-d"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        2001 <= y < 2006]
        ] = hem.get_emissions_per_powertrain("diesel", euro_class=3)

        # Year index for EURO 2 pollution class, starts in 1997, ends in 2000
        self.array.loc[
            :, ["ICEV-d", "PHEV-c-d", "HEV-d"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        1997 <= y < 2001]
        ] = hem.get_emissions_per_powertrain("diesel", euro_class=2)

        # Year index for EURO 1 pollution class, starts in 1993, ends in 1996
        self.array.loc[
            :, ["ICEV-d", "PHEV-c-d", "HEV-d"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        1993 <= y < 1997]
        ] = hem.get_emissions_per_powertrain("diesel", euro_class=1)

        # Year index for EURO 0 pollution class, ends in 1992
        self.array.loc[
            :, ["ICEV-d", "PHEV-c-d", "HEV-d"], list_direct_emissions, [y for y in self.array.year.values if y < 1993]
        ] = hem.get_emissions_per_powertrain("diesel", euro_class=0)

        # Applies an emission factor, useful for sensitivity purpose
        self.array.loc[
            :, ["ICEV-d", "PHEV-c-d", "HEV-d"], list_direct_emissions, :
        ] *= self.array.loc[:, ["ICEV-d", "PHEV-c-d", "HEV-d"], "emission factor", :]

        # Year index for EURO 6-d pollution class, starts in 2020
        self.array.loc[
            :, ["ICEV-p", "HEV-p", "PHEV-c-p"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        y >= 2020]
        ] = hem.get_emissions_per_powertrain("petrol", euro_class=6.3)

        # Year index for EURO 6-d-TEMP pollution class, starts in 2019, ends in 2020
        self.array.loc[
            :, ["ICEV-p", "HEV-p", "PHEV-c-p"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        2019 <= y < 2020]
        ] = hem.get_emissions_per_powertrain("petrol", euro_class=6.2)

        # Year index for EURO 6-c pollution class, starts in 2017, ends in 2018
        self.array.loc[
            :, ["ICEV-p", "HEV-p", "PHEV-c-p"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        2017 <= y < 2019]
        ] = hem.get_emissions_per_powertrain("petrol", euro_class=6.1)

        # Year index for EURO 6-ab pollution class, starts in 2015, ends in 2017
        self.array.loc[
            :, ["ICEV-p", "HEV-p", "PHEV-c-p"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        2015 <= y < 2017]
        ] = hem.get_emissions_per_powertrain("petrol", euro_class=6.0)

        # Year index for EURO 5 pollution class, starts in 2011, ends in 2014
        self.array.loc[
            :, ["ICEV-p", "HEV-p", "PHEV-c-p"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        2011 <= y < 2015]
        ] = hem.get_emissions_per_powertrain("petrol", euro_class=5)

        # Year index for EURO 4 pollution class, starts in 2006, ends in 2010
        self.array.loc[
            :, ["ICEV-p", "HEV-p", "PHEV-c-p"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        2006 <= y < 2011]
        ] = hem.get_emissions_per_powertrain("petrol", euro_class=4)

        # Year index for EURO 3 pollution class, starts in 2001, ends in 2005
        self.array.loc[
            :, ["ICEV-p", "HEV-p", "PHEV-c-p"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        2001 <= y < 2006]
        ] = hem.get_emissions_per_powertrain("petrol", euro_class=3)

        # Year index for EURO 2 pollution class, starts in 1997, ends in 2000
        self.array.loc[
            :, ["ICEV-p", "HEV-p", "PHEV-c-p"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        1997 <= y < 2001]
        ] = hem.get_emissions_per_powertrain("petrol", euro_class=2)

        # Year index for EURO 1 pollution class, starts in 1993, ends in 1996
        self.array.loc[
            :, ["ICEV-p", "HEV-p", "PHEV-c-p"], list_direct_emissions, [y for y in self.array.year.values if
                                                                        1993 <= y < 1997]
        ] = hem.get_emissions_per_powertrain("petrol", euro_class=1)

        # Year index for EURO 0 pollution class, starts ends in 1992
        self.array.loc[
            :, ["ICEV-p", "HEV-p", "PHEV-c-p"], list_direct_emissions, [y for y in self.array.year.values if y < 1993]
        ] = hem.get_emissions_per_powertrain("petrol", euro_class=0)

        # Applies an emission factor, useful for sensitivity purpose
        self.array.loc[
            :, ["ICEV-p", "HEV-p", "PHEV-c-p"], list_direct_emissions, :
        ] *= self.array.loc[:, ["ICEV-p", "HEV-p", "PHEV-c-p"], "emission factor", :]

        # Year index for EURO 6 pollution class, starts in 2015
        self.array.loc[
            :, "ICEV-g", list_direct_emissions, [y for y in self.array.year.values if y>=2015]
        ] = hem.get_emissions_per_powertrain("CNG", euro_class=6)

        # Year index for EURO 5 pollution class, starts in 2011, ends in 2014
        self.array.loc[
            :, "ICEV-g", list_direct_emissions, [y for y in self.array.year.values if 2011 <= y < 2015]
        ] = hem.get_emissions_per_powertrain("CNG", euro_class=5)

        # Year index for EURO 4 pollution class, starts in 2006, ends in 2010
        self.array.loc[
            :, "ICEV-g", list_direct_emissions, [y for y in self.array.year.values if 2006 <= y < 2011]
        ] = hem.get_emissions_per_powertrain("CNG", euro_class=4)

        # Year index for EURO 3 pollution class, starts in 2001, ends in 2005
        self.array.loc[
            :, "ICEV-g", list_direct_emissions, [y for y in self.array.year.values if 2001 <= y < 2006]
        ] = hem.get_emissions_per_powertrain("CNG", euro_class=3)

        # Year index for EURO 2 pollution class, ends in 2000
        self.array.loc[
            :, "ICEV-g", list_direct_emissions, [y for y in self.array.year.values if y < 2001]
        ] = hem.get_emissions_per_powertrain("CNG", euro_class=2)

        # Applies an emission factor, useful for sensitivity purpose
        self.array.loc[:, "ICEV-g", list_direct_emissions, :] *= self.array.loc[
            :, "ICEV-g", "emission factor", :
        ]

    def set_noise_emissions(self):
        """
        Calculate noise emissions based on ``driving cycle``.
        The driving cycle is passed to the :class:`NoiseEmissionsModel` class and :meth:`get_sound_power_per_compartment`
        returns emissions per compartment type ("rural", "non-urban" and "urban") per second of driving cycle.

        Noise emissions are not differentiated by size classes at the moment, but only by powertrain "type"
        (e.g., combustion, hybrid and electric)

        :return: Does not return anything. Modifies ``self.array`` in place.
        """
        nem = NoiseEmissionsModel(self.ecm.cycle, self.ecm.cycle_name)

        list_noise_emissions = [
            "noise, octave 1, day time, urban",
            "noise, octave 2, day time, urban",
            "noise, octave 3, day time, urban",
            "noise, octave 4, day time, urban",
            "noise, octave 5, day time, urban",
            "noise, octave 6, day time, urban",
            "noise, octave 7, day time, urban",
            "noise, octave 8, day time, urban",
            "noise, octave 1, day time, suburban",
            "noise, octave 2, day time, suburban",
            "noise, octave 3, day time, suburban",
            "noise, octave 4, day time, suburban",
            "noise, octave 5, day time, suburban",
            "noise, octave 6, day time, suburban",
            "noise, octave 7, day time, suburban",
            "noise, octave 8, day time, suburban",
            "noise, octave 1, day time, rural",
            "noise, octave 2, day time, rural",
            "noise, octave 3, day time, rural",
            "noise, octave 4, day time, rural",
            "noise, octave 5, day time, rural",
            "noise, octave 6, day time, rural",
            "noise, octave 7, day time, rural",
            "noise, octave 8, day time, rural",
        ]

        self.array.loc[
            :, list(self.combustion), list_noise_emissions, :, :
        ] = nem.get_sound_power_per_compartment("combustion").reshape((24, 1, 1))
        self.array.loc[
            :, list(self.electric), list_noise_emissions, :, :
        ] = nem.get_sound_power_per_compartment("electric").reshape((24, 1, 1))
        self.array.loc[
            :, list(self.fuel_cell), list_noise_emissions, :, :
        ] = nem.get_sound_power_per_compartment("electric").reshape((24, 1, 1))
        self.array.loc[
            :, ["HEV-p", "HEV-d"], list_noise_emissions, :, :
        ] = nem.get_sound_power_per_compartment("hybrid").reshape((24, 1, 1))

    def calculate_cost_impacts(self, sensitivity=False, scope=None):
        """
        This method returns an array with cost values per vehicle-km, sub-divided into the following groups:

            * Purchase
            * Maintentance
            * Component replacement
            * Energy
            * Total cost of ownership

        :return: A xarray array with cost information per vehicle-km
        :rtype: xarray.core.dataarray.DataArray
        """

        if scope is None:
            scope = {}
            scope["size"] = self.array.coords["size"].values.tolist()
            scope["powertrain"] = self.array.coords["powertrain"].values.tolist()
            scope["year"] = self.array.coords["year"].values.tolist()
        else:
            scope["size"] = scope.get("size", self.array.coords["size"].values.tolist())
            scope["powertrain"] = scope.get(
                "powertrain", self.array.coords["powertrain"].values.tolist()
            )
            scope["year"] = scope.get("year", self.array.coords["year"].values.tolist())

        list_cost_cat = ["purchase", "maintenance", "component replacement", "energy", "total"]

        response = xr.DataArray(
            np.zeros(
                (len(scope['size']),
                 len(scope['powertrain']),
                 len(list_cost_cat),
                 len(scope['year']),
                 len(self.array.coords['value'].values))
            ),
            coords=[
                scope['size'],
                scope['powertrain'],
                ["purchase", "maintenance", "component replacement", "energy", "total"],
                scope['year'],
                self.array.coords['value'].values.tolist(),
            ],
            dims=["size", "powertrain", "cost_type", "year", "value"],
        )

        response.loc[
            :,:,["purchase", "maintenance", "component replacement", "energy", "total"],:,:
        ] = self.array.sel(powertrain=scope['powertrain'],
                           size=scope['size'],
                           year=scope['year'],
            parameter=["amortised purchase cost",
                       "maintenance cost",
                       "amortised component replacement cost",
                       "energy cost",
                       "total cost per km"]
        ).values

        if not sensitivity:
            return response
        else:
            return response/response.sel(value="reference")
