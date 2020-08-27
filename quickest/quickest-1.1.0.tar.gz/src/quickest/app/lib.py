import os, sys, json, logging
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt

from .cli import splash, list_menu, app_menu, input_prompt
from .io import load_config, get_logger

from ..core.api import StoppingProblem
from ..core.schema import Adapter, ExperimentSchema
from ..backend import Backend


# Applications built using the core API and backend functionality


def simulate(experiment_config, backend_config):

    logging.info("Entered simulation")

    backend = Backend(**backend_config)
    stoppingProblem = StoppingProblem.from_config(experiment_config)

    logging.debug("Got stopping problem from config {}".format(stoppingProblem))
    result = stoppingProblem.run()

    experiment_config["results"] = result
    experiment_config["results"]["timestamp"] = datetime.now().isoformat()

    experiment_dict = Adapter.jsonify(experiment_config)

    backend.save(experiment_dict)
    return 0


def optimise(
    experiment_config, backend_config, steps=100, initial_lr=1, decay_constant=1.5
):

    backend = Backend(**backend_config)
    # logger = get_logger()

    # logger.info("Got logger {}".format(logger))

    stoppingProblem = StoppingProblem.from_config(experiment_config)

    param_history, cost_history = stoppingProblem.optimise(
        backend=backend,
        steps=steps,
        initial_lr=initial_lr,
        decay_constant=decay_constant,
    )

    experiment_config = dict(stoppingProblem)  # Get the optimised results
    result = stoppingProblem.run()
    adapter = Adapter()

    experiment_config["results"] = result
    experiment_config["results"]["timestamp"] = datetime.now().isoformat()
    experiment_config["solver"] = {}
    experiment_config["solver"]["parameter_history"] = param_history
    experiment_config["solver"]["cost_history"] = cost_history
    experiment_config["solver"]["initial_lr"] = initial_lr
    experiment_config["solver"]["decay_constant"] = decay_constant

    experiment_dict = Adapter.jsonify(experiment_config)
    backend.save(experiment_dict)
    return 0


def view_simulation(backend_config):

    FOLDER = backend_config["loc"]
    files = [
        f
        for f in os.listdir(FOLDER)
        if (
            os.path.isfile(os.path.join(FOLDER, f))
            and os.path.splitext(os.path.join(FOLDER, f))[-1] == ".json"
        )
    ]
    if not files:
        print("No json files in chosen directory {}".format(FOLDER))
        sys.exit(1)

    files.sort(reverse=True)
    file_options = {"file": files}

    experiment_file = list_menu(file_options)["file"]

    file_to_load = os.path.join(FOLDER, experiment_file)
    with open(file_to_load) as f:
        data = json.load(f)

    results = data["results"]

    es = ExperimentSchema()

    validated_results_data = es.load(results)

    filter_history = np.array(validated_results_data["filter_history"])
    observation_history = np.array(validated_results_data["observation_history"])
    state_history = np.array(validated_results_data["state_history"])

    post_change_belief = np.sum(
        filter_history[:, validated_results_data["post_change_states"]], 1
    )

    CHANGE_PT_COLOUR = "m"

    t = np.linspace(1, len(state_history), len(state_history))
    plt.subplot(311)
    plt.plot(t, state_history)

    plt.subplot(312)
    plt.plot(t, post_change_belief)
    axes = plt.gca()
    axes.set_ylim([0, 1])

    plt.subplot(313)
    plt.plot(t, observation_history)

    if validated_results_data["change_point"] is not None:
        change_point = validated_results_data["change_point"]
        plt.axvline(change_point, c=CHANGE_PT_COLOUR, ymin=0, ymax=1)

    FORMAT = ".png"
    SAVE_LOCATION = input_prompt(msg="Save to:", default=FOLDER)
    SAVE_FILE = os.path.splitext(experiment_file)[0] + FORMAT

    OUT_FILE = os.path.join(SAVE_LOCATION, SAVE_FILE)

    plt.savefig(OUT_FILE)

    print("Saved to {}".format(OUT_FILE))
    plt.show()


def get_config(config, **kwargs):

    cwd = os.getcwd()
    filename = os.path.join(cwd, "config.json")

    with open(filename, "w") as outfile:
        json.dump(config, outfile)

    print("Written config to {}".format(filename))


application_types = {
    "simulate": simulate,
    "optimise": optimise,
    "view": view_simulation,
    "getconf": get_config,
}


def get_app_list():
    return list(application_types.keys())


def launch(args):

    splash("gotta go fast")

    logger = get_logger()
    logger.info("Got logger {}".format(logger))

    if args.application:
        application_str = args.application
    else:
        application_str = app_menu(application_types)

    if args.loc:
        outfolder = args.loc
    else:
        outfolder = os.getcwd()

    backend_config = {"loc": outfolder}

    if application_str == "view":
        return view_simulation(backend_config)

    if args.conf:
        print("Got config file {}".format(args.conf))
        config_dict = load_config(args.conf)

    else:
        print("No config supplied - creating one now")

        num_states = int(input_prompt(msg="Enter belief space dimensions", default="3"))

        num_pre_change_states = num_states - int(
            input_prompt(msg="Enter the number of post-change states", default="1")
        )

        class_opts = list_menu(StoppingProblem.get_opts())

        choices = {
            "num_states": num_states,
            "num_pre_change_states": num_pre_change_states,
            **class_opts,
        }
        config_dict = StoppingProblem.get_config(choices)

    if application_str == "getconf":
        return get_config(config_dict)
    elif application_str == "optimise":
        if not args.steps:
            steps = 100
        else:
            steps = args.steps

        if not args.lr:
            initial_lr = 1
        else:
            initial_lr = args.lr

        if not args.decay:
            decay_constant = 1.5
        else:
            decay_constant = args.decay
        print(
            "Optimising for {} steps with initial learning rate {} and decay constant {}".format(
                steps, initial_lr, decay_constant
            )
        )
        return optimise(
            config_dict,
            backend_config,
            steps=steps,
            initial_lr=initial_lr,
            decay_constant=decay_constant,
        )
    else:
        return application_types[application_str](config_dict, backend_config)

