# Tests
## Test Environment
Two separate virtual environments can be configured for testing purposes. One option is to use a virtual environment with the SDK installed as a package, i.e. from TestPyPi. Note, the latest SDK version on TestPyPi may be out of date with active development code, as new versions are only published on merge to `staging`. Attempting to use an outdated SDK version with new test code will result in errors. Therefore, this approach is recommended for infrequent hardware calibration tests, or when you know the SDK version to be installed is up to date with your test code. For active development, it is instead recommended to use a virtual environment that does not install the SDK as a package, but uses local source code instead.
## Run Hardware Tests
### Virtual Environment with SDK Installed as a Package
From the project root directory run the following:
1. Create virtual env:
```
$ python3 -m venv venv_integration
```
2. Activate virtual env:
```
$ source venv_integration/bin/activate
```
3. Install dependencies:
```
$ python3 -m pip install -r requirements_integration.txt
```
4. Run tests:
```
$ python3 -m pytest ./tests/<test_path>
```
### Virtual Environment using local SDK
From project root directory run the following:
1. Create virtual env:
```
$ python3 -m venv venv_test
```
2. Activate virtual env:
```
$ source venv_test/bin/activate
```
3. Install dependencies:
```
$ python3 -m pip install -r requirements_test.txt
```
4. Change directory:
```
$ cd ./src
```
5. Run tests:
```
$ python3 -m pytest ../tests/<test_path>
```
### Generate Test Report
If you wish to generate an HTML test report, choose a virtual environment from above, and replace the "Run tests" step with either of the following commands:
* SDK as a package:
```
$ python3 -m pytest ./tests/<test_path> --html=<path-to-report> --log-level=INFO
```
* Local SDK:
```
$ python3 -m pytest ../tests/<test_path> --html=<path-to-report> --log-level=INFO
```
The `<test_path>` can be left blank to run all integration and hardware tests, or set to a filepath to run a specific test module under `tests/`. A folder containing the HTML test report will be added at `<path-to-report>`. An example path is: `./tests/reports/report.html`. Include the `--log-level=INFO` tag to add logs with helpful test details in report (recommended).

To view the HTML report:
1. Change directory to report folder:
```
$ cd <path-to-report>
```
2. Start a simple python webserver on edgepi:
```
$ python3 -m http.server
```
3. In a browser-enabled machine, navigate to `http://<edgepi-address>:8000/`
4. The HTML test report folder should be visible.

### Configure Self-hosted GitHub Actions Test Runner
The integration tests can be run as part of GitHub Actions workflows, but this requires setting up an EdgePi unit as a self-hosted test runner.
To do so, follow the steps below (working as of Dec 2022):
1. Visit https://github.com/EdgePi-Cloud/edgepi-python-sdk/settings/actions/runners/
2. Select `New self-hosted runner`
3. Choose OS and architecture -> `Linux` -> `ARM64`
4. Follow all steps under `Download`
5. Run `$ ./config.sh --url https://github.com/EdgePi-Cloud/edgepi-python-sdk --token <token>`
    * `<token>` here denotes your personal GitHub access token
6. Run the actions runner [as a service](https://docs.github.com/en/actions/hosting-your-own-runners/configuring-the-self-hosted-runner-application-as-a-service):
```
$ sudo ./svc.sh install
$ sudo ./svc.sh start
```
