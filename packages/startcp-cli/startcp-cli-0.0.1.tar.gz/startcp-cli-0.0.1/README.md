>
>    Don't Forget To Update StartCp-Cli Frequently, Thank You For Using

>    Use `pip install -U startcp-cli` or `pip install startcp-cli==x.y.z` x.y.z is the latest version
>

## Startcp-Cli

<P>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A CLI application for generating battlespace in seconds for online coding competitions with features like custom template configuration, backup language support, auto input output files generation, etc. But, currently available for Codechef only.
</p>

<p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Made with :heavy_heart_exclamation: using Python3.

[![PyPI version](https://badge.fury.io/py/startcp-cli.svg)](https://badge.fury.io/py/startcp-cli) ![PyPI - Downloads](https://img.shields.io/pypi/dm/startcp-cli)

</p>


#### Dependencies
- `startcp-cli` runs on Python3.x
- [`pip3`](https://pip.pypa.io/en/stable/installing/)
- [`requests`](https://requests.readthedocs.io/en/master/user/install/)
- [`argparse`](https://pypi.org/project/argparse/)
and our beloved
- [`colorama`](https://pypi.org/project/colorama/)
- Thanks to all :pray:


#### Installation (Not for development)
- <strong>Note: Please update globally installed package frequently. :innocent:	</strong>
- Installing from `pypi`
    - `pip install startcp-cli` (use pip for Python3)
    - Already installed ?
        - Update using `pip install -U startcp-cli`
        - see [How To Update Pip Package](https://stackoverflow.com/questions/4536103/how-can-i-upgrade-specific-packages-using-pip-and-a-requirements-file)
- Installing Manually :
    - `git clone https://github.com/asprazz/startcp-cli.git`
    - `cd startcp-cli`
        - Option 1:
            - (if windows) `pip install .`
            - (if linux/mac) `sudo pip install . -H`
        - Option 2:
            - (optional for linux users) if requires `chmod +x install.sh`
            - then run `scripts/./install.sh`


#### Usage
- After installing using pip or building from source, by using `startcp` on terminal you can trigger the execution for startcp-cli from anywhere.
- Please enter URL of the competition to parse and generate the battlespace.
- Battle space will auto generated in ${USER_HOME}/startcp/ (default path which is configurable see Configuration)
- Battlespace incldes,
    - a problem.html file with problem direct link
    - in.txt containing all input cases
    - sol.py | sol.cpp either blank coding file or prepared from custom template


#### Configuration
- `startcp -g` or `startcp --generate` will generate configuration file in ${USER_HOME}/startcp/
- By setting, `IS_SETUP_DONE = 1` in configuration file custom configuration can be used over default ones



#### Contributing Guidelines
- Thank you for Showing interest in contributing to this project
- Please see https://github.com/asprazz/startcp-cli/blob/master/CONTRIBUTORS.md

##### Development
- Please, follow the contributing guidelines
- Fork the repository and clone it to your local environment
- Activate environment if any (
    [`venv`](https://docs.python.org/3/library/venv.html)
    or [`conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
    for more details
  )
- Running `startcp`
  - Running locally
      - `cd startcp-cli`
      - `python startcp/__main__.py`
  - Installing globally from your local repository
      - `cd startcp-cli`
          - Option 1:
              - (if windows) `pip install .`
              - (if linux/mac) `sudo pip install . -H`
          - Option 2:
              - (optional for linux users) if requires `chmod +x install.sh`
              - then run `scripts/./install.sh`
          - option 3:
              - `python setup.py install`
- Fix :wrench: something broken or Build :hammer: something interesting
- Don't forget to create child branch from `develop` and that branch only



#### Error reports
- First of all thank you.
- https://github.com/asprazz/startcp-cli/issues

