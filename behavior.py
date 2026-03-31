from time import sleep
import random
from selenium.webdriver.common.keys import Keys

def humanType(element, text, speed):

    sleep(random.uniform((speed*0.5),(speed*0.75)))

    for char in text:

        # Random typing error
        if random.random() < 0.05:
            wrong = random.choice("abcdefghijklmnopqrstuvwxyz1234567890")
            element.send_keys(wrong)
            sleep(random.uniform((speed*0.25),(speed*0.5)))
            element.send_keys(Keys.BACKSPACE)

        element.send_keys(char)

        if char in ",;":
            sleep(random.uniform((speed*0.25),(speed*0.5)))

        elif char in ".!?":
            sleep(random.uniform((speed*0.5),(speed*0.75)))

        else:
            sleep(random.uniform((speed*0.05),(speed*0.10)))

    sleep(random.uniform((speed*0.5),(speed*0.75)))

def humanWait(speed):
    sleep(random.uniform((speed*0.5),speed))
