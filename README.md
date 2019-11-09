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

# Running

`LunchBot` expects the following environmental variables to be available when it
is run:
```bash
GOOGLE_API_KEY
SLACK_TOKEN
SLACK_CHANNEL
DOORDASH_USERNAME
DOORDASH_PASSWORD
```

To run `LunchBot`, simply run
```bash
python3 -m PATH/TO/LUNCHBOT
```
in a crontab.
