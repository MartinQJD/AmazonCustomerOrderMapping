import sys
import time
import os
from sys import stdin
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#define constants
PRE_SELECTED_RANAGE_1=1
PRE_SELECTED_RANAGE_3=3
PRE_SELECTED_RANAGE_7=7
PRE_SELECTED_RANAGE_14=14
PRE_SELECTED_RANAGE_30=30
PRE_SELECTED_RANAGE_90=90
PRE_SELECTED_RANAGE_180=180
PRE_SELECTED_RANAGE_365=365

MARKET_CA_ID="marketplace_A2EUQ1WTGCTBG2"
MARKET_US_ID="marketplace_ATVPDKIKX0DER"

def WaitForManualLogin():
    """wait for login in the amazon seller central manually.
    Input 'y' to return true, input 'n' to return false
    """
    while True:
        print("\n**********************************")    
        print("Please manually login the amazon seller central before downloading data.")
        print("If login sucessful, enter 'Y + RETURN' to continue,")
        print("of course, you can enter 'X + RETURN' to exit program.")
        print("Are you ready to continue?[Y/X]")
        y_x=stdin.readline().strip()[:1]
        if (y_x.lower()=='y'):
            return True
        elif (y_x.lower()=='x'):
            return False

def IsContinueToDo():
    while True: 
        print("\n**********************************")
        print("Do you continue to download data?")
        print("If yes,enter 'Y + RETURN' to continue,")
        print("otherwise enter 'N + RETURN' to exit.")
        print("What do you choose?[Y/N]")
        y_n=stdin.readline().strip()[:1]
        if (y_n.lower()=='y'):
            return True
        elif (y_n.lower()=='n'):
            return False

def MakeSureLoginStatus():
    while True:
        print("\n**********************************")    
        print("Note:after a period of time,the session whould be expired.If you encounter this situation, please login first. ")
        print("If the page has been logged in,enter 'Y + RETURN' to continue.")
        print("Of course, you can enter 'X + RETURN' to exit program.")
        print("Are you ready to continue?[Y/X]")
        y_x=stdin.readline().strip()[:1]
        if (y_x.lower()=='y'):
            return True
        elif (y_x.lower()=='x'):
            return False
            
def ChooseDownloadingDatePeriod():
     while True: 
        print("\n**********************************")  
        print("How many days of data do you want do download?")
        print("Please enter Option No + RETURN to continue:")
        print("1: 1 days")
        print("2: 3 days")
        print("3: 7 days")
        print("4: 14 days")
        print("5: 30 days")
        print("6: 90 days")
        print("7: 180 days")
        print("8: 365 days")
        
        option=int(stdin.readline())
        if option==1:
            return PRE_SELECTED_RANAGE_1
        elif option==2:
            return PRE_SELECTED_RANAGE_3
        elif option==3:
            return PRE_SELECTED_RANAGE_7
        elif option==4:
            return PRE_SELECTED_RANAGE_14
        elif option==5:
            return PRE_SELECTED_RANAGE_30  
        elif option==6:
            return PRE_SELECTED_RANAGE_90
        elif option==7:
            return PRE_SELECTED_RANAGE_180
        elif option==8:
            return PRE_SELECTED_RANAGE_365
        else:
            print("Please choose valid option number [1-9]")
            
def NoOrderFound(driver):
    try:
        elem=driver.find_element_by_xpath("//span[text()='No Order Found']")    
        if elem.is_displayed():
            return True
        else:
            return False
    except:
        return False

def HasNextPage(driver):
    try:
        nextPage=driver.find_element_by_xpath("//a[@class='myo_list_orders_link'][contains(text(),'Next')]")    
        nextPage.click()
        time.sleep(5)
        if not NoOrderFound(driver):
            return True
        else:
            return False    
    except:
        return False


def Show100RowsPerPage(driver):
    driver.find_element_by_xpath("//select[@name='itemsPerPage']/option[@value='100']").click()
    driver.find_element_by_xpath("//form[@onsubmit='return MYO.LO.DoAjaxSearchCall( this );']//input[@type='image']").click()
    time.sleep(5)
    
def GetCustomerOrderMapping(driver,sku,lastDays,marketplaceId):
    driver.get("https://sellercentral.amazon.com/gp/orders-v2/search/ref=ag_myosearch_apsearch_myo")
    #Search Type = SKU
    driver.find_element_by_xpath("//select[@name='searchType']/option[@value='MerchantSKU']").click()
    #Input SKU
    driver.find_element_by_name("searchKeyword").send_keys(sku)
    
    #Choose exact date scope
    #driver.find_element_by_id("_myoSO_SearchOption_exactDates").click()
    #exactDateBegin=driver.find_element_by_id("exactDateBegin")
    #exactDateBegin.clear()
    #exactDateBegin.send_keys(fromDate)
    #exactDateEnd=driver.find_element_by_id("exactDateEnd")
    #exactDateEnd.clear()
    #exactDateEnd.send_keys(toDate)
    
    #Select last days to search
    driver.find_element_by_xpath("//select[@name='preSelectedRange']/option[@value='" + str(lastDays) + "']").click()
    
    #OrderStatus = Shipped
    driver.find_element_by_xpath("//select[@name='statusFilter']/option[@value='Shipped']").click()
    #Choose Marketplace
    driver.find_element_by_id(marketplaceId).click()
    
    #Click Search
    driver.find_element_by_name("Search").click()
    
    #wait for search result
    time.sleep(5)
    
    #define result
    data=[]
    
    #if no data return directly
    if NoOrderFound(driver):
        return data    
    
    #Change 15 rows/page to 100 rows/page
    Show100RowsPerPage(driver)
    if NoOrderFound(driver):
        return data  
    
    hasDataToParse=True    
    page=1
    #Parse current page of orders
    while True==hasDataToParse:
        #read order lines
        orderRows=driver.find_elements_by_class_name("order-row")   
        print("Page %d,total rows:%d" % (page,len(orderRows)))
        
        #parse customer id and order id
        for orderRow in orderRows:
            cust_id=orderRow.find_element_by_class_name("cust-id").get_attribute('value')
            order_id=orderRow.find_element_by_class_name("order-id").get_attribute('value')
            order_date=orderRow.find_elements_by_xpath(".//td")[1].text.split('\n')[0]
            if cust_id!="":
                data.insert(0,[cust_id,order_id,order_date])
            
        #Try page to next
        hasDataToParse=HasNextPage(driver)
        if hasDataToParse:
            page+=1
            
    return data     

def LoadDataAsDictionary(fileName):
    fileData={}   
    
    if not os.path.isfile(fileName):
        return fileData
    
    with open(fileName,'r') as fo:
        for line in fo.readlines():
            cols=line.split('\t')
            fileData[cols[1]]=cols[0]
    return fileData    
    
def SaveData(fileName,data):
    if (data is None):
        return
        
    #load existing file data into a dictionary with key=order_id
    currentData=LoadDataAsDictionary(fileName)
    
    #write data to file    
    with open(fileName,'a') as fo:
        for row in data:
            if (row[1] not in currentData): #if the order does not exist, append to the file
                fo.write(row[0] + "\t" + row[1] + "\t" + row[2] + "\n" )
    
    
if __name__=="__main__":
    try:
        #Create a new chrome browser instance and open amazon seller central site 
        driver=webdriver.Chrome()
        driver.get("https://SellerCentral.amazon.com")
        driver.maximize_window()
        
        #Because amazon seller central need the second-step verification by mobile, here need to manully login   
        if False==WaitForManualLogin():
            print("Login failed,exit.")
            sys.exit(0)
        
        isContinueToDo=True
        
        while True==isContinueToDo:
            
            datePeriod=ChooseDownloadingDatePeriod()
            
            #Get the pair of customer id and order id, and save as a file.
            #Here you need to specify the SKU and marketplace that you want to download.
            
            #FOR EXAMPLE
            #////////////////////////////////////////////////
            
            #SKU:M000001 
            print("\nBegin to download SKU:M000001")
            ret=GetCustomerOrderMapping(driver,'M000001',datePeriod,MARKET_US_ID)
            if len(ret)>0:
                SaveData("C:\\CustomerOrders\\M000001.csv",ret)
            
            #SKU:M000002
            print("\nBegin to download SKU:M000002")
            ret=GetCustomerOrderMapping(driver,'M000002',datePeriod,MARKET_US_ID)
            if len(ret)>0:
                SaveData("C:\\CustomerOrders\\M000002.csv",ret)
            
            #/////////////////////////////////////////////
            
            print("\nData downloading is over!")
            isContinueToDo=IsContinueToDo()
            if isContinueToDo:
                driver.refresh();
                if not MakeSureLoginStatus():
                    sys.exit(0)
        
    finally:
        if driver is not None:
            driver.close()
    
