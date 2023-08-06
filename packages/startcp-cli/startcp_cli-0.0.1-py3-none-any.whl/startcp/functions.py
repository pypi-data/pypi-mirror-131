import json
import requests
import re
import os
from dotenv import load_dotenv, find_dotenv

from startcp import printer, constants, codechef



rangebi = printer.Rangebi()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

try:
    if constants.startcp_config_file.is_file():
        load_dotenv(dotenv_path=str(constants.startcp_config_file))
    else:
        load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))
except Exception:
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))
    print(rangebi.get_in_info("Custom configuration file not loaded. Please fix the file first."))

platform_id = None


def run(args):

    comp_url = ''

    if args.generate:
        generate_start_cp_config_file()
        return

    if args.url:
        comp_url = args.url.lower()
    else:
        print(
            rangebi.get_in_success(
                "Enter Competition URL:"
            ),
            end=" "
        )
        comp_url = input()

    if not validate_url(comp_url):
        print(
            rangebi.get_in_danger(
                "URL is not valid. Please try again!"
            )
        )
        printer.new_lines()
        return
    else:
        perform_operations_on_url(comp_url)


def validate_url(comp_url):
    global platform_id

    # regex matching for codechef url
    codechef_validate_re = re.compile(r"^https://www.codechef.com/(\w+)(\?.*)?$")
    if(re.match(codechef_validate_re, comp_url)):
        platform_id = constants.codechef
        return True

    return False


def perform_operations_on_url(comp_url):
    params = parse_url(comp_url)

    if len(params) < 1:
        printer.new_lines()
        print(
            rangebi.get_in_danger(
                "Error parsing the URL!"
            )
        )
        printer.new_lines()
    else:
        prepare_battlezone(params, comp_url)


def parse_url(comp_url):
    problem_urls = []
    if platform_id == constants.codechef:
        problem_urls = codechef.get_codechef_problem_urls(comp_url)

    return problem_urls


def prepare_battlezone(problem_urls, comp_url):

    build_ships()

    if platform_id == constants.codechef:
        codechef.prepare_for_codechef_battle(problem_urls, comp_url)


def build_ships():
    if (not (os.getenv(constants.is_setup_done) is None)) and (int(os.getenv(constants.is_setup_done)) == 1):
        if not (os.getenv(constants.project_path) is None):
            os.chdir(os.getenv(constants.project_path))
        else:
            os.makedirs(constants.startcp_default_folder, exist_ok=True)
            os.chdir(constants.startcp_default_folder)
    else:
        # lets go home by default
        os.makedirs(constants.startcp_default_folder, exist_ok=True)
        os.chdir(constants.startcp_default_folder)


def generate_start_cp_config_file():

    if constants.startcp_config_file.is_file():
        print(
            rangebi.get_in_success(
                "Hey! Config file already generated."
            )
        )
    else:
        start_cp_configuration = """IS_SETUP_DONE = 0\nPROJECT_PATH = /home/user_name \nUSE_TEMPLATE = 0\nMAIN_LANG_TEMPLATE_PATH = /home/user_name \nBACKUP_LANG_TEMPLATE_PATH = /home/user_name \n"""
        os.makedirs(constants.startcp_default_folder, exist_ok=True)
        with open(str(constants.startcp_config_file), "w") as f:
            f.write(start_cp_configuration)
