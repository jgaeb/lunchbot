from urllib.parse import urlparse
from datetime import date
from time import sleep

from selenium.webdriver import Firefox
from selenium.common.exceptions import NoSuchElementException
import requests

class DoorDashOrder(Firefox):
    def __init__(self):
        super().__init__()
        self.logged_in = False
        self.order_url = None
        # NOTE: Wait up to one minute for DOM elements to load.
        self.implicitly_wait(60)

    def login(self, username: str, password: str) -> None:
        try:
            self.get("https://www.doordash.com/accounts/login")
            self.find_element_by_xpath("//input[@id='email']").send_keys(username)
            self.find_element_by_xpath("//input[@id='id_password']").send_keys(password)
            self.find_element_by_xpath("//button[@type='submit']").click()
            # TODO(jgaeb): Change to 60s for production.
            sleep(10)
            if self.current_url == "https://www.doordash.com/":
                self.logged_in = True
            else:
                raise LoginError
        except NoSuchElementException as e:
            raise LoginError(f"{e!r}")

    def group_order(self, restaurant_url: str) -> None:
        if self.logged_in:
            url = urlparse(restaurant_url)
            if (url.netloc != 'www.doordash.com' or
                    not url.path.startswith("/store/") or
                    not requests.get(restaurant_url).ok):
                raise NavigationError(restaurant_url)
            self.get(restaurant_url)
            try:
                self.find_element_by_xpath(
                        "//button[@data-anchor-id='CreateGroupCartModalButton']"
                ).click()
                self.find_element_by_xpath(
                        "//button//span[div='$15']"
                ).click()
                submit_button = self.find_element_by_xpath(
                        "//button[@data-anchor-id='CreateGroupCartButton']"
                ).click()
                return self.find_element_by_xpath(
                        "//input[@data-anchor-id='GroupCartLinkTextField']"
                ).get_attribute("value"), self.title.split(" Delivery")[0]
            except:
                raise GroupOrderFailedError(f"{e!r}")
        else:
            raise NotLoggedInError

################################## EXCEPTIONS ##################################

class LoginError(Exception):
    pass

class NavigationError(Exception):
    pass

class NotLoggedInError(Exception):
    pass

class GroupOrderFailedError(Exception):
    pass
