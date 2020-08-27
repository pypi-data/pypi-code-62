import os, json, logging

from ..app.cli import print_progress_bar

import numpy as np
from numpy import linalg
from numpy.random import uniform

from scipy.stats import rv_discrete, norm
from scipy.special import expit, logit


CONTINUE = 0
STOP = -1


class Module:
    """A modular component of an experiment. 
    The serialisable properties of this module should be immutable. 
    Ie the only stateful properties of a module are ephemeral and are discarded after use.
    """

    def __iter__(self):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    @classmethod
    def opts(cls):
        return [subclass.__name__ for subclass in cls.__subclasses__()]


#  Universal factory for modules that may or may not exhibit polymorphism
class ModuleFactory:
    def _get_module(self, base_cls, type=None, **kwargs):

        if len(base_cls.__subclasses__()) == 0:
            return base_cls(**kwargs)

        else:
            if type == None:
                type = base_cls.__subclasses__()[0].__name__

            for subclass in base_cls.__subclasses__():
                if type == subclass.__name__:
                    return subclass(**kwargs)

        raise AttributeError("Class {} has no subclass {}".format(base_cls, type))


class ChangeProcess(Module):
    def __init__(
        self,
        delay_cost=0.001,
        false_alarm_cost=1,
        max_duration=10000,
        observation_pdfs=None,
        initial_distribution=None,
        num_states=None,
        num_pre_change_states=None,
    ):

        if num_states is None:
            num_states = 5
        if num_pre_change_states is None:
            num_pre_change_states = 1

        self._delay_cost = 0.001
        self._false_alarm_cost = 1
        self._max_duration = 10000
        self._state_space = list(range(num_states))
        self._simulation_time = 0
        self._num_pre_change_states = num_pre_change_states
        self._history = np.zeros(self._max_duration, dtype=np.uint8)
        self._change_time = np.nan

        if initial_distribution is None:
            initial_distribution = [0] * num_states
            initial_distribution[0] = 1
        self._initial_distribution = rv_discrete(
            name="initial_distribution",
            values=(self._state_space, initial_distribution),
        )

        if observation_pdfs is None:
            observation_pdfs = []
            # [[0, 1], [0.1, 1], [0.2, 1], [0.5, 1]]
            for i, _ in enumerate(self._state_space):
                observation_pdfs.append([i * 0.1, 1])

        self._observation_pdfs = []

        for pdf in observation_pdfs:
            self._observation_pdfs.append(norm(pdf[0], pdf[1]))

        self._hidden_state = 0

    def __call__(self, action, dynamics):
        """[summary]

        Args:
            action ([type]): [description]
            dynamics (quickest.core.lib.Dynamics): The dynamics to use for the hidden state update

        Returns:
            [type]: [description]
        """

        cost = self._detection_penalty(action)

        if cost > 0.0:
            logging.debug(
                "Got penalty {} for action {} in state {}".format(
                    cost, action, self._hidden_state
                )
            )

        new_state = dynamics(self._hidden_state)

        if (np.isnan(self._change_time)) and not (
            new_state in list(range(self._num_pre_change_states))
        ):

            self._change_time = self._simulation_time
            logging.debug(
                "********* A CHANGE OCCURRED [{}/{}] ********".format(
                    self._change_time, self._max_duration
                )
            )

        self._hidden_state = new_state
        self._history[self._simulation_time] = self._hidden_state
        self._simulation_time = self._simulation_time + 1

        return cost

    def __iter__(self):
        yield ("delay_cost", self._delay_cost)
        yield ("false_alarm_cost", self._false_alarm_cost)
        yield ("max_duration", self._max_duration)
        yield ("num_states", len(self._state_space))
        yield ("num_pre_change_states", self._num_pre_change_states)
        yield ("initial_distribution", self._initial_distribution.pk.tolist())

        observation_pdfs = []
        for pdf in self._observation_pdfs:
            observation_pdfs.append(list(pdf.args))
        yield ("observation_pdfs", observation_pdfs)

    def __repr__(self):
        return "Change process with state space {}".format(self._state_space)

    @property
    def max_duration(self):
        return self._max_duration

    @property
    def num_states(self):
        return len(self._state_space)

    @property
    def num_pre_change_states(self):
        return self._num_pre_change_states

    @property
    def observation_pdfs(self):
        return self._observation_pdfs

    @property
    def state_history(self):
        return self._history

    @property
    def change_point(self):
        if not np.isnan(self._change_time):
            return self._change_time
        else:
            return None

    @property
    def initial_belief(self):
        return self._initial_distribution.pk.tolist()

    def observe(self):
        # TODO - sample from observation pdfs
        return self._observation_pdfs[self._hidden_state].rvs()

    def reset(self):
        self._hidden_state = self.sample_initial_state()
        self._history.fill(0)
        self._simulation_time = 0
        self._change_time = np.nan

    def sample_initial_state(self):
        return self._initial_distribution.rvs()

    # TODO How to handle different types of costs? Will action always be stop/go?

    def _detection_penalty(self, action):
        """Returns the cost of taking an action when only considering detection (not isolation)

        Args:
            action (int): 0 (continue) or 1 (stop)
        """

        # Check if simulation has finished
        penalty = 0

        if (action == STOP) or (
            action in list(range(self._num_pre_change_states, len(self._state_space)))
        ):

            if not np.isnan(self._change_time):

                time_since_change = np.float64(
                    self._simulation_time - self._change_time
                )

                # successful detection or isolation
                if action == STOP or action == self._hidden_state:
                    penalty = self._delay_cost * time_since_change
                else:
                    # unsuccessful isolation or false alarm
                    penalty = self._false_alarm_cost

                logging.debug(
                    "Stopped process {} steps after the change point".format(
                        time_since_change
                    )
                )
            else:
                logging.debug(
                    "False alarm applied at simulation timestep {}".format(
                        self._simulation_time
                    )
                )
                penalty = self._false_alarm_cost

        elif action == CONTINUE:

            if self._simulation_time == self._max_duration - 1 and not np.isnan(
                self._change_time
            ):

                logging.debug(
                    "Reached end of simulation without declaring change that occurred at {}".format(
                        self._change_time
                    )
                )

                if not np.isnan(self._change_time):
                    time_since_change = self._simulation_time - self._change_time
                    penalty = self._delay_cost * time_since_change

        else:
            raise ValueError(
                "action must be in one of 0 (continue), -1 (detect without isolation) or the number of the state to detect and isolate"
            )

        return np.float64(penalty)


class FilterMixin:
    def _filter(self, measurement, prior_belief, transition_matrix, observation_pdfs):
        """[summary]

        Args:
            measurement (float): 
            prior_belief (array-like): 
            transition_matrix ([type]): 
            observation_pdfs ([list of scipy.stats.rv_discrete]):
        """

        likelihoods = np.zeros_like(observation_pdfs)

        for i in range(len(observation_pdfs)):
            likelihood = observation_pdfs[i].pdf(measurement)
            likelihoods[i] = likelihood

        N = len(likelihoods)
        likelihood_matrix = np.zeros((N, N), dtype=np.float64)

        for i in range(N):
            likelihood_matrix[i, i] = likelihoods[i]

        unnormalised_estimate = np.matmul(
            np.matmul(likelihood_matrix, np.transpose(transition_matrix)), prior_belief
        )

        belief = unnormalised_estimate / np.sum(unnormalised_estimate)

        return belief


class Policy(Module):
    def __call__(self):
        raise NotImplementedError

    @property
    def params(self):
        return self._deparameterise(self._free_params)

    @params.setter
    def params(self, var):

        params = np.array(var, dtype=np.float64)
        free_params = self._reparameterise(params)

        if isinstance(free_params, int) or isinstance(free_params, float):
            free_params = np.array([free_params], dtype=np.float64)
        self._free_params = free_params

    @property
    def free_params(self):
        """
        Returns:
            [numpy array of float64]: The free optimisation parameters used by solvers 
        """
        return self._free_params

    @free_params.setter
    def free_params(self, var):
        if isinstance(var, int) or isinstance(var, float):
            free_params = np.array([var], dtype=np.float64)
        else:
            free_params = np.array(var, dtype=np.float64)
        self._free_params = free_params

    @staticmethod
    def _reparameterise(decision_parameters):
        # decision_parameter(s) to free params
        raise NotImplementedError

    @staticmethod
    def _deparameterise(free_parameters, **kwargs):
        # free params to decision_parameters
        raise NotImplementedError


class Threshold(Policy):
    def __init__(self, threshold=None, **kwargs):
        """A detector that marginalises pre- and post-belief states to the belief 
        that the change has or has not occurred, then compares that belief
        to a scalar threshold in [0,1].

        Args:
            threshold (float): The decision threshold. Defaults to 0.5.
        """
        if threshold == None:
            threshold_ = 0.5
        else:
            threshold_ = threshold
        self.free_params = self._reparameterise(threshold_)

    def __repr__(self):
        return "Threshold"

    def __iter__(self):
        yield ("type", self.__repr__())
        yield ("threshold", self.threshold)

    def __call__(self, belief, num_pre_change_states):
        """The core policy method

        Args:
            belief (Array-like): A N-dimensional array in belief space 
            num_pre_change_states (int): the first N elements in the belief
            array are pre-change states.
        Returns:
            [int]: 0 for continue, 1 for stop
        """

        probability_no_change = np.sum(belief[:num_pre_change_states])
        probability_of_change = 1 - probability_no_change

        if probability_of_change < self.threshold:
            action = CONTINUE
        else:
            logging.debug(
                "Decided to stop, probability of change: {}, threshold: {}".format(
                    probability_of_change, self.threshold
                )
            )
            action = STOP
        return action

    @property
    def threshold(self):
        return self.params[0]

    @threshold.setter
    def threshold(self, val):
        self.params = [val]

    @staticmethod
    def _reparameterise(params, **kwargs):
        """Convert decision boundary to free optimisation parameter

        Args:
            params (float): Decision boundary (threshold)

        Returns:
            [np.ndarray of float64]: free optimisation parameter parameter
        """
        return logit(params)

    @staticmethod
    def _deparameterise(free_params):
        """Converts free parameters to a decision parameter

        Args:
            free_params (array of numpy.float64): A free optimisation parameter

        Returns:
            [float]: Decision threshold
        """
        return expit(free_params)


class Hyperplanes(Policy):
    def __init__(self, num_states=None, num_pre_change_states=None, planes=None):

        if planes is not None:
            num_post_change_states = np.array(planes).shape[0]
            self._free_params = self._reparameterise(planes)

        # The constructor needs to initialise a set of valid hyperplanes
        else:

            if num_states is None:
                num_states = 3

            if num_pre_change_states is None:
                num_pre_change_states = 1

            num_post_change_states = num_states - num_pre_change_states

            param_size = (num_post_change_states, num_states)

            self._free_params = uniform(size=param_size)
            print("Hyperplanes constructor set params : {}".format(self._free_params))
        self._num_post_change_states = num_post_change_states

    def __call__(self, belief, *args, **kwargs):

        for state, plane in zip(self.post_change_states, self.planes):
            test_statistic = np.dot(belief, plane)
            if test_statistic < 0:
                return state

        return CONTINUE

    def __repr__(self):
        return "Hyperplanes"

    def __iter__(self):
        yield ("type", self.__repr__())
        yield ("planes", [list(p) for p in self.planes])

    @property
    def planes(self):
        params = self._deparameterise(self._free_params)
        # planes = {}
        # for state, param in zip(self.post_change_states, params):
        #     planes[str(state)] = list(param)
        # return planes
        return params

    @property
    def post_change_states(self):
        num_states = self._free_params.shape[
            1
        ]  # 0 is number of planes, 1 is belief space dimension
        first_post_change_state = num_states - self._num_post_change_states
        return list(range(first_post_change_state, num_states))

    @staticmethod
    def _reparameterise(planes):
        # decision parameters to free params

        free_params = np.zeros_like(planes, dtype=np.float64)
        planes = np.array(planes)

        num_states = np.array(free_params).shape[1]
        num_post_change_states = np.array(free_params).shape[0]

        first_post_change_state = num_states - num_post_change_states
        post_change_states = list(range(first_post_change_state, num_states))

        for state, (j, plane) in zip(post_change_states, enumerate(planes)):

            for i, var in enumerate(plane):

                free_params[j, i] = 10
                if i == state:

                    if not var < 0:
                        raise ValueError(
                            "Invalid plane. The parameter corresponding to the belief state must be < 0."
                        )
                    new_val = np.arcsin(np.sqrt(-var))
                    free_params[j, i] = new_val
                else:

                    if not var > 0:
                        raise ValueError(
                            "Invalid plane. Parameters other than the belief state must be > 0."
                        )

                    free_params[j, i] = np.arcsin(np.sqrt(var))

        return free_params

    @staticmethod
    def _deparameterise(free_parameters):
        # free params to decision parameters

        params = np.zeros_like(free_parameters)
        num_states = params.shape[1]
        num_post_change_states = params.shape[0]
        num_pre_change_states = num_states - num_post_change_states
        post_change_states = list(range(num_pre_change_states, num_states))

        for state, (i, free_param) in zip(
            post_change_states, enumerate(free_parameters)
        ):
            # the state param needs to map to [-1,0]
            # all others map to [0,1]

            params[i, :] = np.square(np.sin(free_param))
            params[i, state] = -params[i, state]

        return params


class Ellipsoids(Policy):
    """A decision policy where a change is declared if the belief state enters 
    the volume of an ellipsoid centred on the vertex of the belief simplex.
    The number of coefficients per ellipsoid is equal to the ambient dimension of the belief space.
    """

    def __init__(self, num_states=None, num_pre_change_states=None, ellipsoids=None):
        if ellipsoids is not None:

            # We need an ellipsoid rule for each post change state
            num_post_change_states = np.array(ellipsoids).shape[0]
            self._free_params = self._reparameterise(np.array(ellipsoids))

        else:

            if num_states is None:
                num_states = 3

            if num_pre_change_states is None:
                num_pre_change_states = 1

            num_post_change_states = num_states - num_pre_change_states

            if num_post_change_states < 1:
                raise AttributeError(
                    "Invalid number of pre- ({}) and post- ({}) change states".format(
                        num_pre_change_states, num_post_change_states
                    )
                )

            param_size = (num_post_change_states, num_states)

            self._free_params = np.ones(size=param_size)

            logging.info(
                "Ellipsoid constructor set params : {}".format(self._free_params)
            )
        self._num_post_change_states = num_post_change_states

    def __call__(self, belief, *args, **kwargs):

        num_states = self._free_params.shape[1]

        for state, ellipsoid in zip(self.post_change_states, self.ellipsoids):
            test_statistic = 0
            # For each state, add to the accumulator
            for i in range(num_states):
                if i == state:
                    test_statistic += np.square((belief[i] - 1.0)) / np.square(
                        ellipsoid[i]
                    )  # this is the vertex that the ellipsoid is centred on
                else:
                    test_statistic += np.square(belief[i]) / np.square(
                        ellipsoid[i]
                    )  # just add
            if test_statistic < 1:
                logging.debug("Collision detected for state {}".format(state))

                return state

        return CONTINUE

    def __repr__(self):
        return "Ellipsoids"

    def __iter__(self):
        yield ("type", self.__repr__())
        yield ("ellipsoids", [list(e) for e in self.ellipsoids])

    @property
    def ellipsoids(self):
        ellipsoids = self._deparameterise(self._free_params)
        # planes = {}
        # for state, param in zip(self.post_change_states, params):
        #     planes[str(state)] = list(param)
        # return planes
        return ellipsoids

    @property
    def post_change_states(self):
        num_states = self._free_params.shape[
            1
        ]  # 0 is number of planes, 1 is belief space dimension
        first_post_change_state = num_states - self._num_post_change_states
        return list(range(first_post_change_state, num_states))

    @staticmethod
    def _reparameterise(ellipsoid_coefficients):
        """Convert the ellipsoid coefficients to free optimization parameters

        TODO EXPLAIN CHOICE OF REPARAMETERISATION

        Args:
            ellipsoid_coefficients (numpy.ndarray): MxN where M is the number of anomalies and N is the number of dimensions in belief space.
            The a, b, c .. etc that appear in the equation for an ellipsoid

        Returns:
            numpy.ndarray: Optimisation parameters
        """
        return expit(ellipsoid_coefficients / np.sqrt(2))

    @staticmethod
    def _deparameterise(free_parameters):
        """Convert the free optimisation parameters to the coefficients in an ellipsoid equation
        Eg in three dimensions x^2/a^2 + y^2/b^2 + z^2/c^2, the ellipsoid coefficients are a, b and c

        Args:
            free_parameters ([type]): [description]

        Returns:
            [type]: [description]
        """
        return np.sqrt(2) * logit(free_parameters)


class Dynamics(Module):
    # TODO COMMON METHODS

    @property
    def transition_matrix(self):
        raise NotImplementedError


class MarkovChain(Dynamics):
    def __init__(self, mockdata=[3, 5, 6]):
        self.data = mockdata

    def __repr__(self):
        return "MarkovChain"

    def __iter__(self):
        yield ("type", self.__repr__())
        yield ("mock", self.data)

    @property
    def transition_matrix(self):
        pass


class AugmentedHMM(Dynamics):
    def __init__(
        self,
        change_point_matrix=None,
        geometric_prior_matrix=None,
        pre_change_point_matrix=None,
        post_change_point_matrix=None,
        num_states=None,
        num_pre_change_states=None,
    ):

        if (pre_change_point_matrix is not None) and (
            post_change_point_matrix is not None
        ):
            num_pre_change_states = len(pre_change_point_matrix)
            num_post_change_states = len(post_change_point_matrix)
            num_states = num_pre_change_states + num_post_change_states
        else:
            if num_states is None:
                num_states = 5

            if num_pre_change_states is None:
                num_pre_change_states = 1

            num_post_change_states = num_states - num_pre_change_states

        # the probability of each pre-change state transitioning to each post-change staet
        if change_point_matrix is not None:
            self._change_point_matrix = np.array(change_point_matrix)
        else:
            m = np.ones(
                (num_pre_change_states, num_post_change_states), dtype=np.float64
            ) / np.float64(num_post_change_states)
            self._change_point_matrix = m

        # Geometric prior matrix is the probably of transitioning from each pre-change state to each post-change state
        if geometric_prior_matrix is not None:
            self._geometric_prior_matrix = np.array(geometric_prior_matrix)
        else:
            m = np.array([[0.99, 0.01], [0.0, 1.0]], dtype=np.float64)
            self._geometric_prior_matrix = m

        # the probability of transitions within the pre-change states
        if pre_change_point_matrix is not None:
            self._pre_change_point_matrix = np.array(pre_change_point_matrix)
        else:
            m = np.ones(
                (num_pre_change_states, num_pre_change_states), dtype=np.float64
            ) / np.float64(num_pre_change_states)
            self._pre_change_point_matrix = m

        if post_change_point_matrix is not None:
            self._post_change_point_matrix = np.array(post_change_point_matrix)
        else:
            m = np.ones(
                (num_post_change_states, num_post_change_states), dtype=np.float64
            ) / np.float64(num_post_change_states)
            self._post_change_point_matrix = m

        self._transition_matrix = self._get_transition_matrix(
            self._change_point_matrix,
            self._geometric_prior_matrix,
            self._pre_change_point_matrix,
            self._post_change_point_matrix,
        )

        self._transition_distributions = []

        state_space = tuple(range(num_states))

        for row in self._transition_matrix:
            pk_norm = row / np.float64(np.sum(row))
            self._transition_distributions.append(
                rv_discrete(
                    name="transition distribution", values=(state_space, pk_norm),
                )
            )

    def __repr__(self):
        return "AugmentedHMM"

    def __iter__(self):
        yield ("type", self.__repr__())
        yield ("change_point_matrix", self._change_point_matrix.tolist())
        yield ("geometric_prior_matrix", self._geometric_prior_matrix.tolist())
        yield ("pre_change_point_matrix", self._pre_change_point_matrix.tolist())
        yield ("post_change_point_matrix", self._post_change_point_matrix.tolist())

    def __call__(self, old_state):
        return self._transition_distributions[old_state].rvs()

    @property
    def transition_matrix(self):
        return self._transition_matrix

    @staticmethod
    def _get_transition_matrix(
        change_point_matrix,
        geometric_prior_matrix,
        pre_change_point_matrix,
        post_change_point_matrix,
    ):

        num_pre_change_states = pre_change_point_matrix.shape[0]
        num_post_change_states = post_change_point_matrix.shape[0]

        dim = num_pre_change_states + num_post_change_states
        matrix = np.zeros((dim, dim), dtype=np.float64)

        matrix[:num_pre_change_states, :num_pre_change_states] = (
            geometric_prior_matrix[0, 0] * pre_change_point_matrix
        )

        matrix[:num_pre_change_states, num_pre_change_states:] = (
            geometric_prior_matrix[0, 1] * change_point_matrix
        )

        matrix[num_pre_change_states:, num_pre_change_states:] = (
            geometric_prior_matrix[1, 1] * post_change_point_matrix
        )

        # TODO ADD CASE WHERE CHANGE CAN SWITCH OFF

        return matrix


class _StoppingProblem(ModuleFactory, FilterMixin):
    modules = {"change_process": ChangeProcess, "dynamics": Dynamics, "policy": Policy}

    def __init__(
        self, dynamics={}, policy={}, change_process={},
    ):

        if "num_states" not in change_process.keys():
            change_process["num_states"] = 5
        if "num_pre_change_states" not in change_process.keys():
            change_process["num_pre_change_states"] = 1

        self._changeProcess = self._get_module(ChangeProcess, **change_process)
        logging.debug(
            "Stopping problem got change process {}".format(self._changeProcess)
        )

        self._dynamics = self._get_module(
            Dynamics,
            **dynamics,
            num_states=change_process["num_states"],
            num_pre_change_states=change_process["num_pre_change_states"]
        )

        logging.debug("Stopping problem got dynamics {}".format(self._dynamics))
        self._policy = self._get_module(
            Policy,
            **policy,
            num_states=change_process["num_states"],
            num_pre_change_states=change_process["num_pre_change_states"]
        )

        logging.debug("Stopping problem got policy {}".format(self._policy))

    def __iter__(self):
        yield ("change_process", dict(self._changeProcess))
        yield ("dynamics", dict(self._dynamics))
        yield ("policy", dict(self._policy))

    def run(self):

        self._changeProcess.reset()
        logging.debug("Reset change process")

        filt_hist = np.zeros(
            (self._changeProcess.max_duration, self._changeProcess.num_states),
            dtype=np.float64,
        )
        obs_hist = np.zeros(self._changeProcess.max_duration, dtype=np.float64)

        cost = 0
        k = 0

        # Get an initial belief
        belief = self._changeProcess.initial_belief
        logging.debug("Stopping problem got initial belief {}".format(belief))
        logging.debug("Starting simulation run...")
        while cost == 0 and k < self._changeProcess.max_duration:

            observation = self._changeProcess.observe()
            obs_hist[k] = observation

            belief = self._filter(
                observation,
                belief,
                self._dynamics.transition_matrix,
                self._changeProcess.observation_pdfs,
            )

            filt_hist[k, :] = belief

            action = self._policy(belief, self._changeProcess._num_pre_change_states)
            cost = self._changeProcess(action, self._dynamics)
            k = k + 1

        state_history = self._changeProcess.state_history

        filt_hist = filt_hist[:k, :]
        obs_hist = obs_hist[:k]
        state_history = state_history[:k]

        state_space = list(range(self._changeProcess.num_states))

        result = {
            "cost": cost,
            "filter_history": filt_hist,
            "observation_history": obs_hist,
            "state_history": state_history,
            "pre_change_states": state_space[
                : self._changeProcess.num_pre_change_states
            ],
            "post_change_states": state_space[
                self._changeProcess.num_pre_change_states :
            ],
        }

        if self._changeProcess.change_point:
            result["change_point"] = self._changeProcess.change_point

        return result

    def optimise(
        self,
        steps=100,
        initial_lr=10,
        decay_constant=1.5,
        samples_per_step=10,
        backend=None,
    ):

        logging.debug("Optimising for {} steps".format(steps))

        param_history = np.zeros([steps] + list(self._policy.params.shape))
        eval_cost_history = np.zeros(steps)

        for step in range(steps):

            logging.debug("Started optimisation step {}".format(step))

            old_params = self._policy.free_params

            # Symmetric binomial
            perturbation_vector = np.random.binomial(
                1, 0.5, self._policy.free_params.shape
            ).astype(np.float64)

            perturbation_vector[np.isclose(perturbation_vector, 0)] = -1

            params1 = old_params + perturbation_vector
            params2 = old_params - perturbation_vector

            self._policy.free_params = params1
            loss_accumulator = np.float64(0)

            for i in range(samples_per_step):
                logging.debug(
                    "Params 1 - getting loss score {}/{}".format(i, samples_per_step)
                )
                result = self.run()
                loss_accumulator = loss_accumulator + result["cost"]

                # TODO SAVE RESULT TO BACKEND

            expected_loss_1 = loss_accumulator / np.float64(samples_per_step)
            logging.debug("Expected loss for params 1: {}".format(expected_loss_1))

            self._policy.free_params = params2
            loss_accumulator = np.float64(0)

            for i in range(samples_per_step):
                result = self.run()
                loss_accumulator = loss_accumulator + result["cost"]
                # TODO SAVE RESULT TO BACKEND
            expected_loss_2 = loss_accumulator / np.float64(samples_per_step)

            gradient = (expected_loss_1 - expected_loss_2) / (2 * perturbation_vector)
            logging.debug("Gradient: {}".format(gradient))
            # BACKPROP GRADIENT

            learning_rate = initial_lr * np.exp(
                -np.float64(step) * np.float64(decay_constant) / np.float64(steps)
            )  # TODO SCHEDULE

            logging.debug("Learning rate: {}".format(learning_rate))
            new_params = old_params - learning_rate * gradient

            # deparameterise

            self._policy.free_params = new_params
            param_history[step,] = self._policy.params

            evaluation = self.run()
            eval_cost_history[step] = evaluation["cost"]

            print_progress_bar(step, steps)

        # TODO INITIAL LEARNING RATE, DECAY CONSTANT
        return param_history, eval_cost_history

