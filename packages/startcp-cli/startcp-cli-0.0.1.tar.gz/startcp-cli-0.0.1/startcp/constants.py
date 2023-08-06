from pathlib import Path

# STARTCP CONFIGURATIONS
startcp_default_folder = str(Path.home()) + "/" + "start_cp"
startcp_config_file = Path(startcp_default_folder + "/" + 'startcp_config.env')
# END

# CONSTANTS CONFIGURATIONS
is_setup_done = "IS_SETUP_DONE"
project_path = "PROJECT_PATH"
codechef = "CODECHEF"
use_template = "USE_TEMPLATE"
main_lang_template_path = "MAIN_LANG_TEMPLATE_PATH"
backup_lang_template_path = "BACKUP_LANG_TEMPLATE_PATH"
# END

# API CONFIGURATIONS
codechef_contest_api_url = "https://www.codechef.com/api/contests/"
# END
