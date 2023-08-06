import logging
import random
import time
import traceback
from configparser import ConfigParser
from typing import Callable

import win32api
import win32con
from tqdm import tqdm

from spaceinator import __version__ as version

log = logging.getLogger()


def display_title() -> None:
    print(
        fr"""
   _____                       _             __            
  / ___/____  ____ _________  (_)___  ____ _/ /_____  _____
  \__ \/ __ \/ __ `/ ___/ _ \/ / __ \/ __ `/ __/ __ \/ ___/
 ___/ / /_/ / /_/ / /__/  __/ / / / / /_/ / /_/ /_/ / /    
/____/ .___/\__,_/\___/\___/_/_/ /_/\__,_/\__/\____/_/     
    /_/
    
Banner by https://manytools.org/hacker-tools/ascii-banner/
version {version}
"""
    )


def press_spacebar(times_pressed: int) -> int:
    log.info("Pressing space bar.")

    # Randomize the press duration to match a human keystroke.
    random_key_press_duration = random.uniform(0.06, 0.20)

    # Key Down
    start = time.perf_counter()
    win32api.keybd_event(0x20, 0, 0, 0)  # 0x20 is the space bar key

    # Key Up
    time.sleep(random_key_press_duration)
    win32api.keybd_event(0x20, 0, win32con.KEYEVENTF_KEYUP, 0)

    print(f"Spacebar pressed at {time.strftime('%I:%M:%S %p')} for {time.perf_counter() - start:0.3f} seconds. ",
          end='')
    log.debug("Space bar pressed successfully.")
    times_pressed += 1

    return times_pressed


def instructions() -> None:
    newlines_before = 2
    newlines_after = 2

    print("\n" * newlines_before)
    print(
        "Spaceinator will press the space bar once at a random point in time within the given range."
    )
    print("\n" * newlines_after)


def validate_positive_int_or_empty_str(inp) -> bool:
    if inp == "":
        log.debug("User bypassed min minute prompt. Using previously stored value.")
        return True

    try:
        inp = int(inp)
    except ValueError:
        print("Input must be a positive non-zero integer.")
        log.error("Input must be a positive non-zero integer.")
        return False

    if not inp > 0:
        print("Input must be a positive non-zero integer.")
        log.error("Input must be a positive non-zero integer.")
        return False

    return True


def get_max_value(config: ConfigParser) -> None:
    min_minute = config.getint("main", "min_minute")
    while True:
        user_response = get_user_input(
            default_value=config.getint("main", "max_minute"),
            input_type="maximum",
            is_valid=validate_positive_int_or_empty_str,
        )

        is_valid = validate_max_value(user_response, min_minute, config)
        if is_valid:
            break


def validate_max_value(
        user_response: str, min_minute: int, config: ConfigParser
) -> bool:
    if user_response:
        if int(user_response) <= min_minute:
            log.error(f"Input must be greater than minimum input ({min_minute}).")
            return False

        else:
            config.set("main", "max_minute", user_response)
            config.save()
            return True
    else:
        return True


def get_min_value(config: ConfigParser) -> None:
    user_response = get_user_input(
        default_value=config.getint("main", "min_minute"),
        input_type="minimum",
        is_valid=validate_positive_int_or_empty_str,
    )
    if user_response:
        config.set("main", "min_minute", user_response)
        config.save()


def run(config: ConfigParser) -> None:
    """
    pyautogui presses the space key once randomly within the time range
    given within the config file. Updates the "times_pressed" attribute.
    """

    times_pressed = config.getint("main", "times_pressed")

    min_minute = config.getint("main", "min_minute")
    max_minute = config.getint("main", "max_minute")

    print("Starting in 5 seconds. Press ctrl+C to quit.")
    time.sleep(5)
    start = time.perf_counter()

    while True:
        try:
            times_pressed = press_spacebar(times_pressed)
            config.set("main", "times_pressed", str(times_pressed))
            config.save()

            sleep_minutes = random.randrange(start=min_minute, stop=max_minute)
            sleep_seconds = random.randrange(start=1, stop=59)
            sleep_duration = (sleep_minutes * 60) + sleep_seconds

            log.debug(
                f"Sleep duration {time.strftime('%H:%M:%S', time.gmtime(sleep_duration))}"
            )
            print(f"Next press in {sleep_minutes} minutes and {sleep_seconds} seconds.")

            for i in tqdm(range(sleep_duration),
                          ncols=80,
                          leave=False,
                          bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'
                          ):
                if i == sleep_duration:
                    continue  # Press space on the last iteration instead of pausing for an additional second.
                time.sleep(1)

        except KeyboardInterrupt:
            log.debug("User KeyboardInterrupt")
            print("Shutting down...")
            time.sleep(2)
            raise SystemExit

        except Exception:
            log.error(f"Unhandled exception: {traceback.print_exc()}")

        finally:
            run_duration = time.perf_counter() - start
            log.info(f"Spacebar pressed {times_pressed} times in {run_duration}")
            config.save()


def get_user_input(
        default_value: int, input_type: str, is_valid: Callable[[str], bool]
) -> str:
    while True:
        response = input(
            f"Please enter the {input_type} minute range. ({default_value}): "
        )
        if is_valid(response):
            return response
