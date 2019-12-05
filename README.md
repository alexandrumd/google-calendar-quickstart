# Info
This is a Google Calendar API quickstart in python for querying upcoming 10 events and free/ busy information.

Used as a PoC to showcase that this basic type of information is accessible only via the `https://www.googleapis.com/auth/calendar.readonly` Google Calendar scope (more info [here](https://developers.google.com/calendar/auth)). Ideally apps integrating with Google Calendar would only need this `scope` to help organizing meetings across different orgs.
Base code is from https://developers.google.com/calendar/quickstart/python.

# Prerequisites
Besides python3 you need a Google Account with Google Calendar API enabled (check https://console.developers.google.com/apis/library) - the script will request the needed permission at runtime - and a file named `credentials.json` containing the oAuth API credentials [downloaded from Google](https://console.developers.google.com/apis/credentials) placed in the same folder.

# How to use it
* As always, upgrade your pip - `pip3 install --upgrade pip; pip install --upgrade pip`
* Create virtual environment - `python3 -m venv venv3`
* Activate virtual environment - `source venv3/bin/activate`
* Install Python requirements - `pip3 install -r requirements.txt`
* Run it - `python3 quickstart.py`
  * you can supply min/max time ranges using the `-min` & `-max` args to get free/ busy info in the form `YYYY-MM-DDTHH:mm:ss+00:00` where the last part represents UTC zone. 
  For example `python3 quickstart.py -min=2019-12-05T00:00:00+02:00 -max=2019-12-05T23:59:00+02:00` to get free/ busy info for that specific interval. If args are not supplied it will default to the hardcoded ones.
  * display help info - `python3 quickstart.py -h`