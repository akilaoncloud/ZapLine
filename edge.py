from selenium import webdriver  # pip install selenium

from selenium.common.exceptions import *
from requests.exceptions import ConnectionError

from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from time import sleep
from traceback import format_exc
import logging

from settings import *

class Edge:

    def quitBrowser(self):
        try: # Tries to quit in case the browser is still open
            driver.quit()
        except: # If it's already closed, it does nothing
            pass

    def syncBrowser(self):
        global driver
        global EdgeOptions
        global EdgeService
        global wait
        global ignore

        self.quitBrowser()

        try:
            # Configures the Browser
            EdgeOptions = Options() # Add preferences on how to open the browser
            EdgeOptions.add_argument('--start-maximized') # Opens maximized
            EdgeOptions.add_argument('--no-first-run') # Opens faster
            EdgeOptions.add_experimental_option('detach', True) # Doesn't quit even after the function end
            EdgeOptions.add_argument('--guest') # Opens in guest mode, without looking for profiles
            #EdgeOptions.add_argument(r'--user-data-dir=C:\Users\"USERNAME"\AppData\Local\Microsoft\Edge\User Data') # Opens with user profile
            EdgeService = Service(EdgeChromiumDriverManager().install())

            # Constructs the Browser
            driver = webdriver.Edge(options=EdgeOptions, service=EdgeService)
            driver.get('https://web.whatsapp.com/')

            ignore = (NoSuchElementException, StaleElementReferenceException) # Ignores old or non existent elements
            wait = WebDriverWait(driver, WAIT_TIME, ignored_exceptions=ignore) # Tolerates x seconds

            # SYNC_TIME minutes to sync your WhatsApp
            WebDriverWait(driver, SYNC_TIME).until(EC.element_to_be_clickable((By.CSS_SELECTOR, NEW_CHAT)))

        except ConnectionError: # Internet error
        
            result = CONNECTION_ERROR
            logging.error(format_exc())
            
            try: # Tries to quit in case the browser is still open
                driver.quit()
            except: # If it's already closed, it does nothing
                pass

        except Exception as e: # In case of any other error
            
            result = SYNC_ERROR
            logging.error(format_exc())
            
            try: # Tries to quit in case the browser is still open
                driver.quit()
            except: # If it's already closed, it does nothing
                pass

        else:
            # Synchronized
            result = STATUS_SYNCED
            
        return result

    def resetScreen(self, speed):
        sleep(speed/2)
        for rpt in range(4): # Resets WhatsApp's screen to the default page
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        sleep(speed/2)

    def writeMessage(self, element, message, speed):
        text_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, element)))

        lenght_msg = len(message.split("\n"))
        count_lin = 1

        for line_of_text in message.split("\n"):
            text_field.send_keys(line_of_text)

            if count_lin < lenght_msg:
                text_field.send_keys(Keys.SHIFT + Keys.ENTER)

            count_lin += 1

        text_field.click()
        
        sleep(speed); return text_field

    def attachPhoto(self, path):
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ATTACH_PLUS_BUTTON))).click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, IMG_VID_BUTTON))).send_keys(path)

    def sendContact(self, last_search, contact, mode, message, path, speed): 
        # It can retry on finding a contact
        contact_search_retries = 1 

        try:        
            contact_number = str(contact[2].value)

            # Verifies if last searched contact was found
            if last_search != 'Not Found':
                #If it was, it opens the search bar again.
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, NEW_CHAT))).click()

            # Inserts contact number in the search bar
            search_bar = driver.switch_to.active_element
            search_bar.send_keys(str(contact_number))

            sleep(speed)

            # Looks for a valid contact number
            while True: 

                # Searching...
                try: 
                    search = wait.until(
                        EC.any_of(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, OFFLINE_SUBTITLE)),
                            EC.visibility_of_element_located((By.CSS_SELECTOR, RESULTS_SUBTITLE)),
                            EC.visibility_of_element_located((By.CSS_SELECTOR, CHAT_LIST))
                        )
                    ).text

                except StaleElementReferenceException:
                    logging.warning('\n\nStaleElement - Retrying...\n\n')
                    sleep(1)

                else:
                    logging.info(search)

                    if contact_number in search: # No results found for 'contact_number'
                        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, SEARCH_BAR_CLEAN_BUTTON))).click()
                        contact[3].value = '✘'
                        search = 'Not Found'
                        break

                    elif (contact_search_retries == 20) or ('internet' in search): # Slow |OR| no connection.
                        return CONNECTION_ERROR
                        
                    elif '...' in search: # Looking for... 
                        sleep(1) # It's still looking if the contact exists or not
                        contact_search_retries+=1

                    # Found it
                    else:
                        search_bar.send_keys(Keys.ENTER)

                        footer = int(wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'footer'))).get_attribute('childElementCount'))
                        
                        if footer == 1: # When a contact is blocked, all the child elements of the footer tag will be reduced to one 
                            self.resetScreen(speed)
                            contact[3].value = '✘'
                            break # Doesn't send if the contact is currently blocked

                        match mode:

                            case 0: # Only message
                                msg = self.writeMessage(MAIN_TEXT_INPUT, message, speed)
                                msg.send_keys(Keys.ENTER)

                            case 1: # Only image
                                self.attachPhoto(path)
                                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, FILE_SEND_BUTTON))).click()

                            case 2: # Message and Image
                                self.writeMessage(MAIN_TEXT_INPUT, message, speed)

                                self.attachPhoto(path)
                                
                                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, FILE_SEND_BUTTON))).click()
                                #wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, FILE_TEXT_INPUT))).send_keys(Keys.ENTER)

                        wait.until( # Check if both the send buttons are gone
                            EC.all_of(
                                EC.invisibility_of_element((By.CSS_SELECTOR, FILE_SEND_BUTTON)),
                                EC.invisibility_of_element((By.CSS_SELECTOR, MAIN_SEND_BUTTON)),
                                EC.element_to_be_clickable((By.CSS_SELECTOR, MAIN_TEXT_INPUT))
                            )
                        )                
                        # [ESC] is pressed, returning to the default screen                    
                        self.resetScreen(speed)
                        contact[3].value = '✔'
                        break

        except Exception:
            # In case of error
            result = DEFAULT_ERROR
            logging.error(format_exc())

        else:
            # Search complete
            result = search

        return result