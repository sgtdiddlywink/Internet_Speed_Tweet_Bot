"""
IMPORTANT NOTE: Do not have 2FA for Twitter account.  This script will not work if it is turned on.

This script will begin by checking your internet download and upload speeds.  It is important to not be performing
other tasks on your computer when this happens or be over wifi as that can negatively influence the speeds you will be
getting.

Once the speeds have been gathered they will be compared to your guaranteed speeds per your contract below (You will
need to provide this as it is different for everyone.

the script will then log in to your Twitter account and post a new tweet to ISP on whether you are getting your
guaranteed speeds.

You will need to add your twitter login and password below for this to work.

You may need to adjust the sleep time after clicking the "GO" button for initializing the internet speed test.  It is by
default set to 40 seconds but may need to be increased based on your speeds.

Be careful running this to many times in a row as Twitter my recognize it and ask for a captcha check.

"""

# Import and install appropriate modules below.
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Put your own credentials here.  Ensure there is no 2FA turned on or this will not work.
TWITTER_LOGIN = "YOUR TWITTER LOGIN"
TWITTER_PASSWORD = "YOUR TWITTER PASSWORD"

# Add your ISP's Twitter handle below as a string to automatically populate the tweet.
ISP_TWITTER_HANDLE = "YOUR ISP TWITTER HANDLE"

# User should modify these value inputs depending on their agreed upon contract with their ISP.  In the contract,
# there should be minimum speeds that will be met.  Input these below.  Values are in Mbps.
PROMISED_DOWNLOAD_SPEED = 100
PROMISED_UPLOAD_SPEED = 10

"""Need to install the appropriate browser driver and place .exe in accessible file."""
# Chrome driver path should reference the .exe browser driver.
chrome_driver_path = "THE PATH TOWARDS YOUR DRIVER"


# Create class for the bot.
class InternetSpeedTwitterBot:

    # Initialize basics features of the class.
    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.up = None
        self.down = None

    # Create method for obtaining your internet speed.
    def get_internet_speed(self):

        # Open internet speed URL and obtain an upload speed and a download speed
        url = "https://www.speedtest.net/"
        self.driver.get(url=url)

        # Sleep for two seconds to let page load.
        time.sleep(2)

        # Click on the "GO" button to initialize internet speed test.
        self.driver.find_element(
            By.XPATH,
            "//*[@id='container']/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]"
        ).click()

        # Sleep for 40 seconds for internet speed test.  This may need to be increased depending on your speeds.
        time.sleep(40)
        # Check down and up speeds and save them as variable.
        self.down = float(self.driver.find_element(
            By.XPATH,
            "//*[@id='container']/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]"
            "/div/div[2]/span"
        ).text)
        self.up = float(self.driver.find_element(
            By.XPATH,
            "//*[@id='container']/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]"
            "/div/div[2]/span"
        ).text)

    # Create method for tweeting at your ISP.
    def tweet_at_provider(self):

        # Open twitter on browser.
        url = "https://twitter.com/"
        self.driver.get(url=url)

        # Sleep for two seconds to let page load.
        time.sleep(2)

        # Click on "Sign In" button at the bottom.
        self.driver.find_element(
            By.XPATH,
            "//*[@id='react-root']/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a"
        ).click()

        # Sleep for two seconds to let page load.
        time.sleep(2)

        # Fill in the username input box that appears.
        self.driver.find_element(
            By.XPATH,
            "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]"
            "/label/div/div[2]/div/input"
        ).send_keys(TWITTER_LOGIN)

        # Click the "Next" button.
        self.driver.find_element(
            By.XPATH,
            "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]"
        ).click()

        # Sleep for two seconds to let page load.
        time.sleep(2)

        # Fill in the password input box that appears.
        self.driver.find_element(
            By.XPATH,
            "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]"
            "/div/label/div/div[2]/div[1]/input"
        ).send_keys(TWITTER_PASSWORD)

        # Sleep for two seconds to load.
        time.sleep(2)

        # Click on the "Log in" button.
        self.driver.find_element(
            By.XPATH,
            "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]"
            "/div/div/div/div"
        ).click()

        # Sleep for ten seconds to load.
        time.sleep(10)

        # Click on input box for tweet.
        self.driver.find_element(
            By.CSS_SELECTOR,
            "a[aria-label='Tweet']"
        ).click()

        # The tweet message below:
        tweet_message = f"Hey {ISP_TWITTER_HANDLE}!, why is my internet speed {self.down}Mbps Down and {self.up}Mbps " \
                        f"Up when I pay for {PROMISED_DOWNLOAD_SPEED}Mbps Down and {PROMISED_UPLOAD_SPEED}Mbps UP?"

        # Fill in your tweet with the information.
        self.driver.find_element(
            By.CSS_SELECTOR,
            "div[data-contents='true']"
        ).send_keys(tweet_message)

        # Click on "Tweet" Button.
        self.driver.find_element(
            By.XPATH,
            "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div/div/div"
            "/div/div[2]/div[3]/div/div/div[2]/div[4]/div/span/span"
        ).click()

        # Print a message on the console to notify that tweet has been performed.
        print("Tweet has been posted. Have a nice day.")

        # Quit out of Twitter window.
        self.driver.quit()


# Create a bot object from the class.
tweet_bot = InternetSpeedTwitterBot(chrome_driver_path)
# Get the internet speeds.
tweet_bot.get_internet_speed()

# Assign variables to the internet speeds
download_speed = tweet_bot.down
upload_speed = tweet_bot.up

# If statement to check to see if either down or up speeds promised are less than what is being provided.  If they are
# not then bot will tweet it out.
if download_speed < PROMISED_DOWNLOAD_SPEED or upload_speed < PROMISED_UPLOAD_SPEED:
    tweet_bot.tweet_at_provider()
else:
    print("Speeds look great!")



