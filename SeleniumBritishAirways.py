
Selenium Automation Script Documentation
========================================
Source Code is at the bottom of the page.
========================================
Introduction
------------

This documentation provides comprehensive information on how to use the Selenium automation script for interactive sessions with a website. The script is designed to perform actions on a web page and record them for testing or automation purposes.

Features
--------

*   Interactive sessions with a website.
*   Recording of actions and capturing screenshots.
*   Support for using proxies.
*   Option to run in headless mode.
*   Multi-threading for running multiple instances simultaneously.
*   Configuration with a list of usernames and passwords.

Prerequisites
-------------

Before using the script, make sure you have the following:

1.  **Python:** The script is written in Python, so you need to have Python installed on your system.
2.  **Selenium:** Install the Selenium library for Python using pip:
    
        pip install selenium
    
3.  **Undetected Chromedriver:** Install the "undetected\_chromedriver" library for Selenium to ensure that your automated sessions are undetectable:
    
        pip install undetected-chromedriver
    

Usage
-----

Follow the steps below to use the Selenium automation script:

1.  **Create a List of Proxies**

Define a list of proxy servers that you want to use for your sessions. You can customize the list according to your needs. Below is an example of how the proxies should look:

    proxies = ['proxy1', 'proxy2', 'proxy3']

4.  **Define Usernames and Passwords**

Create lists of usernames and passwords that correspond to the proxies. These will be used for logging in during the sessions. Here's an example:

    usernames = ['user1', 'user2', 'user3']

    passwords = ['pass1', 'pass2', 'pass3']

8.  **Create Test Instances**

To run sessions with different configurations, create instances of the TestBA class with various settings. Below are examples of how to create instances:

**To run with a random proxy and without headless mode:**

    import random

    # Select a random proxy from the list

    random_proxy = random.choice(proxies)

    # Create an instance with the selected proxy and no headless mode

    test_instance_random_proxy = TestBA(proxy=random_proxy, headless=False)

You can create instances with other combinations of proxy and headless settings as needed.

17.  **Start Sessions**

Use the created instances to start interactive sessions. These sessions will perform actions on a website, such as logging in, and record the actions for testing or automation purposes. Here's how to start a session:

    # Start the interactive session

    test_instance_random_proxy.interactive_session()

21.  **Customize as Needed**

You can further customize the script and add additional steps within the interactive session method to meet your specific requirements.

Recording Sessions
------------------

The script is designed to record actions and capture screenshots during the interactive sessions. The recorded actions are stored in the \`recorded\_actions\` attribute of the \`InteractiveSessionRecorder\` class. You can access and analyze these actions as needed for testing and automation purposes.

Here's an example of how to access recorded actions:

    # Access the recorded actions for a specific instance (e.g., test_instance_random_proxy)

    recorded_actions = test_instance_random_proxy.recorder.recorded_actions

Additionally, the script saves screenshots of each action in a folder named "screenshots" for reference. The folder structure may look like this:

    screenshots/
        ├── screenshot_1.png
        ├── screenshot_2.png
        ├── ...
        └── screenshot_n.png
        

You can analyze the screenshots to verify the recorded actions visually.

Conclusion
----------

The provided Selenium automation script allows you to perform interactive sessions with a website, record actions, and customize the use of proxies and headless mode. It's a flexible tool for automating web interactions and testing scenarios.

**Note:** Ensure compliance with website terms of service and legal regulations when using this script for web automation and scraping.

Code Explanation and Usage
--------------------------

Below is the Python code for the Selenium automation script with explanations and usage instructions:

    import os
        import threading
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from undetected_chromedriver import Chrome, ChromeOptions
        from selenium.common.exceptions import TimeoutException

**InteractiveSessionRecorder Class:**

The `InteractiveSessionRecorder` class is responsible for recording user interactions with the web page and capturing screenshots.

    class InteractiveSessionRecorder:
            def __init__(self, url):
                # Initialize with the URL of the web page to interact with
                self.url = url
                self.recorded_actions = []
                self.screenshot_folder = "screenshots"
                self.screenshot_counter = 1

**Log Function:**

The `log` function is used to print log messages during the session.

        def log(self, message):
                print(message)

**Capture Screenshot Function:**

The `capture_screenshot` function captures a screenshot of the web page for a specific action description.

        def capture_screenshot(self, description):
                screenshot_path = os.path.join(self.screenshot_folder, f"screenshot_{self.screenshot_counter}.png")
                self.screenshot_counter += 1
                try:
                    self.driver.save_screenshot(screenshot_path)
                    self.log(f"Screenshot captured for '{description}'. Path: {screenshot_path}")
                except Exception as e:
                    self.log(f"Failed to capture screenshot for '{description}': {str(e)}")

**Record Action Function:**

The `record_action` function records a user action along with the XPath of the clicked element and captures a screenshot of the action.

        def record_action(self, description):
                self.log(f"Perform the action: {description}")
                xpath = input("Enter the XPath of the clicked element: ")
                action = {'type': 'click', 'xpath': xpath}
                self.recorded_actions.append(action)
                self.capture_screenshot(description)
                self.log("Action recorded.")

**TestBA Class:**

The `TestBA` class represents a test session with British Airways website and provides options for configuring proxies, headless mode, and user credentials.

    class TestBA:
            def __init__(self, proxy=None, headless=False, username=None, password=None):
                self.driver = None
                self.recorder = None
                self.proxy = proxy
                self.headless = headless
                self.username = username
                self.password = password

**Setup Method:**

The `setup_method` function initializes the Selenium WebDriver with the specified options, opens the British Airways website, and sets up the `InteractiveSessionRecorder` for recording actions.

        def setup_method(self, method):
                chrome_options = ChromeOptions()
                if self.proxy:
                    chrome_options.add_argument(f'--proxy-server={self.proxy}')
                if self.headless:
                    chrome_options.add_argument('--headless')
                self.driver = Chrome(options=chrome_options)
                self.vars = {}
                self.driver.get("https://www.britishairways.com/travel/loginr/public/en_gb")
                self.recorder = InteractiveSessionRecorder("https://www.britishairways.com/travel/loginr/public/en_gb/", log_file="session_logs.txt")
                self.recorder.driver = self.driver

**Teardown Method:**

The `teardown_method` function is used to clean up resources and quit the WebDriver after the test session.

        def teardown_method(self, method):
                self.driver.quit()

**Wait for Element Function:**

The `wait_for_element` function is a utility for waiting until an element is present on the web page before performing actions.

        def wait_for_element(self, by, value, timeout=20):
                try:
                    return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
                except TimeoutException:
                    self.recorder.log(f"Element not found: {by} = {value}")
                    return None

**Handle Accept Cookies Function:**

The `handle_accept_cookies` function handles the acceptance of cookies on the website if a "Accept All Cookies" button is present.

        def handle_accept_cookies(self):
                try:
                    accept_cookies_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Agree')]"))
                    )
                    accept_cookies_button.click()
                    self.recorder.log("Clicked 'Accept All Cookies' button.")
                except TimeoutException:
                    self.recorder.log("Accept Cookies button not found or not clickable.")

**Interactive Session Function:**

The `interactive_session` function represents an interactive session with the website. It performs actions such as logging in and records these actions using the `InteractiveSessionRecorder`.

        def interactive_session(self, num_sessions=3):
                self.setup_method(None)
        
                for session in range(num_sessions):
                    self.recorder.log(f"Interactive Session {session + 1}")
                    print(f"Current URL: {self.driver.current_url}")
        
                    self.wait_for_element(By.ID, "membershipNumber")
                    self.wait_for_element(By.ID, "input_password")
        
                    # Handle accept cookies overlay
                    self.handle_accept_cookies()
        
                    # Fill in username and password
                    username_input = self.wait_for_element(By.ID, "membershipNumber")
                    password_input = self.wait_for_element(By.ID, "input_password")
                    
                    if username_input and password_input:
                        username_input.send_keys(self.username)
                        password_input.send_keys(self.password)
        
                        # Press Enter key to submit the form
                        password_input.send_keys(Keys.ENTER)
        
                        self.recorder.log("Submitted login form by pressing Enter.")
                    else:
                        self.recorder.log("Username and password input fields not found.")
        
                    # You can add additional steps as required after logging in
        
                    self.setup_method(None)
        
                self.recorder.replay_sessions()
                self.recorder.learn_common_elements()

**Usage Example:**

To demonstrate the usage of the script with various configurations, we provide an example that creates and starts 10 instances with different proxy, headless, username, and password settings.

    # Create a list of proxy, headless, usernames, and passwords
        proxies = ['proxy1', 'proxy2', 'proxy3']
        headless_options = [True, False]
        usernames = ['user1', 'user2', 'user3']
        passwords = ['pass1', 'pass2', 'pass3']
        
        # Create and start 10 instances with different configurations
        threads = []
        for _ in range(10):
            proxy = proxies[_ % len(proxies)]
            headless = headless_options[_ % len(headless_options)]
            username = usernames[_ % len(usernames)]
            password = passwords[_ % len(passwords)]
            test_instance = TestBA(proxy=proxy, headless=headless, username=username, password=password)
            thread = threading.Thread(target=test_instance.interactive_session)
            threads.append(thread)
        
        # Start the threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to finish
        for thread in threads:
            thread.join()

This example creates 10 instances of the `TestBA` class with different configurations, such as proxies, headless mode, usernames, and passwords, and runs them concurrently in separate threads.

### Proxy Formats

The exact format of a proxy URL can vary depending on the proxy service you're using and its configuration. Below, we outline some common formats for proxy URLs:

1.  **HTTP Proxy:**

**Format:** http://username:password@proxy\_host:proxy\_port

**Example:** http://user123:pass456@proxy.example.com:8080

4.  **HTTPS Proxy:**

**Format:** https://username:password@proxy\_host:proxy\_port

**Example:** https://user789:securepass@proxy.example.com:8443

7.  **Proxy Without Authentication:**

**Format:** http://proxy\_host:proxy\_port

**Example:** http://proxy.example.com:8080

10.  **IP Authentication Proxy:**

**Format:** http://proxy\_ip:proxy\_port

**Example:** http://203.0.113.1:8888

13.  **Proxy with Subdomain:**

**Format:** http://subdomain.proxy\_host:proxy\_port

**Example:** http://sub1.proxy.example.com:8080

16.  **Proxy with Path (Rare):**

**Format:** http://proxy\_host:proxy\_port/path

**Example:** http://proxy.example.com:8080/somepath

19.  **Socks Proxy:**

**Format:** socks5://username:password@proxy\_host:proxy\_port

**Example:** socks5://usersocks:sockspass@proxy.example.com:1080

Each proxy URL typically consists of the following components:

*   **Protocol:** Specifies the type of proxy (e.g., http, https, socks5).
*   **Username and Password (optional):** If your proxy requires authentication, you provide the username and password.
*   **Proxy Host:** The hostname or IP address of the proxy server.
*   **Proxy Port:** The port number on which the proxy server is listening.
*   **Path (optional):** Rarely used, specifies a path or endpoint on the proxy server.

The exact format may vary based on the proxy service provider you are using. When using proxies in your automation script, you should check the documentation or details provided by the proxy service to ensure you're using the correct format and authentication credentials.

In your Python code, you would typically set the proxy URL as a string in the format mentioned above, and then use it when configuring your web scraping or automation tool to route requests through the proxy server.

Source Code
===========

    
                import os
                import threading
                from selenium import webdriver
                from selenium.webdriver.common.by import By
                from selenium.webdriver.common.keys import Keys
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                from undetected_chromedriver import Chrome, ChromeOptions
                from selenium.common.exceptions import TimeoutException
                
                class InteractiveSessionRecorder:
                    def __init__(self, url, log_file=None):
                        self.url = url
                        self.recorded_actions = []
                        self.screenshot_folder = "screenshots"
                        self.screenshot_counter = 1
                        self.log_file = log_file
    
                        if not os.path.exists(self.screenshot_folder):
                            os.makedirs(self.screenshot_folder)
    
                    def log(self, message):
                        print(message)
                        if self.log_file:
                            with open(self.log_file, "a") as log:
                                log.write(message + "\n")
    
                
                    def capture_screenshot(self, description):
                        screenshot_path = os.path.join(self.screenshot_folder, f"screenshot_{self.screenshot_counter}.png")
                        self.screenshot_counter += 1
                        try:
                            self.driver.save_screenshot(screenshot_path)
                            self.log(f"Screenshot captured for '{description}'. Path: {screenshot_path}")
                        except Exception as e:
                            self.log(f"Failed to capture screenshot for '{description}': {str(e)}")
                
                    def record_action(self, description):
                        self.log(f"Perform the action: {description}")
                        xpath = input("Enter the XPath of the clicked element: ")
                        action = {'type': 'click', 'xpath': xpath}
                        self.recorded_actions.append(action)
                        self.capture_screenshot(description)
                        self.log("Action recorded.")
                
                class TestBA:
                    def __init__(self, proxy=None, headless=False, username=None, password=None):
                        self.driver = None
                        self.recorder = None
                        self.proxy = proxy
                        self.headless = headless
                        self.username = username
                        self.password = password
                
                    def setup_method(self, method):
                        chrome_options = ChromeOptions()
                        if self.proxy:
                            chrome_options.add_argument(f'--proxy-server={self.proxy}')
                        if self.headless:
                            chrome_options.add_argument('--headless')
                        self.driver = Chrome(options=chrome_options)
                        self.vars = {}
                        self.driver.get("https://www.britishairways.com/travel/loginr/public/en_gb")
                        self.recorder = InteractiveSessionRecorder("https://www.britishairways.com/travel/loginr/public/en_gb/", log_file="session_logs.txt")
                        self.recorder.driver = self.driver
                
                    def teardown_method(self, method):
                        self.driver.quit()
                
                    def wait_for_element(self, by, value, timeout=20):
                        try:
                            return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
                        except TimeoutException:
                            self.recorder.log(f"Element not found: {by} = {value}")
                            return None
                
                    def handle_accept_cookies(self):
                        try:
                            accept_cookies_button = WebDriverWait(self.driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Agree')]"))
                            )
                            accept_cookies_button.click()
                            self.recorder.log("Clicked 'Accept All Cookies' button.")
                        except TimeoutException:
                            self.recorder.log("Accept Cookies button not found or not clickable.")
                
                    def interactive_session(self, num_sessions=3):
                        self.setup_method(None)
                
                        for session in range(num_sessions):
                            self.recorder.log(f"Interactive Session {session + 1}")
                            print(f"Current URL: {self.driver.current_url}")
                
                            self.wait_for_element(By.ID, "membershipNumber")
                            self.wait_for_element(By.ID, "input_password")
                
                            # Handle accept cookies overlay
                            self.handle_accept_cookies()
                
                            # Fill in username and password
                            username_input = self.wait_for_element(By.ID, "membershipNumber")
                            password_input = self.wait_for_element(By.ID, "input_password")
                            
                            if username_input and password_input:
                                username_input.send_keys(self.username)
                                password_input.send_keys(self.password)
                
                                # Press Enter key to submit the form
                                password_input.send_keys(Keys.ENTER)
                                
                                try:
                                    WebDriverWait(self.driver, 20).until(
                                        EC.presence_of_element_located((By.XPATH, "//div[@id='some_element_id']"))
                                    )
                                    self.successful_logins.append(f"Username: {self.username}, Password: {self.password}")
                                    self.recorder.log("Login successful.")
                                except TimeoutException:
                                    self.failed_logins.append(f"Username: {self.username}, Password: {self.password}")
                                    self.recorder.log("Login failed.")
                    
                                self.recorder.log("Submitted login form by pressing Enter.")
                            else:
                                self.recorder.log("Username and password input fields not found.")
                
                            # You can add additional steps as required after logging in
                
                            self.setup_method(None)
                
                        self.recorder.replay_sessions()
                        self.recorder.learn_common_elements()
                
                # Create a list of proxy, headless, usernames, and passwords
                proxies = ['proxy1', 'proxy2', 'proxy3']
                headless_options = [True, False]
                usernames = ['user1', 'user2', 'user3']
                passwords = ['pass1', 'pass2', 'pass3']
                
                # Create and start 10 instances with different configurations
                threads = []
                for _ in range(10):
                    proxy = proxies[_ % len(proxies)]
                    headless = headless_options[_ % len(headless_options)]
                    username = usernames[_ % len(usernames)]
                    password = passwords[_ % len(passwords)]
                  
                    test_instance = TestBA(proxy=proxy, headless=headless, username=username, password=password)
                    thread = threading.Thread(target=test_instance.interactive_session)
                    threads.append(thread)
                
                # Start the threads
                for thread in threads:
                    thread.start()
                
                # Wait for all threads to finish
                for thread in threads:
                    thread.join()
                
            

