# py-stability-iot
## What is this?
This Python utility is made for Linux IoT devices which require hard system reset (power set to very low level, or cut off) upon reaching some undesired state.

A simple way to achieve this is to generate a file on the filesystem, which is then detected by some application, which in turn triggers hard system reset using specific hardware (RTC, watchdog).
This script implements checking of an indicator file and the subsequent system reset using either an RTC clock with 'off' functionality, or a Watchdog device.

## Requirements
To use this script, you need the following on your host system:
- Python (Python 3 or at least Python 2.7)
- Hardware that supports hard system reset with power cut off (or set to very low level): RTC, Watchdog
- rtcwake utility
- Some kind of job scheduler, for example cron.

## Usage
To use these scripts, you need to place the correct version with config.ini (default supplied in the repository) in some folder and run it in background, like so:
```
python3 stability.py &
```
or
```
python stability-python2.py &
```

It's best used with a scheduler of your choice as a job that runs on system boot, or, if run with single_run = true, as a reocurring job.

Regarding versions:
- stability.py is for Python 3.
- stability-python2.py is for Python 2 (at least Python 2.7).

By default, the script runs in background mode - it will continuously check for the presence of /tmp/() (configurable) and execute system reset via watchdog device if found.

## Configuration Options

The following is the default configuration:
```
[general]
recovery_device = watchdog
checking_interval = 5
indicator_file_path = /tmp/pywatchdog-fault-indicator
single_run = false

[watchdog-device]
wdt_path = /dev/watchdog
wdt_kill_delay = 300

[rtc-device]
rtc_path = /dev/rtc
rtc_mode = off
```

Detailed explanation of each option per section below:

### [general]
#### recovery_device
This determines what device will the script use to try resetting the system.

#### checking_interval
How often should the check for the indicator file be ran?

#### single_run
Should the program execute only once, or keep checking for the indicator file in background? Default: Run in background.

### [watchdog-device]
#### wdt_path
Path to the watchdog device.

#### wdt_kill_delay
To reboot the system, for how long should we capture the WDT file until the watchdog will give up and restart the system? (seconds)

### [rtc-device]
#### rtc_path
Path to the RTC device.
#### rtc_mode
What mode should the RTC be requested to operate in? Different RTC devices support different modes, usually for best power cycling the 'off' mode is provided, but sometimes it's unavailable. In such cases, 'mem' should be a suitable alternative.

## Why not just use a shell script with cron that calls 'rtcwake ...' or equivalent on fault condition?

While you certainly can do so in most cases, there are situations when this becomes difficult.
For example, you can't directly supply a Docker container with access to RTC clock and/or Watchdog devices, and the ability to trigger them, without granting significant privileges to the container.

In such cases, you would need an external monitoring mechanism via some channel - for example, an indicator file on a mounted named volume. 
This script implements such a monitoring mechanism.

