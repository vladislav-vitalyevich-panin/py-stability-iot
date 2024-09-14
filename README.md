# py-stability-iot
# Note: The utility is not implemented yet - work is done on separate branches.
## What is this?
This Python utility is made for Linux IoT devices which require hard system reset (power set to very low level, or cut off) upon reaching some undesired state.

A simple way to achieve this is to generate a file on the filesystem, which is then detected by some application, which in turn triggers hard system reset using specific hardware (RTC, watchdog).
This script implements checking of an indicator file and the subsequent system reset using either an RTC clock with 'off' functionality, or a Watchdog device.

## Requirements
To use this script, you need the following on your host system:
- Python
- Hardware that supports hard system reset with power cut off (or set to very low level): RTC, Watchdog
- rtcwake utility

## Why not just use a shell script with cron that calls 'rtcwake ...' or equivalent on fault condition?

While you certainly can do so in most cases, there are situations when this becomes difficult.
For example, you can't directly supply a Docker container with access to RTC clock and/or Watchdog devices, and the ability to trigger them, without granting significant privileges to the container.

In such cases, you would need an external monitoring mechanism via some channel - for example, an indicator file on a mounted named volume. 
This script implements such a monitoring mechanism.

