import os
from pathlib import Path
import shutil
import re
import requests

from startcp import printer, constants



rangebi = printer.Rangebi()


def get_codechef_problem_urls(comp_url):
    problem_urls = []

    codechef_comp_id = get_codechef_competition_id(comp_url)
    if not (codechef_comp_id == ""):
        fetch_url = constants.codechef_contest_api_url + codechef_comp_id
        response = requests.get(fetch_url)
        if (response.status_code == 200):
            response = response.json()
            for problem in response["problems"].keys():
                problem_urls.append(
                    fetch_url+response["problems"][problem]["problem_url"])
    return problem_urls


def get_codechef_competition_id(comp_url):
    codechef_validate_re = re.compile(r"^https://www.codechef.com/(\w+)(\?.*)?$")
    search_result = re.search(codechef_validate_re, comp_url)
    try:
        return search_result.group(1)
    except:
        return ""


def prepare_for_codechef_battle(problem_urls, comp_url):

    codechef_comp_id = get_codechef_competition_id(comp_url)
    os.makedirs(codechef_comp_id, exist_ok=True)
    os.chdir(codechef_comp_id)

    problem_counter = 1
    for problem_url in problem_urls:
        problem_folder_name = str(problem_counter) + "_" + problem_url.split("/")[-1]
        os.makedirs(problem_folder_name, exist_ok=True)

        response = requests.get(problem_url)

        if (response.status_code == 200):

            response = response.json()

            if not os.path.isfile(problem_folder_name + "/" + "problem.html"):
                Path(problem_folder_name + "/" + "problem.html").touch()

            tmplt_file_created = True
            if (not (os.getenv(constants.use_template) is None)) and (int(os.getenv(constants.use_template)) == 1):
                try:
                    if not (os.getenv(constants.main_lang_template_path) is None):
                        if Path(os.getenv(constants.main_lang_template_path)).is_file():
                            shutil.copy(os.getenv(constants.main_lang_template_path), problem_folder_name + "/")
                            if not (os.getenv(constants.backup_lang_template_path) is None):
                                if Path(os.getenv(constants.backup_lang_template_path)).is_file():
                                    shutil.copy(os.getenv(constants.backup_lang_template_path), problem_folder_name + "/")
                        else:
                            tmplt_file_created = False
                    else:
                        tmplt_file_created = False
                except Exception:
                    tmplt_file_created = False
            else:
                tmplt_file_created = False

            if not tmplt_file_created:
                if not os.path.isfile(problem_folder_name + "/" + "sol.py"):
                    Path(problem_folder_name + "/" + "sol.py").touch()

                if not os.path.isfile(problem_folder_name + "/" + "sol.cpp"):
                    Path(problem_folder_name + "/" + "sol.cpp").touch()

            for sample_test_case in response["problemComponents"]["sampleTestCases"]:

                id = sample_test_case["id"]
                input_str = sample_test_case["input"]
                output_str = sample_test_case["output"]

                input_filename = problem_folder_name + "/" + "in" + str(id) + ".txt"
                output_filename = problem_folder_name + "/" + "out" + str(id) + ".txt"

                with open(input_filename, "w+") as outfile:
                    outfile.write(input_str)
                with open(output_filename, "w+") as outfile:
                    outfile.write(output_str)

        problem_counter += 1
