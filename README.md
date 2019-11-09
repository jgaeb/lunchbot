LunchBot
========
`LunchBot` makes ordering lunch easy and fair(-ish).

# Installation

To install `LunchBot` (on Linux) run the following commands in the `lunchbot`
directory:
```bash
sudo apt-get geckodriver
sudo apt-get firefox
pip3 install -r requirements.txt
```

`LunchBot` expects the following variables to be available in the environment
where it is run:
```bash
GOOGLE_API_KEY
SLACK_TOKEN
DOORDASH_USERNAME
DOORDASH_PASSWORD
```

# Running

To run `LunchBot`, simply run
```bash
python3 -m PATH/TO/LUNCHBOT
```
in a crontab.
