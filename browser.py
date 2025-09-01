from selenium import webdriver  # pip install selenium

from selenium.common.exceptions import *
from requests.exceptions import ConnectionError

from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from time import sleep
from traceback import format_exc
import logging

from settings import *

class Browser:

    def quitBrowser(self):
        try: # Tries to quit in case the browser is still open
            driver.quit()
        except: # If it's already closed, it does nothing
            pass

    def syncBrowser(self):
        global driver
        global BrowserOptions
        global BrowserService
        global wait
        global ignore

        self.quitBrowser()

        try:
            # Configures the Browser
            BrowserOptions = Options() # Add preferences on how to open the browser
            BrowserOptions.add_argument('--start-maximized') # Opens maximized
            BrowserOptions.add_argument('--no-first-run') # Opens faster
            BrowserOptions.add_experimental_option('detach', True) # Doesn't quit even after the function end
            BrowserOptions.add_argument('--guest') # Opens in guest mode, without looking for profiles
            #BrowserOptions.add_argument(r'--user-data-dir=C:\Users\"USERNAME"\AppData\Local\Microsoft\Edge\User Data') # Opens with user profile
            BrowserService = Service()

            # Constructs the Browser
            driver = webdriver.Edge(options=BrowserOptions, service=BrowserService)
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

    def writeMessage(self, message, speed):
        text_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, MAIN_TEXT_INPUT)))

        lenght_msg = len(message.split("\n"))
        count_lin = 1

        for line_of_text in message.split("\n"):
            text_field.send_keys(line_of_text)

            if count_lin < lenght_msg:
                text_field.send_keys(Keys.SHIFT + Keys.ENTER)

            count_lin += 1

        text_field.click()
        
        sleep(speed)

    def attachPhoto(self, path):
        wait.until(
            EC.any_of(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ATTACH_PLUS_BUTTON[0])),
                EC.element_to_be_clickable((By.CSS_SELECTOR, ATTACH_PLUS_BUTTON[1]))
            )
        ).click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, IMG_VID_BUTTON))).send_keys(path)

    def sendIt(self, element):
        wait.until(
            EC.any_of(
                EC.element_to_be_clickable((By.CSS_SELECTOR, element[0])),
                EC.element_to_be_clickable((By.CSS_SELECTOR, element[1]))
            )
        ).click()

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
                        wait.until(
                            EC.any_of(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, SEARCH_BAR_CLEAN_BUTTON[0])),
                                EC.element_to_be_clickable((By.CSS_SELECTOR, SEARCH_BAR_CLEAN_BUTTON[1]))
                            )
                        ).click()
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

                        try:
                            footer = int(wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'footer'))).get_attribute('childElementCount'))

                        except TimeoutException: # Retries if contact was not opened
                            logging.warning('\n\nTimeOutFooter - Retrying...\n\n')
                            search_bar.send_keys(Keys.ENTER)
                            footer = int(wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'footer'))).get_attribute('childElementCount'))
                        
                        if footer == 1: # When a contact is blocked, all the child elements of the footer tag will be reduced to one 
                            self.resetScreen(speed)
                            contact[3].value = '✘'
                            break # Doesn't send if the contact is currently blocked

                        match mode:

                            case 0: # Only message
                                self.writeMessage(message, speed)
                                self.sendIt(MAIN_SEND_BUTTON)

                            case 1: # Only image
                                self.attachPhoto(path)
                                self.sendIt(FILE_SEND_BUTTON)

                            case 2: # Message and Image
                                self.writeMessage(message, speed)
                                self.attachPhoto(path)
                                self.sendIt(FILE_SEND_BUTTON)

                        wait.until( # Check if both the send buttons are gone
                            EC.all_of(
                                EC.any_of(
                                    EC.invisibility_of_element((By.CSS_SELECTOR, FILE_SEND_BUTTON[0])),
                                    EC.invisibility_of_element((By.CSS_SELECTOR, FILE_SEND_BUTTON[1]))
                                ),
                                EC.any_of(
                                    EC.invisibility_of_element((By.CSS_SELECTOR, MAIN_SEND_BUTTON[0])),
                                    EC.invisibility_of_element((By.CSS_SELECTOR, MAIN_SEND_BUTTON[1]))
                                ),
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