"""
    pint.babel
    ~~~~~~~~~~

    :copyright: 2016 by Pint Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from .compat import HAS_BABEL

_babel_units = dict(
    standard_gravity="acceleration-g-force",
    millibar="pressure-millibar",
    metric_ton="mass-metric-ton",
    megawatt="power-megawatt",
    degF="temperature-fahrenheit",
    dietary_calorie="energy-foodcalorie",
    millisecond="duration-millisecond",
    mph="speed-mile-per-hour",
    acre_foot="volume-acre-foot",
    mebibit="digital-megabit",
    gibibit="digital-gigabit",
    tebibit="digital-terabit",
    mebibyte="digital-megabyte",
    kibibyte="digital-kilobyte",
    mm_Hg="pressure-millimeter-of-mercury",
    month="duration-month",
    kilocalorie="energy-kilocalorie",
    cubic_mile="volume-cubic-mile",
    arcsecond="angle-arc-second",
    byte="digital-byte",
    metric_cup="volume-cup-metric",
    kilojoule="energy-kilojoule",
    meter_per_second_squared="acceleration-meter-per-second-squared",
    pint="volume-pint",
    square_centimeter="area-square-centimeter",
    in_Hg="pressure-inch-hg",
    milliampere="electric-milliampere",
    arcminute="angle-arc-minute",
    MPG="consumption-mile-per-gallon",
    hertz="frequency-hertz",
    day="duration-day",
    mps="speed-meter-per-second",
    kilometer="length-kilometer",
    square_yard="area-square-yard",
    kelvin="temperature-kelvin",
    kilogram="mass-kilogram",
    kilohertz="frequency-kilohertz",
    megahertz="frequency-megahertz",
    meter="length-meter",
    cubic_inch="volume-cubic-inch",
    kilowatt_hour="energy-kilowatt-hour",
    second="duration-second",
    yard="length-yard",
    light_year="length-light-year",
    millimeter="length-millimeter",
    metric_horsepower="power-horsepower",
    gibibyte="digital-gigabyte",
    # 'temperature-generic',
    liter="volume-liter",
    turn="angle-revolution",
    microsecond="duration-microsecond",
    pound="mass-pound",
    ounce="mass-ounce",
    calorie="energy-calorie",
    centimeter="length-centimeter",
    inch="length-inch",
    centiliter="volume-centiliter",
    troy_ounce="mass-ounce-troy",
    gram="mass-gram",
    kilowatt="power-kilowatt",
    knot="speed-knot",
    lux="light-lux",
    hectoliter="volume-hectoliter",
    microgram="mass-microgram",
    degC="temperature-celsius",
    tablespoon="volume-tablespoon",
    cubic_yard="volume-cubic-yard",
    square_foot="area-square-foot",
    tebibyte="digital-terabyte",
    square_inch="area-square-inch",
    carat="mass-carat",
    hectopascal="pressure-hectopascal",
    gigawatt="power-gigawatt",
    watt="power-watt",
    micrometer="length-micrometer",
    volt="electric-volt",
    bit="digital-bit",
    gigahertz="frequency-gigahertz",
    teaspoon="volume-teaspoon",
    ohm="electric-ohm",
    joule="energy-joule",
    cup="volume-cup",
    square_mile="area-square-mile",
    nautical_mile="length-nautical-mile",
    square_meter="area-square-meter",
    mile="length-mile",
    acre="area-acre",
    nanometer="length-nanometer",
    hour="duration-hour",
    astronomical_unit="length-astronomical-unit",
    liter_per_100kilometers="consumption-liter-per-100kilometers",
    megaliter="volume-megaliter",
    ton="mass-ton",
    hectare="area-hectare",
    square_kilometer="area-square-kilometer",
    kibibit="digital-kilobit",
    mile_scandinavian="length-mile-scandinavian",
    liter_per_kilometer="consumption-liter-per-kilometer",
    century="duration-century",
    cubic_foot="volume-cubic-foot",
    deciliter="volume-deciliter",
    # pint='volume-pint-metric',
    cubic_meter="volume-cubic-meter",
    cubic_kilometer="volume-cubic-kilometer",
    quart="volume-quart",
    cc="volume-cubic-centimeter",
    pound_force_per_square_inch="pressure-pound-per-square-inch",
    milligram="mass-milligram",
    kph="speed-kilometer-per-hour",
    minute="duration-minute",
    parsec="length-parsec",
    picometer="length-picometer",
    degree="angle-degree",
    milliwatt="power-milliwatt",
    week="duration-week",
    ampere="electric-ampere",
    milliliter="volume-milliliter",
    decimeter="length-decimeter",
    fluid_ounce="volume-fluid-ounce",
    nanosecond="duration-nanosecond",
    foot="length-foot",
    karat="proportion-karat",
    year="duration-year",
    gallon="volume-gallon",
    radian="angle-radian",
)

if not HAS_BABEL:
    _babel_units = {}

_babel_systems = dict(mks="metric", imperial="uksystem", US="ussystem")

_babel_lengths = ["narrow", "short", "long"]
