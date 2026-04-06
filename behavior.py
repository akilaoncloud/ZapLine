from time import sleep
import random
from selenium.webdriver.common.keys import Keys

def humanType(element, text, speed):

    sleep(random.uniform((speed*0.20),(speed*0.40)))

    for char in text:

        # Random typing error
        if random.random() < 0.005: # 0.5% chance of error
            wrong = random.choice("abcdefghijklmnopqrstuvwxyz1234567890")
            element.send_keys(wrong)
            sleep(random.uniform((speed*0.30),(speed*0.50)))
            element.send_keys(Keys.BACKSPACE)

        element.send_keys(char)

        if char in " ":
            sleep(random.uniform((speed*0.10),(speed*0.15)))

        elif char in ",;({[-*":
            sleep(random.uniform((speed*0.15),(speed*0.30)))

        elif char in ".!?":
            sleep(random.uniform((speed*0.30),(speed*0.50)))

        else:
            sleep(random.uniform((speed*0.03),(speed*0.08)))

    sleep(random.uniform((speed*0.20),(speed*0.40)))

def humanWait(speed):
    sleep(random.uniform((speed*0.80),(speed*1.20)))
