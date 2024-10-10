import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class TradeExecutor:
    def __init__(self, ASSET_PATH, DIRECTION, UNITS, REF, config):
        self.username = config["trader_credentials"]["username"]
        self.password = config["trader_credentials"]["password"]
        self.user = config["trader_credentials"]["user"]
        self.asset_path = ASSET_PATH
        self.direction = DIRECTION
        self.units = UNITS
        self.rationale = REF
        self.driver = webdriver.Chrome()

    def login(self):
        print("Starting Web Application...")
        self.driver.get('https://portfolio.traderion.com/auth/login')  # Replace with the actual URL
        self.driver.implicitly_wait(5)  # Wait for 5 seconds

        try: 
            username_box = self.driver.find_element(By.ID, 'normal_login_username')
            password_box = self.driver.find_element(By.ID, 'normal_login_password')

            print("Logging in...")
            username_box.send_keys(self.username)
            password_box.send_keys(self.password)

            login_button = self.driver.find_element(By.CSS_SELECTOR, "button.ant-btn.login-form-button.ant-btn-primary")
            login_button.click()

            radio = self.driver.find_element(By.XPATH, f"//label[span[text()='{self.user}']]/span/input")
            radio.click()

            ok_button = self.driver.find_element(By.XPATH, "//button[span[text()='Ok']]")
            ok_button.click()

            print("Joining relevant server...")
            join_button = self.driver.find_element(By.XPATH, "//tr[td[text()='Running']]//a[text()='Join']")
            join_button.click()

            time.sleep(20)  # Adjust as necessary

            # Switch to the latest window
            self.driver.switch_to.window(self.driver.window_handles[-1])
        except Exception as e:
            print(f"An error occurred while logging in: {e}")

    def select_investment(self):
        print("Selecting investment...")
        try:
            self.driver.find_element(By.XPATH, f"//div[contains(span/text(), '{self.asset_path.split('/')[0]}')]").click()

            if len(self.asset_path.split('/')) == 3: 
                tab = self.driver.find_element(By.XPATH, f"//div[@role='tab' and text()='{self.asset_path.split('/')[1]}']")
                tab.click()
                time.sleep(2)

            elif len(self.asset_path.split('/')) == 2: 
                trade_button = self.driver.find_element(By.XPATH, f"//div[@role='tab' and text()='{self.asset_path.split('/')[1]}']//following-sibling::div[contains(@class, 'ant-collapse-item')]//button[contains(text(), 'Trade')]")
                trade_button.click()
                time.sleep(2)

            ticker = self.asset_path.split('/')[2]
            trade_button_xpath = f'//tr[td[contains(text(), "{ticker}")]]//button[span[text()="Trade"]]'
            trade_button = self.driver.find_element(By.XPATH, trade_button_xpath)
            trade_button.click()
        except Exception as e:
            print(f"An error occurred while selecting asset: {e}")

    def enter_trade(self):
        print("Entering trade...")
        if self.direction == "Buy":
            radio_button_xpath = '//input[@value="0"]'  # XPath for Buy
        elif self.direction == "Sell":
            radio_button_xpath = '//input[@value="1"]'  # XPath for Sell
        else:
            radio_button_xpath = '//input[@value="2"]'  # XPath for Short Sell

        try:
            order_type_radio = self.driver.find_element(By.XPATH, radio_button_xpath)
            order_type_radio.click()
            print(f"{self.direction} radio button selected successfully!")

            quantity_input_xpath = '//div[@class="ant-input-number-input-wrap"]/input[@class="ant-input-number-input"]'
            quantity_input = self.driver.find_element(By.XPATH, quantity_input_xpath)

            quantity_input.click()
            quantity_input.send_keys(Keys.ARROW_LEFT)
            quantity_input.send_keys(Keys.DELETE)  # Clear existing value
            for _ in range(10):  
                quantity_input.send_keys(Keys.ARROW_LEFT)
                quantity_input.send_keys(Keys.DELETE)

            quantity_input.send_keys(self.units)  # Enter quantity
            print("Quantity set successfully!")

            rationale_textarea_xpath = '//textarea[@placeholder="Investment Rationale | required field min. 10 char."]'
            rationale_textarea = self.driver.find_element(By.XPATH, rationale_textarea_xpath)

            rationale_textarea.click()
            rationale_textarea.clear()  # Clear existing text
            rationale_textarea.send_keys(self.rationale)  # Enter the investment rationale
            print("Investment rationale entered successfully!")

        except Exception as e:
            print(f"An error occurred while entering trade details: {e}")

    def place_trade(self):
        print("Placing trade...")
        try: 
            place_order_button = self.driver.find_element(By.XPATH, "//button[span[text()='Place Order']]")
            place_order_button.click()
            print("Trade placed successfully!")
        except Exception as e:
            print(f"An error occurred while executing trade: {e}")

    def execute_trade(self):
        self.login()
        self.select_investment()
        self.enter_trade()
        self.place_trade()
        time.sleep(5)  # Wait for confirmation
        self.driver.quit()

# Example of how to use the TradeExecutor class:
if __name__ == "__main__":

    ASSET_PATH = "Equities/North America/NVDA US",
    DIRECTION = "Buy",
    UNITS = "1",
    REF = "Automated Trading - Strategy: TEST."

    # Load configuration from JSON file
    with open('config/config.json', 'r') as config_file:
        config = json.load(config_file)

    executor = TradeExecutor(ASSET_PATH, DIRECTION, UNITS, REF, config)
    executor.execute_trade()

