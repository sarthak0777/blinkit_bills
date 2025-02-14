from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import pyautogui

# Set up the Chrome WebDriver
driver = webdriver.Chrome()  # Ensure chromedriver is in PATH or provide the correct path

# Open Blinkit and log in manually
driver.get("https://www.blinkit.com/")




time.sleep(3)

try:
    # Step 1: Click on "Fetch location online"
    fetch_location_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Fetch location online')]")
    fetch_location_button.click()
    time.sleep(5)  # Wait for location fetching

    # Check if the location was set successfully
    current_url = driver.current_url
    if "location" not in current_url:  # If location fetching failed, proceed to manual selection
        raise Exception("Location fetching failed")
except:
    try:
        # Step 2: Click on the manual location option
        # manual_location_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Enter location manually')]")
        # manual_location_button.click()
        # time.sleep(2)

        # Step 3: Enter "Delhi" in the search box
        location_input = driver.find_element(By.CLASS_NAME, "LocationSearchBox__InputSelect-sc-1k8u6a6-0")
        location_input.send_keys("D")
        time.sleep(0.5)
        location_input.send_keys("e")
        time.sleep(0.5)
        location_input.send_keys("l")
        time.sleep(2)  # Wait for the list to appear

        # Step 4: Select the first suggestion
        first_suggestion = driver.find_element(By.CLASS_NAME, "LocationSearchList__LocationListContainer-sc-93rfr7-0")
        first_suggestion.click()
        time.sleep(2)

    except Exception as e:
        print(f"Failed to set location: {e}")
        driver.quit()
        exit()


# ProfileButton__Text-sc-975teb-2
login_button = driver.find_element(By.CLASS_NAME, "ProfileButton__Text-sc-975teb-2")
login_button.click()


input("Please log in to your Blinkit account, then press Enter to continue...")

# Navigate to the Orders page
driver.get("https://www.blinkit.com/account/orders")

# Wait for orders to load
time.sleep(5)

# Scroll down and click "Load More" until all orders are loaded
for _ in range(30):
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for page update

        # Find and click the "Load More" button (Update the class name if necessary)
        button = driver.find_element(By.CLASS_NAME, "load-more-button")  # Adjust this based on Blinkit's HTML
        button.click()
        time.sleep(2)
    except Exception as e:
        print("No more 'Load More' button or an error occurred:", e)
        break

# Allow time for all orders to fully load
time.sleep(5)

# Locate all orders on the page
#class="OrderHistory__ViewDetailsButton-sc-1xssk01-2 jiUXCL"
# orders = driver.find_elements(By.XPATH, "//div[contains(@class, 'OrderHistory__ViewDetailsButton-sc-1xssk01-2')]")
# OrderHistory__ViewDetailsButton-sc-1xssk01-2
orders = driver.find_elements(By.CLASS_NAME, "OrderHistory__ViewDetailsButton-sc-1xssk01-2")  # Adjust this based on Blinkit's structure
# Create a folder to save screenshots
if not os.path.exists("Blinkit_Invoices_FullScreen"):
    os.makedirs("Blinkit_Invoices_FullScreen")

# Loop through each order and take a full-screen screenshot
for i in range(len(orders)):
    try:
        order = orders[i]
        order.click()  # Open order details
        time.sleep(2)

        # Capture a full desktop screenshot
        screenshot_path = f"Blinkit_Invoices_FullScreen/invoice_{i+1}.png"
        pyautogui.screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")
        
        # Close the invoice details to return to the order list
        # close_button = driver.find_element(By.XPATH, "//span[contains(@class, 'close-icon')]")
        close_button = driver.find_element(By.CLASS_NAME, "OrderDetailsWrapper__BackButtonIcon-sc-3jjy9q-6")  # Adjust as needed
        close_button.click()
        time.sleep(2)
        orders = driver.find_elements(By.CLASS_NAME, "OrderHistory__ViewDetailsButton-sc-1xssk01-2")
    except Exception as e:
        print(f"Could not capture screenshot for order {i+1}: {e}")
        # Try closing the order details popup in case of failure
        try:
            close_button = driver.find_element(By.CLASS_NAME, "OrderDetailsWrapper__BackButtonIcon-sc-3jjy9q-6")
            close_button.click()
        except:
            pass

# Close the browser
driver.quit()
