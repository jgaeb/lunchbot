LunchBot
========
<img src="LunchBot.jpg" alt="LunchBot icon" style="width: 500px;">

`LunchBot` makes ordering lunch easy and fair(-ish).

# Installation

To install `LunchBot` (on Mac) run the following commands in the `lunchbot`
directory:
```bash
brew install geckodriver
brew install firefox
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
