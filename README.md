# Project Wishlist - Game Price Monitor 🎮

This project monitors game prices on the Nintendo eShop and sends notifications when there is a price drop. It automaticaly checks the eshop-prices.com website, on your wishlist section, filtered by discounts, and checks for price changes. This was not tested for lists with more than one page (filtered with discounts).

It will create a folder called `historico_precos` with a `.csv` file for each game. It will also create a useful information log called `log_de_execução` after it's done running.

## Chrome Profile Path Configuration

For the program to work correctly, you must create a Chrome profile so that your eShop Prices login is maintained. (Selenium is the name of the tool used to perform the automation)

1. Create a folder named 'Profile Selenium' like this: "C:\Users\YOUR_USER\AppData\Local\Google\Chrome\User Data\Profile Selenium"

2. Open Chrome manually using the profile you already configured in your script. You can do this using Windows Run or Command Prompt:
```
chrome.exe --user-data-dir="C:\Users\YOUR_USER\AppData\Local\Google\Chrome\User Data\Profile Selenium"
```
-Important: Close all Chrome windows before running this command to avoid instance conflicts.

3. Log in to the Site:
-Access the site manually: https://eshop-prices.com
-Log in with your email and password.
-Check if you are authenticated and that the site maintains the session even after closing the tab.

4. Close Chrome. Selenium cannot use a profile that is already open.
-Run your Python program normally. It will use the profile that already has the authenticated session and will not ask for the login again.

You will also need to configure the path of this Chrome profile using a file called `.env`.

1. Open the `.env` file in your project directory.

2. Edit the line to match your Chrome profile path. We are also adding the eshop-prices URL(this needs to be the URL for the wishlist filtered with dicounts). Should it change with time, edit it in this file:
```env
CHROME_PROFILE_PATH=C:/Users/YOUR_USER/AppData/Local/Google/Chrome/User Data/Profile Selenium
BASE_URL=https://eshop-prices.com/wishlist?currency=BRL&sort_by=discount&direction=desc
```

3. Save the file and run the program.

-The path should use / or \\ instead of \ to avoid escaping issues on Windows.

## Scheduling the script to run automaticaly

1. Open the Task Manager, pressing 'Win+R' and typing:

```
taskschd.msc
```

2. Create a task:

Triggers: Choose the frequency and time you want it to be run.
Actions: (If you are using the python file)Start a Program and Browse to this file in the project folder: 'executar_script.bat'
Actions: (If you are using the EXE file)Start a Program and Browse to the executable file.
