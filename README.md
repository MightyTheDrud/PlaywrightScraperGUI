GUI JavaScript Spotter Tool

Overview
This script automates interaction with web applications using Playwright, a browser automation library, to check and display rendering issues across different environments. It uses a Tkinter GUI to interact with users and display results visually.

Key Features:
- Browser Automation: Utilizes Playwright with Microsoft Edge in both headless and non-headless modes to interact with and scrape web pages.
- GUI Interface: Provides a user-friendly Tkinter interface for selecting environments and viewing data.
- Periodic Checks: Automatically refreshes data every 10 minutes, with options to change this frequency.
- Data Visualization: Displays counts and allows for in-depth viewing of rendering issues through pop-up tables.

Installation Prerequisites:
- Python 3.x
- Microsoft Edge (for the specified executable path), can be replaced with Chrome if preferred, both are chromium-based.

Libraries Utilized:
- tkinter
- playwright
- beautifulsoup4
- pytz

Setup:
Install Python packages in a virtual environment to avoid conflcts, in my batch script, I installed below pip packages in a virtual environment called "portaPython":

pip install tkinter playwright beautifulsoup4 pytz

Ensure Microsoft Edge is installed at the path specified in the script or update the path accordingly.

Usage:
Once configured properly with virtual environment "portaPython", run this script from JavascriptScraperWithGUIRun.bat

Interaction:
Menu Bar: Select from "Option One", "Option Two", or "Option Three" to choose which environment to interact with.

GUI Elements:
- Render Image: Indicates the start of the rendering check.
- Local Side / Remote Side: Shows counts of issues found locally or remotely.
- Failed Render: Number of failed renderings.
- IQ Render, Amount, Render Reject, Balance: Specific counters for different rendering queues.

Functionality:
- Automatic Refresh: Every 10 minutes (configurable), the script will recheck and update the GUI if minimized or not.
- Alert Popups: Notifies users if any issues are detected in each category.
- Detailed View: Clicking on any counter opens a popup with detailed data in a table format.

Functions Explained:
- dateFind(): Gets the current date formatted for US/Eastern time zone.
- popupTables(): Generates a Tkinter popup window with tabular data.
- Option Functions (optionOne, optionTwo, optionThree): Initialize browser sessions for different environments.
- interactWithMainTestPage(): Handles navigation and data extraction from the web application.
- workflowPageSpecificTable(): Extracts and formats data from specific grids on the page.
- menuOption*(): Correlate with the options in the GUI menu, executing tasks for each environment.
- spotterGUI Class: Manages the creation and behavior of the GUI, including periodic data refresh and user interaction.

Notes:
- Headless Mode: Options Two and Three use headless mode for Edge, which means no browser window will open during execution.
- Security: The script uses --disable-blink-features=AutomationControlled to bypass some automation detection mechanisms.

Troubleshooting:
- If the script fails to interact with web pages, check to ensure the Edge executable is indeed correct.
- When in doubt with playwright or just programming in general, add as many prints as possible to help debug your script and ensure you're pulling the proper elements at critical points.
- In the batch script, comment out pythonw at the end and swap with python; pythonw hides the console, swap back to pythonw when you're finished debugging the program. =)
- Always also ensure the webpages desired are still up and running; also ensure elements haven't changed; most likely the case if you get your program up and running, but the program fails after a period of time.












