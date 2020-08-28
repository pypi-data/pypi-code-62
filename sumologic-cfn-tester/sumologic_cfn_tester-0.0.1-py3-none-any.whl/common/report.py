import datetime
import json
import os

from common.utils import load_json_file, get_absolute_path

from common.objects import Level


class ReportGeneration(object):

    # Create Report as per test case with all stages it passed through.
    @staticmethod
    def generate_report(output, test_file_path, template_path, logger):

        all_test_cases = {}
        skipped_cases = 0
        json_data = load_json_file(os.path.realpath(test_file_path))
        total_tests = 0
        for test in json_data["Tests"]:
            if "Skip" in test and test["Skip"]:
                skipped_cases = skipped_cases + 1
                total_tests += 1
            else:
                for region in test["Regions"]:
                    all_test_cases[test["TestName"] + "#" + region] = "PASS"
                    total_tests += 1

        test_cases = []
        if output:
            for element in output:
                processes = {}
                test_case_errors = 0
                process_names = element["Validations"]
                test_name = element["TestName"]
                region = element["Region"]
                element["Status"] = "PASS"
                for process in process_names:
                    for process_name, sub_process_names in process.items():
                        sub_processes = []
                        for sub_process_name, issues in sub_process_names.items():
                            error_warning = {}
                            if issues:
                                errors = len(issues.filter({"Level": Level.ERROR}))
                                warnings = len(issues.filter({"Level": Level.WARNING}))
                                if errors > 0 or warnings > 0:
                                    error_warning[sub_process_name] = {"Errors": errors, "Warnings": warnings}
                                test_case_errors += errors
                            if error_warning:
                                sub_processes.append(error_warning)
                        if sub_processes:
                            processes[process_name] = sub_processes
                if processes:
                    test_cases.append(
                        {"TestName": test_name, "Region": region, "Status": "FAIL" if test_case_errors > 0 else "PASS",
                         "Validations": processes})
                if test_case_errors > 0:
                    element["Status"] = "FAIL"
                    all_test_cases[test_name + "#" + region] = "FAIL"

        failed_cases = sum(status == "FAIL" for status in all_test_cases.values())
        passed_cases = sum(status == "PASS" for status in all_test_cases.values())

        if (passed_cases + failed_cases + skipped_cases) != total_tests:
            raise Exception(
                "Issue with Report Generation as Total Test cases(%s) "
                "does not match Passed(%s) + Failed(%s)+ Skipped(%s) Test Cases" % (
                    total_tests, passed_cases, failed_cases, skipped_cases))

        # Create Result file
        with open("report.json", 'w') as parameter:
            json.dump(output, parameter, indent=4, default=ReportGeneration.object_to_dictionary)

        # Creating report data
        report = {"Template": template_path,
                  "ReportPath": os.path.abspath("report.json"),
                  "Status": "FAIL" if failed_cases > 0 else "PASS",
                  "TestResult": {"Total": total_tests, "Pass": passed_cases, "Fail": failed_cases,
                                 "Skipped": skipped_cases}}
        # "Report_Status": test_cases}

        logger.info("Report for CloudFormation Testing is : \n %s" % (json.dumps(report, indent=4)))

    @staticmethod
    def object_to_dictionary(obj):
        if isinstance(obj, datetime.date):
            return obj.strftime("%m/%d/%Y, %H:%M:%S %p")
        else:
            return obj.__dict__
