# Game Price Monitor 🎮

This project monitors game prices on the Nintendo eShop and sends notifications when there is a price drop.

## Installation
bash
git clone https://github.com/your_user/repository_name.git
cd repository_name
pip install -r requirements.txt

## Chrome Profile Path Configuration

For the program to work correctly, you must create a Chrome profile so that your eShop Prices login is maintained. (Selenium is the name of the tool used to perform the automation)

1. Open Chrome manually using the profile you already configured in your script. You can do this using Windows Run or Command Prompt:

chrome.exe --user-data-dir="C:\Users\YOUR_USER\AppData\Local\Google\Chrome\User Data\Profile Selenium"

-Important: Close all Chrome windows before running this command to avoid instance conflicts.

2. Log in to the Website:
-Access the website manually: https://eshop-prices.com
-Log in with your email and password.
-Check if you are authenticated and that the website maintains the session even after closing the tab.

3. Close Chrome. Selenium cannot use a profile that is already open.
-Run your Python program normally. It will use the profile that already has the authenticated session and will not ask for the login again.

You will also need to configure the path of this Chrome profile using a file called `.env`.

1. Open the `.env` file in your project directory.
2. Edit the line to match your Chrome profile path:
```env
CHROME_PROFILE_PATH=C:/Users/YOUR_USER/AppData/Local/Google/Chrome/User Data/Profile Selenium
```
3. Save the file and run the program.

-The path should use / or \\ instead of \ to avoid escaping issues on Windows.
