from configparser import ConfigParser
import os
import time

"""
    Filesystem and RTC modes of operation support single-run execution (no running in background).
    Watchdog mode of operation does not support single-run execution, because it has to hold the RTC device open.
"""

def trigger_rtc(rtc_path: str, rtc_mode: str):
    return os.system('rtcwake --device ' + rtc_path + ' -s 60 -m ' + rtc_mode)

def trigger_wdt(indicator_file: str, wdt_path: str, wdt_kill_delay: int):
    """
        This function opens the WDT file and holds it for 5 minutes.
        Most WDT's will trigger system reboot if not kicked for about a minute, but it's vendor-specific, so 
        might warrant a config option.
    """
    with open(wdt_path, 'w') as wdt_file:
        os.remove(indicator_file)
        time.sleep(wdt_kill_delay)
    return True

def handle_rtc_reboot(config: ConfigParser, indicator_file: str):
    print("Triggering RTC...")
    rtc_path = config.get('rtc-device', 'rtc_path')
    rtc_mode = config.get('rtc-device', 'rtc_mode')
    if trigger_rtc(rtc_path, rtc_mode):
        print("Failed to execute RTC sleep!")
        exit(1)
    else:
        os.remove(indicator_file)

def handle_wdt_reboot(config: ConfigParser, indicator_file: str):
            print("Triggering watchdog...")
            wdt_path = config.get('watchdog-device', 'wdt_path')
            wdt_kill_delay = int(config.get('watchdog-device', 'wdt_kill_delay'))
            if trigger_wdt(indicator_file, wdt_path, wdt_kill_delay):
                print("Failed to force WDT reboot!")
                exit(1)

def monitor_system(config: ConfigParser):
    indicator_file = config.get('general','indicator_file_path').rstrip()
    if os.path.exists(indicator_file):
        if config.get('general', 'recovery_device') == 'rtc':
            handle_rtc_reboot(config, indicator_file)
        elif config.get('general', 'recovery_device') == 'watchdog':
            handle_wdt_reboot(config, indicator_file) 

def monitor_system_continuous_wdt(config: ConfigParser):
    indicator_file = config.get('general','indicator_file_path').rstrip()
    checking_interval = int(config.get('general','checking_interval'))
    while(True):
        if os.path.exists(indicator_file):
            handle_wdt_reboot(config, indicator_file)
        time.sleep(checking_interval)
    
def monitor_system_continuous_rtc(config: ConfigParser):
    indicator_file = config.get('general','indicator_file_path').rstrip()
    checking_interval = int(config.get('general','checking_interval'))
    while(True):
        if os.path.exists(indicator_file):
            handle_rtc_reboot(config, indicator_file)
        time.sleep(checking_interval)



if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini')

    if config.get('general', "recovery_device") == 'rtc':
        print("Warning: this utility requires rtcwake to be installed when used in RTC mode.")

    if bool(config.get('general', "single_run")):
        monitor_system(config)
    else:
        if config.get('general', "recovery_device") == 'watchdog':
            monitor_system_continuous_wdt(config)
        elif config.get('general', "recovery_device") == 'rtc':
            monitor_system_continuous_rtc(config)
