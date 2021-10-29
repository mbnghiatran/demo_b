import os, time
import requests
import warnings
from classes import *
warnings.filterwarnings("ignore")
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FOptions
from selenium.webdriver.firefox.service import Service as FService


def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok


def debug_handler(driver):
    for i, handle in enumerate(driver.window_handles):
        print(i, handle.current_url)


def close_all_tab(driver, except_pages = []):
    for i, handle in enumerate(driver.window_handles):
        if handle not in except_pages:
            driver.switch_to.window(handle)
            driver.close()


def get_element_by_xpath(xpath, time = 3):
    button = WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, xpath)))
    return button


def login_wallet(userinfo, driverinfo, driver, session):
    driver.switch_to.window(session)
    try:
        xpath_b_ok = "//span[@class='MuiButton-label' and text()='Ok']"
        b_ok = get_element_by_xpath(xpath_b_ok)
        b_ok.click()
    except:
        pass
    # step 0
    textbox_pass = get_element_by_xpath("//input[@type='password']")
    textbox_pass.send_keys(userinfo.WalletPassword)
    # step 1 
    bcheck_keep_wallet = get_element_by_xpath("//span[text()='Keep wallet unlocked']")
    bcheck_keep_wallet.click()
    # step 2
    b_unlock = get_element_by_xpath("//span[text()= 'Unlock']")
    b_unlock.click()
    # step 3
    auto_connect = get_element_by_xpath("//label[@class='MuiFormControlLabel-root']")
    auto_connect.click()
    # step 4
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") # scroll to ignore hidden
    understand_check = get_element_by_xpath("//span[@class='MuiButton-label' and text()='I understand']")
    understand_check.click()
    # step 5
    bconnect = get_element_by_xpath("//span[@class='MuiButton-label' and text()='Connect']")
    bconnect.click()
    # step 6
    # approve = get_element_by_xpath("//span[@class='MuiButton-label'][contains(text(),'Approve')]")
    approve = get_element_by_xpath("//span[@class='MuiButton-label' and text()='Approve']")
    approve.click()

    sollet_page = driver.current_window_handle
    return sollet_page


def telegram_task(userinfo, driverinfo, driver, session):
    # switch to main_page to keep context of driver
    driver.switch_to.window(driver.window_handles[0])
    # Open and switch to the new window
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get(driverinfo.LinkTelegram)
    # TODO

    # close current window
    driver.close()
    return 


def twitter_task(userinfo, driverinfo, driver):
    # switch to main_page to keep context of driver
    driver.switch_to.window(driver.window_handles[0])
    # Open and switch to the new window
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get(driverinfo.LinkRetweet)

    follow = get_element_by_xpath("//div[@data-testid='confirmationSheetConfirm']").click()
    like = get_element_by_xpath("//div[@data-testid='like']").click()
    retweet = get_element_by_xpath("//div[@data-testid='retweet']").click()
    retweet_confirm = get_element_by_xpath("//div[@data-testid='retweetConfirm']").click()
    quote = get_element_by_xpath("//div[@data-testid='unretweet']").click()
    quote_confirm = get_element_by_xpath("//a[@href='/compose/tweet']").click()
    quote_editor = get_element_by_xpath("//div[@data-testid='tweetTextarea_0']").send_keys(userinfo.create_quote())
    bpost = get_element_by_xpath("//div[@data-testid='tweetButton']").click()
    # Get retweet link
    driver.get("https://twitter.com/" + userinfo.TwitterUsername + "/with_replies")
    newesttweet = get_element_by_xpath("//div[@lang='en']").click()
    retweetLink = driver.current_url
    
    # close current window
    driver.close()
    return retweetLink
    

def bypass_capcha(driver, session):
    driver.switch_to.window(session)
    # TODO
    return


def fill_form(driver, session):
    driver.switch_to.window(session)
    # TODO
    return


if __name__ == "__main__":
    cfg = yaml_loader("./config.yaml")
    Driverinfo = DriverInfomation(cfg)
    
    ## modified config
    ref_url = cfg['ref_url']
    start, end = cfg['start'], cfg['end']
    profiles = [f"B{i}" for i in list(range(start, end+1))]
    
    for cnt, profile_name in enumerate(profiles):
        print(f"-------------------- Runing Profile: {profile_name} -------------------------")
        profile_path = os.path.join(cfg["profiles_root"], profile_name)
        Userinfo = UserInfomation(cfg)
        Userinfo.FirefoxProfile = "/Users/baonghia/Library/Application Support/Firefox/Profiles/1rs8mr8h.abc"
        
        ## set firefox option
        options = FOptions()
        options.headless = True
        # options.binary_location = os.path.join(profile_path, "App/firefox64/firefox.exe")
        options.profile = Userinfo.FirefoxProfile
        
        ## init driver
        service = FService(Driverinfo.driver_path)
        driver = Firefox(service=service, options=options)

        try:
            # Begin
            driver.get(ref_url)
            main_page = driver.current_window_handle
            main_e1 = get_element_by_xpath("//button[contains(@class, connect-wallet)]").click()
            main_e2 = get_element_by_xpath("//img[@alt='Sollet.io']").click()
            
            # handle wallet
            # sollet_page must be run in background
            sollet_page = login_wallet(Userinfo, Driverinfo, driver, session = driver.window_handles[1])
            close_all_tab(driver, except_pages=[main_page, sollet_page])

            # ## handle twitter
            # retweet_link = twitter_task(Userinfo, Driverinfo, driver)
            # print(f"Done Twitter !!!. Link: {retweet_link}")

            # # Fill form
            # bypass_capcha(driver, main_page)
            # fill_form(driver, main_page)

            driver.quit()
            print("Done sucessfully !!!")
        
        except:
            driver.quit()
            print(f"Fail !!!")
            pass