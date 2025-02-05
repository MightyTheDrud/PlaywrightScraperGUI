"""
While less efficient than scraping pages with beautifulsoup outright, this gets the job done successfully using playwright and a locally-installed, headless instance of
Microsoft Edge. Three varied options exist to choose between within the tkinter GUI, options grabbed from menu choice initially, then grabbed again automatically every 10 minutes.
If you minimize the application, it'll reopen after 10 minutes, whether any values are found in the applicable web application grids or not. If values are found, those
values
counted can be clicked on the GUI to get a more in-depth look for any more serious issues.
"""

from tkinter import *
from tkinter import ttk
from playwright.async_api import async_playwright
from datetime import datetime, timedelta
import pytz
from bs4 import BeautifulSoup
from asyncio import ensure_future
import asyncio
import threading


class AsyncThreading(threading.Thread):
    def __init__(self, target_coroutine, *args):
        super().__init__()
        self.target_coroutine = target_coroutine
        self.args = args
        self.loop = None
    
    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.target_coroutine(*self.args))


#Get current date for Eastern Time Zone
def dateFind():
    est = pytz.timezone("US/Eastern")
    currentDate = datetime.now(est)
    
    useDate = currentDate
    
    useDateFormatted = useDate.strftime("%m/%d/%Y").lstrip("0").replace("/0", "/")
    
    return useDateFormatted 


#If the number of items grabbed from list of values is greater than zero, utilize this popup table to display them.
def popupTables(inputDataListofLists, windowName):

    popupWindow = Toplevel()
    popupWindow.title(windowName)
    
    columnTreeView = ttk.Treeview(popupWindow, columns = [f"col{i}" for i in range(len(inputDataListofLists[0]))], show = "headings")
    
    #This for loop covers the headers
    for i, colHeader in enumerate(inputDataListofLists[0]):
        columnTreeView.heading(f"col{i}", text=colHeader)
        columnWidth = max(100, len(colHeader) * 10)
        columnTreeView.column(f"col{i}", width = columnWidth, anchor="center")
    
    #This for loop covers the data rows
    for dataRow in inputDataListofLists[1:]:
        columnTreeView.insert("", "end", values = dataRow)
    
    #Further force header styling
    popupWindowStyle = ttk.Style()
    popupWindowStyle.theme_use("clam")
    popupWindowStyle.configure("Treeview.Heading", background = "#FF7518", foreground = "#000000")
    
    #Pack the widget
    columnTreeView.pack(expand = True, fill = BOTH)
    
    #Set size of window
    popupWindow.geometry("1200x600")


#Initial prep for each application menu option.  

async def optionOne(play):

    testApplicationURL = "https://your-test-application-here-one.com/application.aspx"
    
    edgeLocation = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    
    webBrowser = await play.chromium.launch(executable_path = edgeLocation, headless = False, args=['--disable-blink-features=AutomationControlled', '--headless=new'])
    
    page = await webBrowser.new_page()

    await page.goto(testApplicationURL, wait_until = "networkidle")
    
    return page, webBrowser
    
    
async def optionTwo(play):
    testApplicationURL = "https://your-test-application-here-two.com/application.aspx"
    
    edgeLocation = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    
    webBrowser = await play.chromium.launch(executable_path = edgeLocation, headless = True, args=['--disable-blink-features=AutomationControlled', '--headless=new'])
    
    page = await webBrowser.new_page()

    await page.goto(testApplicationURL, wait_until = "networkidle")
    
    return page, webBrowser


async def optionThree(play):

    testApplicationURL = "https://your-test-application-here-three.com/application.aspx"
    
    edgeLocation = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    
    webBrowser = await play.chromium.launch(executable_path = edgeLocation, headless = True, args=['--disable-blink-features=AutomationControlled', '--headless=new'])
    
    page = await webBrowser.new_page()

    await page.goto(testApplicationURL, wait_until = "networkidle")     
    
    return page, webBrowser


async def interactWithMainTestPage(page):

    iFrameLoginOpenElement = await page.wait_for_selector("#iframeContent")
    
    iFrameLoginOpen = await iFrameLoginOpenElement.content_frame()
    
    await iFrameLoginOpen.wait_for_load_state()
    
    signOnButton = await iFrameLoginOpen.wait_for_selector("#buttonOK")
    await signOnButton.click()
    
    await page.wait_for_load_state('networkidle')
    
    iFrameWelcomePageElement = await page.wait_for_selector("#iframeContent")
    
    iFrameWelcomePage = await iFrameWelcomePageElement.content_frame()
    
    mainDataPageOuterElement = "welcomeScreen\\:navigation#navimenu #welcome_ID17"
    
    mainDataPageButton = await iFrameWelcomePage.wait_for_selector(mainDataPageOuterElement)
    
    await mainDataPageButton.click()
    
    print("On the main data page now.")

    await page.wait_for_timeout(1000)
    
    mainDataMenuFrame = await page.wait_for_selector("#iframeContent")
    
    mainDataMenu = await mainDataMenuFrame.content_frame()
    
    searchForDate = await mainDataMenu.wait_for_selector("#Text3")
    
    await searchForDate.fill(dateFind())
    
    searchButton = await mainDataMenu.wait_for_selector("#tdButtonMainData")
    await searchButton.click()
    
    print("In the main data menu wrapper...  ")

    await page.wait_for_timeout(500)
    
    #Start by grabbing counter values displayed on the main data page.

    localDatabaseSide = (await mainDataMenu.locator("#tdLocalCount").text_content()).strip()
    remoteDatabaseSide = (await mainDataMenu.locator("#tdRemoteCount").text_content()).strip()
    
    print(f"Rendering jobs found in the local database side but not in the remote database side: {localDatabaseSide}")
    print(f"Rendering jobs found in the remote database side but not in the local database side: {remoteDatabaseSide}\n")
    
    #Grab the local database side grid element.
    databaseGridElement = await mainDataMenu.wait_for_selector("mainDatabasePage\\:datagrid#localgrdElmnt")
    
    #Grab the local database header row th tags
    localDatabaseThTags = await databaseGridElement.eval_on_selector_all(
        "table > tbody > tr:nth-of-type(9) > td > div > table > tbody > tr > th",
        "elements => elements.map(th => th.innerText.trim())"
    )
    
    #Quick print to ensure the tags were grabbed correctly.
    for index, thTag in enumerate(localDatabaseThTags):
        if index == 0:
            continue
        
        print(thTag, end = "  ")

    print()
    
    #Grab the actual grid values now.
    databaseGridThTableValues = await databaseGridElement.eval_on_selector_all(
        "table tbody tr:nth-of-type(12) td div table tbody tr:not(.TemplateRow)",
        "rows => rows.map(row => Array.from(row.querySelectorAll('td')).map(td => td.innerText))"
    )
    
    #Print the grid values to ensure everything is correct when debugging.
    for trTag in databaseGridThTableValues:
        for index, tdTag in enumerate(trTag, start = 0):
            if index == 0:
                continue
            
            print(tdTag, end = " ")
    
        print()

    print()
    
    #Assemble the complete list by adding header row and grid data rows together.
    databaseGridCompleteList = localDatabaseThTags + databaseGridThTableValues
    
    #Get remote database side values now

    await mainDataMenu.locator("#tdRemoteCount").click()
    
    await page.wait_for_timeout(1000)
    
    #Remote database side element
    remoteDatabaseGridElement = await mainDataMenu.wait_for_selector("mainDatabasePage\\:datagrid#remotegrdElmnt")
    
    #Grab the remote database header row th tags
    remoteDatabaseThTags = await remoteDatabaseGridElement.eval_on_selector_all(
        "table > tbody > tr:nth-of-type(9) > td > div > table > tbody > tr > th",
        "elements => elements.map(th => th.innerText.trim())"
    )
    
    #Quick print to ensure the tags were grabbed correctly.
    for index, thTag in enumerate(remoteDatabaseThTags):
        if index == 0:
            continue
        
        print(thTag, end = "  ")

    print()
    
    #Grab the actual grid values now.
    remoteDatabaseGridThTableValues = await remoteDatabaseGridElement.eval_on_selector_all(
        "table tbody tr:nth-of-type(12) td div table tbody tr:not(.TemplateRow)",
        "rows => rows.map(row => Array.from(row.querySelectorAll('td')).map(td => td.innerText))"
    )
    
    #Print the grid values to ensure everything looks correct when debugging.
    for trTag in remoteDatabaseGridThTableValues:
        for index, tdTag in enumerate(trTag, start = 0):
            if index == 0:
                continue
            
            print(tdTag, end = " ")

        print()

    print()
    
    #Assemble the complete list by adding header row and grid data rows together.
    remoteDatabaseGridCompleteList = remoteDatabaseThTags + remoteDatabaseGridThTableValues
    
    #Go to the extra failed renderings page now, starting by going to the main desktop page. 

    await page.locator("span", has_text = "Main Desktop Page >").click()
    await page.wait_for_timeout(2000)
    
    print("Back on the main page post login")

    #Back on main page post login.
    
    postLoginPageOuterElement = "mainDatabasePage\\:datagrid#navimenu #naviID3"
    loginManagementPageButton = await iFrameWelcomePage.wait_for_selector(postLoginPageOuterElement)
    await loginManagementPageButton.click()
    
    await page.wait_for_timeout(2000)
    
    print("On the remaining items management page...")

    #On remaining items management page now.
    remainingManagementOuterFrame = await page.wait_for_selector("#iframeContent")
    remainingManagementFrame = await remainingManagementOuterFrame.content_frame()
    await remainingManagementFrame.wait_for_selector("body", state = "attached")
    
    print("After checking if frame is attached...")

    #Fill the From and To Process Date fields
    remainingManagementFromBoxElement = "#textFromProcDate"
    fromBoxWorkflowPageManagement = await remainingManagementFrame.wait_for_selector(remainingManagementFromBoxElement)
    
    await fromBoxWorkflowPageManagement.fill(dateFind())
    
    workflowToBoxElementManagement = "#textToProcDate"
    toBoxWorkflowPageManagement = await remainingManagementFrame.wait_for_selector(workflowToBoxElementManagement)
    await toBoxWorkflowPageManagement.fill(dateFind())
    
    #Click the Search button
    workflowPageSearchButtonElement = "[name = 'buttonSearchHere']"
    workflowPageSearchButton = await remainingManagementFrame.wait_for_selector(workflowPageSearchButtonElement)
    await workflowPageSearchButton.click()
    
    await page.wait_for_timeout(1000)
    
    #Grab RenderIQ row now:
    workflowGridSelector = "mainDatabasePage\\:datagrid#mainRenderGrid"
    
    workflowGridDataInner = remainingManagementFrame.locator(workflowGridSelector)
    renderIQElemenent = workflowGridDataInner.locator("table > tbody > tr:nth-child(12) > td > div > table > tbody > tr:nth-child(5)")
    
    print("IQ Render element clicked...")

    await renderIQElemenent.click()
    
    await page.wait_for_timeout(500)
    
    #Grab the row values now, starting with the table element itself
    renderRowDisplayOuterTableElement = await remainingManagementFrame.wait_for_selector("mainDatabasePage\\:datagrid#gridFullRenderResults")
    
        iqRenderCompleteList = await workflowPageSpecificTable(renderRowDisplayOuterTableElement)
    
    print(f"iqRenderCompleteList: {iqRenderCompleteList}")
    print()
    
    amountElement = workflowGridDataInner.locator("table > tbody > tr:nth-child(12) > td > div > table > tbody > tr:nth-child(18)")
    
    print("Amount element clicked...")
    
    await amountElement.click()
    
    await page.wait_for_timeout(500)
    
    amountCompleteList = await workflowPageSpecificTable(renderRowDisplayOuterTableElement)
    
    print(f"amountCompleteList: {amountCompleteList}")
    print()
    
    renderRejectElement = workflowGridDataInner.locator("table > tbody > tr:nth-child(12) > td > div > table > tbody > tr:nth-child(11)")
    
    print("Render reject element clicked...")
    
    await renderRejectElement.click()
    
    await page.wait_for_timeout(500)
    
    renderRejectCompleteList = await workflowPageSpecificTable(renderRowDisplayOuterTableElement)
    
    print(f"renderRejectCompleteList: {renderRejectCompleteList}")
    print()
    
    renderBalanceElement = workflowGridDataInner.locator("table > tbody > tr:nth-child(12) > td > div > table > tbody > tr:nth-child(13)")
    
    print("Render Balance element clicked...")
    
    await renderBalanceElement.click()
    
    await page.wait_for_timeout(500)
    
    #specific to render balance
    renderRowDisplayOuterTableElementBalance = await remainingManagementFrame.wait_for_selector("mainDatabasePage\\:datagrid#gridFullRenderResults")
    
    if renderRowDisplayOuterTableElementBalance:
        renderBalanceCompleteList = await workflowPageSpecificTable(renderRowDisplayOuterTableElementBalance)
    
    else:
        renderBalanceCompleteList = await workflowPageSpecificTable(renderRowDisplayOuterTableElement)
    
    print(f"renderBalanceCompleteList: {renderBalanceCompleteList}")
    print()
    
    return localDatabaseSide, remoteDatabaseSide, failedExtraRenderingsListLength, databaseGridCompleteList, remoteDatabaseGridCompleteList, failedExtraRenderingsCompleteList, iqRenderCompleteList, amountCompleteList, renderRejectCompleteList, renderBalanceCompleteList


async def workflowPageSpecificTable(renderRowDisplayOuterTableElement):
    #Grab the header row column values
    workflowTableColumnLabels = await renderRowDisplayOuterTableElement.eval_on_selector_all(
        "table tbody tr:nth-of-type(7) td div table tbody tr th",
        "elements => elements.map(th => th.innerText.trim())"
    )
    
    #Grab the actual data rows now
    workflowTableActualData = await renderRowDisplayOuterTableElement.eval_on_selector_all(
        "table tbody tr:nth-of-type(12) td div table tbody tr:not(.TemplateRow)",
        "rows => rows.map(row => Array.from(row.querySelectorAll('td')).map(td => td.innerText.trim()))"
    )
    
    print(workflowTableActualData)
    
    workflowTableColumnLabels = [workflowTableColumnLabels]
    
    finalWorkflowCompleteList = workflowTableColumnLabels + workflowTableActualData
    
    return finalWorkflowCompleteList    
    

async def menuOptionOne():
    async with async_playwright() as play:
        
        page, webBrowser = await optionOne(play)
        
        localDatabaseSide, remoteDatabaseSide, failedExtraRenderingsListLength, databaseGridCompleteList, remoteDatabaseGridCompleteList, failedExtraRenderingsCompleteList, iqRenderCompleteList, amountCompleteList, renderRejectCompleteList, renderBalanceCompleteList = await interactWithMainTestPage(page)
        
        #close browser instance completely
        await page.close()
        await webBrowser.close()
        
        return localDatabaseSide, remoteDatabaseSide, failedExtraRenderingsListLength, databaseGridCompleteList, remoteDatabaseGridCompleteList, failedExtraRenderingsCompleteList, iqRenderCompleteList, amountCompleteList, renderRejectCompleteList, renderBalanceCompleteList


async def menuOptionTwo():
    async with async_playwright() as play:
        
        page, webBrowser = await optionTwo(play)
        
        localDatabaseSide, remoteDatabaseSide, failedExtraRenderingsListLength, databaseGridCompleteList, remoteDatabaseGridCompleteList, failedExtraRenderingsCompleteList, iqRenderCompleteList, amountCompleteList, renderRejectCompleteList, renderBalanceCompleteList = await interactWithMainTestPage(page)
        
        #close browser instance completely
        await page.close()
        await webBrowser.close()
        
        return localDatabaseSide, remoteDatabaseSide, failedExtraRenderingsListLength, databaseGridCompleteList, remoteDatabaseGridCompleteList, failedExtraRenderingsCompleteList, iqRenderCompleteList, amountCompleteList, renderRejectCompleteList, renderBalanceCompleteList


async def menuOptionThree():
    async with async_playwright() as play:
        
        page, webBrowser = await optionThree(play)
        
        localDatabaseSide, remoteDatabaseSide, failedExtraRenderingsListLength, databaseGridCompleteList, remoteDatabaseGridCompleteList, failedExtraRenderingsCompleteList, iqRenderCompleteList, amountCompleteList, renderRejectCompleteList, renderBalanceCompleteList = await interactWithMainTestPage(page)
        
        #close browser instance completely
        await page.close()
        await webBrowser.close()
        
        return localDatabaseSide, remoteDatabaseSide, failedExtraRenderingsListLength, databaseGridCompleteList, remoteDatabaseGridCompleteList, failedExtraRenderingsCompleteList, iqRenderCompleteList, amountCompleteList, renderRejectCompleteList, renderBalanceCompleteList


class spotterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI JavaScript Spotter Tool")

        self.guiSpotterLabel = Label(root, text = "GUI JavaScript Spotter Tool", font = ("Helvetica", 25, "bold"), bg = "#FF7518", fg = "#000000")
        self.renderImageLabel = Label(root, text = "Render\nImage", font = ("Helvetica", 23, "bold"), bg = "#FF7518", fg = "#000000")
        self.localSideLabel = Label(root, text = "Local Side", font = ("Helvetica", 10, "bold"), bg = "#FF7518", fg = "#000000")
        self.remoteSideLabel = Label(root, text = "Remote Side", font = ("Helvetica", 10, "bold"), bg = "#FF7518", fg = "#000000")
        self.localRenderSideCountLabel = Label(root, text = "0", font = ("Helvetica", 25, "bold"), cursor = "hand2", bg = "#FF7518", fg = "#000000")
        self.remoteRenderSideCountLabel = Label(root, text = "0", font = ("Helvetica", 25, "bold"), cursor = "hand2", bg = "#FF7518", fg = "#000000")
        self.failedRenderLabel = Label(root, text = "Failed\nRender", font = ("Helvetica", 23, "bold"), bg = "#FF7518", fg = "#000000")
        self.failedRenderCountLabel = Label(root, text = "0", font = ("Helvetica", 25, "bold"), cursor = "hand2", bg = "#FF7518", fg = "#000000")
        
        #IQ Render, Amount, Reject, and Balance
        self.iqRenderLabel = Label(root, text = "IQ Render", font = ("Helvetica", 10, "bold"), bg = "#FF7518", fg = "#000000")
        self.amountLabel = Label(root, text = "Amount", font = ("Helvetica", 10, "bold"), bg = "#FF7518", fg = "#000000")
        self.renderRejectLabel = Label(root, text = "Render Reject", font = ("Helvetica", 10, "bold"), bg = "#FF7518", fg = "#000000")
        self.renderBalanceLabel = Label(root, text = "Balance", font = ("Helvetica", 10, "bold"), bg = "#FF7518", fg = "#000000")
        
        #Counters for: IQ Render, Amount, Reject, and Balance
        self.iqRenderCountLabel = Label(root, text = "0", font = ("Helvetica", 25, "bold"), cursor = "hand2", bg = "#FF7518", fg = "#000000")
        self.amountCountLabel = Label(root, text = "0", font = ("Helvetica", 25, "bold"), cursor = "hand2", bg = "#FF7518", fg = "#000000")
        self.renderRejectCountLabel = Label(root, text = "0", font = ("Helvetica", 25, "bold"), cursor = "hand2", bg = "#FF7518", fg = "#000000")
        self.renderBalanceCountLabel = Label(root, text = "0", font = ("Helvetica", 25, "bold"), cursor = "hand2", bg = "#FF7518", fg = "#000000")

        self.guiSpotterLabel.pack(side="top", pady=10)
        self.renderImageLabel.place(relx=0.10, rely=0.25, anchor="w")
        self.localSideLabel.place(relx=0.03, rely=0.40, anchor="w")
        self.remoteSideLabel.place(relx=0.20, rely=0.40, anchor="w")
        self.localRenderSideCountLabel.place(relx=0.08, rely=0.55, anchor="w")
        self.remoteRenderSideCountLabel.place(relx=0.26, rely=0.55, anchor="w")
        self.failedRenderLabel.place(relx=0.90, rely=0.25, anchor="e")
        self.failedRenderCountLabel.place(relx=0.78, rely=0.55, anchor="e")
        
        #Placing in GUI: IQ Render, Amount, Reject, and Balance
        self.iqRenderLabel.place(relx=0.08, rely=0.70, anchor="w")
        self.amountLabel.place(relx=0.24, rely=0.70, anchor="w")
        self.renderRejectLabel.place(relx=0.73, rely=0.70, anchor="e")
        self.renderBalanceLabel.place(relx=0.90, rely=0.70, anchor="e")
        
        #Placing counters in GUI for: IQ Render, Amount, Reject, and Balance
        self.iqRenderCountLabel.place(relx=0.08, rely=0.80, anchor="w")
        self.amountCountLabel.place(relx=0.26, rely=0.80, anchor="w")
        self.renderRejectCountLabel.place(relx=0.68, rely=0.80, anchor="e")
        self.renderBalanceCountLabel.place(relx=0.88, rely=0.80, anchor="e")

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        self.currentOption = None
        self.scheduledTaskID = None

        #Configure GUI Menu at top left
        
        menu = Menu(self.root)
        self.root.config(menu = menu)

        item = Menu(menu, tearoff = 0)

        menu.add_cascade(label = "Choose Environment", menu = item)

        item.add_command(label = "Option One", command = lambda: self.setOption("Option One"))
        item.add_command(label = "Option Two", command = lambda: self.setOption("Option Two"))
        item.add_command(label = "Option Three", command = lambda: self.setOption("Option Three"))

        self.root.bind("", self.minimizeWindow)
        
    
    #This function generates an alert popup that displays topmost on a user's screen, a message can be added, OK button also exists to close popup.

    def alertMessage(self, localCount, message):
        self.alert = Toplevel(self.root)
        self.alert.title("Alert")
        self.alert.geometry("400x200")
        
        self.alert.deiconify()
        self.alert.lift()
        self.alert.attributes("-topmost", True)
        self.alert.focus_force()
        
        messageAlert = Label(self.alert, text = str(localCount) + message)
        messageAlert.pack(pady = 10)
        
        okBtn = Button(self.alert, text = "OK", command = self.alert.destroy)
        okBtn.pack(pady = 5)
        
        self.root.deiconify()
        self.root.state("normal")
        self.root.lift()
        self.root.focus_set()
        
        self.alert.lift()
        self.alert.focus_set()
        
    
    #Properly minimize the GUI
    def minimizeWindow(self, event = None):
        if self.root.state() == "iconic":
            self.root.withdraw()
            self.root.after(100, self.restoreWindow)
    
    #Aids in restoring the GUI when minimized
    def restoreWindow(self):
        if self.root.state() == "normal":
            self.root.deiconify()
            self.root.lift()
        else:
            self.root.after(100, self.restoreWindow)
    

    async def renderImageHelper(self, localDatabaseSide, remoteDatabaseSide, failedExtraRenderingsListLength, databaseGridCompleteList, remoteDatabaseGridCompleteList, failedExtraRenderingsCompleteList, iqRenderCompleteList, amountCompleteList, renderRejectCompleteList, renderBalanceCompleteList):
        #Only for debugging, hidden to users due to python implementation:
        print("databaseGridCompleteList: ")
        print(databaseGridCompleteList)
        
        databaseGridCompleteList2 = [databaseGridCompleteList[:9],] + databaseGridCompleteList[9:]
        
        databaseGridCompleteList3 = [innerList[1:] for innerList in databaseGridCompleteList2]
        
        print("\nModified databaseGridCompleteList3... ")
        print(databaseGridCompleteList3)
        
        print()
        print("remoteDatabaseGridCompleteList: ")
        print(remoteDatabaseGridCompleteList)
        
        remoteDatabaseGridCompleteList2 = [remoteDatabaseGridCompleteList[:7],] + remoteDatabaseGridCompleteList[7:]
        print("\nModified remoteDatabaseGridCompleteList... ")
        print(remoteDatabaseGridCompleteList2)
        
        print()
        print("failedExtraRenderingsCompleteList: ")
        print(failedExtraRenderingsCompleteList)
        
        failedExtraRenderingsCompleteList2 = [failedExtraRenderingsCompleteList[:11],] + failedExtraRenderingsCompleteList[11:]
        failedExtraRenderingsCompleteList3 = [innerList[1:] for innerList in failedExtraRenderingsCompleteList2]
        print("\nModified failedExtraRenderingsCompleteList... ")
        print(failedExtraRenderingsCompleteList3)
        
        print()
        print("Finished displaying each list of list of strings")
        print("\n")

        self.localRenderSideCountLabel.config(text = localDatabaseSide)
        self.remoteRenderSideCountLabel.config(text = remoteDatabaseSide)
        self.failedRenderCountLabel.config(text = failedExtraRenderingsListLength)
        
        self.localRenderSideCountLabel.bind("", lambda event: popupTables(databaseGridCompleteList3, "Local Render Results Found"))
        self.remoteRenderSideCountLabel.bind("", lambda event: popupTables(remoteDatabaseGridCompleteList2, "Remote Render Results Found"))
        self.failedRenderCountLabel.bind("", lambda event: popupTables(failedExtraRenderingsCompleteList3, "Failed Renders"))
        
        #IQ Render, Amount,Reject, and Balance
        iqRenderCompleteListLength = (len(iqRenderCompleteList) - 1)
        amountCompleteListLength = (len(amountCompleteList) - 1)
        renderRejectCompleteListLength = (len(renderRejectCompleteList) - 1)
        renderBalanceCompleteListLength = (len(renderBalanceCompleteList) - 1)
        
        self.iqRenderCountLabel.config(text = str(iqRenderCompleteListLength))
        self.iqRenderCountLabel.bind("", lambda event: popupTables(iqRenderCompleteList, "IQ Render Queue"))
        
        self.amountCountLabel.config(text = str(amountCompleteListLength))
        self.amountCountLabel.bind("", lambda event: popupTables(amountCompleteList, "Amount Queue"))
        
        self.renderRejectCountLabel.config(text = str(renderRejectCompleteListLength))
        self.renderRejectCountLabel.bind("", lambda event: popupTables(renderRejectCompleteList, "Render Reject Queue"))
        
        self.renderBalanceCountLabel.config(text = str(renderBalanceCompleteListLength))
        self.renderBalanceCountLabel.bind("", lambda event: popupTables(renderBalanceCompleteList, "Render Balance Queue"))
        
        if int(localDatabaseSide) > 0:
            self.alertMessage(localDatabaseSide, " item(s) found in local render queue.")
        
        if int(remoteDatabaseSide) > 0:
            self.alertMessage(remoteDatabaseSide, " item(s) found in remote render queue.")
        
        if int(failedExtraRenderingsListLength) > 0:
            self.alertMessage(failedExtraRenderingsListLength, " item(s) found in failed extra renderings queue.")
        
        if int(iqRenderCompleteListLength) > 0:
            self.alertMessage(iqRenderCompleteListLength, " item(s) found in the IQ Render queue")
        
        if int(amountCompleteListLength) > 0:
            self.alertMessage(amountCompleteListLength, " item(s) found in the Amount queue.")
        
        if int(renderRejectCompleteListLength) > 0:
            self.alertMessage(renderRejectCompleteListLength, " item(s) found in the Render Reject queue.")
        
        if int(renderBalanceCompleteListLength) > 0:
            self.alertMessage(renderBalanceCompleteListLength, " item(s) found in the Render Balance queue.")
        
        else:
            self.root.deiconify()
    

    async def renderImageOptionOne(self):
        print("In Render Image option one function")
        localDatabaseSide, remoteDatabaseSide, failedExtraRenderingsListLength, databaseGridCompleteList, remoteDatabaseGridCompleteList, failedExtraRenderingsCompleteList, iqRenderCompleteList, amountCompleteList, renderRejectCompleteList, renderBalanceCompleteList = await menuOptionOne()

        await self.renderImageHelper(localDatabaseSide, remoteDatabaseSide, failedExtraRenderingsListLength, databaseGridCompleteList, remoteDatabaseGridCompleteList, failedExtraRenderingsCompleteList, iqRenderCompleteList, amountCompleteList, renderRejectCompleteList, renderBalanceCompleteList)
        
    
    async def renderImageOptionTwo(self):
        print("In Render Image option two function")
        localDatabaseSide, remoteDatabaseSide, failedExtraRenderingsListLength, databaseGridCompleteList, remoteDatabaseGridCompleteList, failedExtraRenderingsCompleteList, iqRenderCompleteList, amountCompleteList, renderRejectCompleteList, renderBalanceCompleteList = await menuOptionTwo()

        await self.renderImageHelper(localDatabaseSide, remoteDatabaseSide, failedExtraRenderingsListLength, databaseGridCompleteList, remoteDatabaseGridCompleteList, failedExtraRenderingsCompleteList, iqRenderCompleteList, amountCompleteList, renderRejectCompleteList, renderBalanceCompleteList)
        
    
    async def renderImageOptionThree(self):
        print("In Render Image option three function")
        localDatabaseSide, remoteDatabaseSide, failedExtraRenderingsListLength, databaseGridCompleteList, remoteDatabaseGridCompleteList, failedExtraRenderingsCompleteList, iqRenderCompleteList, amountCompleteList, renderRejectCompleteList, renderBalanceCompleteList = await menuOptionThree()

        await self.renderImageHelper(localDatabaseSide, remoteDatabaseSide, failedExtraRenderingsListLength, databaseGridCompleteList, remoteDatabaseGridCompleteList, failedExtraRenderingsCompleteList, iqRenderCompleteList, amountCompleteList, renderRejectCompleteList, renderBalanceCompleteList)
    

    def setOption(self, optionName):
        if self.scheduledTaskID:
            self.root.after_cancel(self.scheduledTaskID)
        
        self.currentOption = optionName
        self.scheduleAutoRun()
        
    
    #Function re-runs JavaScript site grabber functionality every 10 minutes currently, but can be changed.

    def scheduleAutoRun(self):
        
        if self.currentOption == "Option One":
            worker = AsyncThreading(self.renderImageOne)
            worker.start()

        elif self.currentOption == "Option Two":
            worker = AsyncThreading(self.renderImageTwo)
            worker.start()
            
        elif self.currentOption == "Option Three":
            worker = AsyncThreading(self.renderImageThree)
            worker.start()
            
        #Set to check every 5 minutes
        #self.scheduledTaskID = self.root.after(300000, self.scheduleAutoRun)
        
        #Set to check every 10 minutes
        self.scheduledTaskID = self.root.after(600000, self.scheduleAutoRun)
        
        #Set to check every 1 minute
        #self.scheduledTaskID = self.root.after(60000, self.scheduleAutoRun)

    def update(self):
        self.root.update_idletasks()
        self.root.update()
        self.root.after(1000, self.update)


root = Tk()

root.title("GUI JavaScript Spotter")

root.geometry("900x600")

root.config(bg = "#FF7518")


appInit = spotterGUI(root)

appInit.update()

root.mainloop()
    
    