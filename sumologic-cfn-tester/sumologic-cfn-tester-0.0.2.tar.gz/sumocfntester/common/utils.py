import importlib
import json
import os
import subprocess
import sys
import traceback

import cfn_flip
from common.objects import Level


def get_normalized_path(path):
    return os.path.realpath(os.path.abspath(os.path.expanduser(path)))


def check_valid_file(file_path):
    if not os.path.isfile(file_path):
        # traceback.print_exc()
        raise Exception("Provided path %s is not a valid file path." % file_path)
    return True


def get_absolute_path(relative_path, compare_file_path):
    if not os.path.isabs(relative_path):
        absolute_path = os.path.join(os.path.dirname(compare_file_path), relative_path)
        absolute_path = os.path.abspath(absolute_path)
        return absolute_path
    return relative_path


def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read().strip()


def load_json_file(file_full_path):
    """
    Load the given Test JSON file.
    """
    content = {}
    if check_valid_file(file_full_path):
        if ".schema" in file_full_path:
            with open(file_full_path, 'r') as fp:
                content = fp.read()
        else:
            content = cfn_flip.to_json(read_file(file_full_path))
    return json.loads(content)


def _run(command, input=None, check=False, **kwargs):
    if sys.version_info >= (3, 5):
        return subprocess.run(command, capture_output=True)
    if input is not None:
        if 'stdin' in kwargs:
            raise ValueError('stdin and input arguments may not both be used.')
        kwargs['stdin'] = subprocess.PIPE

    process = subprocess.Popen(command, **kwargs)
    try:
        stdout, stderr = process.communicate(input)
    except:
        process.kill()
        process.wait()
        raise
    retcode = process.poll()
    if check and retcode:
        raise subprocess.CalledProcessError(
            retcode, process.args, output=stdout, stderr=stderr)
    return retcode, stdout, stderr


def run_command(cmdargs):
    resp = _run(cmdargs)
    if len(resp.stderr.decode()) > 0:
        # traceback.print_exc()
        raise Exception("Error in run command %s cmd: %s" % (resp, cmdargs))
    return resp.stdout


def get_instance_of_process(process_name):
    modname, _, cls_name = process_name.rpartition('.')
    mod = importlib.import_module(modname)
    return getattr(mod, cls_name)


def generate_data_each_test_case(test_file_full_path):
    json_data = load_json_file(test_file_full_path)
    json_data = json.loads(os.path.expandvars(json.dumps(json_data)))
    processed_data = {}
    global_parameters = {}
    template_path = get_absolute_path(json_data["Global"]["TemplatePath"], test_file_full_path)
    if "GlobalParameters" in json_data["Global"]:
        global_parameters = json_data["Global"]["GlobalParameters"]
    for test in json_data["Tests"]:
        if "Skip" not in test or not test["Skip"]:
            all_parameters = global_parameters.copy()
            if "Parameters" in test:
                parameters = test["Parameters"]
                if "Path" in parameters:
                    parameter_values = load_json_file(get_absolute_path(parameters['Path'], test_file_full_path))
                    all_parameters.update(parameter_values)
                elif "Values" in parameters:
                    all_parameters.update(parameters['Values'])
            assertions = []
            if "Assertions" in test:
                assertions = test["Assertions"]

            regions = test["Regions"]

            processed_data[test["TestName"]] = {"parameters": all_parameters, "assertions": assertions,
                                                "regions": regions}

    # Divide test cases by regions also
    new_data = []
    for test_case, test_data in processed_data.items():
        for region in test_data["regions"]:
            new_data.append({"TestName": test_case, "Region": region,
                             "TestData": {"parameters": test_data["parameters"],
                                          "assertions": test_data["assertions"]}})

    return template_path, new_data, json_data["Global"]["ParallelTestsRun"]


def check_for_error(process_name, process_output):
    if process_output:
        sub_process_outputs = process_output[process_name]
        if sub_process_outputs:
            for sub_process_name, output in sub_process_outputs.items():
                if output:
                    errors = len(output.filter({"Level": Level.ERROR}))
                    if errors > 0:
                        return True
    return False
