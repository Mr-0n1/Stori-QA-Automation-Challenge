# Stori-QA-Automation-Challenge

###### Python Libraries to install.

Install via `pip`
```
pip install selenium
pip install html-testRunner
pip install argparse
```

###### Script Usage.

Run script with the command.
```
python ./test.py
```
The script will start an user input to ask the browser to begin the tests.
Browsers available are `firefox`, `chrome`, `opera`.

Due to the `unittest` library, the suite code architecture didn't allow the use of `argparse` nor `sys` for receiving execution arguments.

Once running, the script will execute the test cases in the selected browser and when it finish, it will create an HTML report in a script-generated folder called "Reports".
