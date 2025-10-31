import requests
import pytest

BASE_URL = "/orders"

def test_get_orders():
    response = requests.get(f"{BASE_URL}/orders")
    assert response.status_code == 200
    data = response.json()
    response_fields = ["symbol", "side", "quantity", "orderType"]
    for field in response_fields:
        assert field in data
        if field == "quantity":
            assert isinstance(data[field], int)
        else:
            assert isinstance(data[field], str)

def test_post_orders():
    body = {
              "symbol": "AAPL",
              "side": "buy",
              "quantity": 10,
              "orderType": "market"
            }
    response = requests.post(url=f"{BASE_URL}/orders", json=body)
    assert response.status_code == 201
    data = response.json()
    response_fields = ["orderId", "status", "symbol", "side", "quantity", "orderType", "timestamp"]
    # positive test
    for field in response_fields:
        assert field in data
        if field == "quantity":
            assert isinstance(data[field], int)
        else:
            assert isinstance(data[field], str)
        if field == "status":
            assert data[field] == "submitted"
    # negative test
    body_negative_symbol = {
              "symbol": "INVALID",
              "side": "buy",
              "quantity": 10,
              "orderType": "market"
            }
    response = requests.post(url=f"{BASE_URL}/orders", json=body_negative_symbol)
    assert response.status_code == 400

    body_negative_quantity = {
              "symbol": "INVALID",
              "side": "buy",
              "quantity": 0,
              "orderType": "market"
            }
    response = requests.post(url=f"{BASE_URL}/orders", json=body_negative_quantity)
    assert response.status_code == 400



'''
Suppose you are automating Robinhood’s login page with Playwright.


# driver class 

class BaseDriver:
    def __init__(self):
        self.playwright = playwright.start
        self.browser = self.playwrigyht.chromium.launch
        self.context
        self.page
    
    def quit(self):
    self.browser.close
    self.playwright.stop()
    
class LoginPageLocators:
    USERNAME_FIELD = "#username"
    PASSWORD_FIELD = "#password"
    LOGIN_BUTTON = "#login-btn"
    
class LoginPageActions:
    def __init__(self, page):
        self.page = page
        
    def enter_username(self, username) 
        self.page.fill(LoginPageLocators.USERNAME_FIELD, username)
    
    def enter_password(self, password)
    
    def click_login(self)
        self.page.click(LoginPageLocators.LOGIN_BUTTON)
    
class LoginPage:
    def __init__(self, driver):
        self.page = driver.page
        self.actions  = LoginPageActions(self.page)
        
    def login(self, username, password)
        self.actions.enter_username(username
        self.actions.enter_password(password
        self.actions.click_login()
        
def test_login():
    driver = BaseDriver()
    try:
        driver.page.goto()
        login_page = LoginPage(driver)
        login_page.login()
        
        assert "dashboard" in driver.page.url, "Login failed"

driver - initilizes playwright/appium
locators - stores the page's element locators
actions - contains user interactions
page object - locator + action
test - use page object

'''