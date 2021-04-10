# Retimer
A simple command line timer for MacOS using the Reminders app.

![Example image](example.png?raw=true "Example")

It uses applescript to create a reminder in the Reminders app. This way you get easily notified across all your Apple devices without installing third party apps and without running extra background processes.

Features include:

- notification after countdown (e.g. in 2 days, 5 hours and 2 minutes)
- notification at specific times (e.g. 10:30)
- notifications for periodic events (e.g. 5 times every 20 minutes)
- notifications for Promodoro timers (e.g. 5 times very 20 minutes with 5 minute breaks between blocks)

## Requirements

Python 3.6+ and Pip
```
brew install python
```
argparse
```
pip install argparse
```

## Usage

For convenience, the script can be made executable and moved in a PATH location, for example:
````
chmod +x timer.py
mv timer.py /usr/local/bin/t
````
Alternatively, you could set an alias in ~/.bash_profile or softlink to the location of the script.

Using the above, the timer can be invoked from anywhere by opening a terminal and simply typing
````
t --help
````

## Example commands

All commands below can be called with the --name flag to set an event name. 

### notify today at a specific time
````
t @17:20
````
### notify today at a specific time with event name
````
t @8:20 --name Breakfast
````
### notify in 20 minutes
````
t 20m
````
### notify in 5 hours
````
t 5h
````
### notify in 2 days, 3 hours and 5 minutes
````
t 2d3h5m
````
### notify 3 times every 30 minutes
````
t 3x30m
````
### notify 5 times every 180 minutes with a 70 minute break
All times are converted to minutes, so it doesn't matter if you input 1h10m or 70m.
````
t 5x180m+1h10m
````
### multiple timers
If multiple timers are created at once, all timers get the same name. A name with a space can be put in quotes.
````
t 5m 1d 2h10m @17:20 --name "go running"
````


## Disclaimer
Don't use this on a computer where you don't trust all users, the script uses eval which can be abused to execute arbitrary code. 
The reminders are all put in a list called "Timer", so make sure this doesn't interfere with an existing list. 


If you experience a problem, feel free to create an issue or PR.
