import os
import time
from selenium import webdriver


def downloadYouTubemp3(url):
    currentDirectory = os.path.dirname(__file__).replace("scripts", "")
    chromedriverPath = currentDirectory + "\setup\chromedriver"
    print(currentDirectory)
    try:
        youtube_url = url

        userhome = str(os.path.expanduser('~'))
        desktop_path = userhome + '\Desktop\\'
        # print(desktop_path)

        driver = chromedriverPath
        # print(driver)

        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': desktop_path}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument("--disable-extensions")
        driver = webdriver.Chrome(driver, chrome_options=chrome_options)

        driver.set_window_position(-10000, 0)

        # driver.set_window_position(-10000, 0)

        driver.get("http://www.flvto.biz/youtube-to-mp3/")
        xpath1 = '//*[@id="convertForm"]/div[1]/div[1]/label/div'
        button = driver.find_element_by_xpath(xpath1).click()
        src = driver.page_source
        inputElement = driver.find_element_by_class_name("url-conv")
        inputElement.send_keys(youtube_url)
        xpath = '//*[@id="convertForm"]/div[1]/div[2]/button'
        button = driver.find_element_by_xpath(xpath).click()

        while ('downloads' not in driver.current_url):
            time.sleep(1)

        if ('downloads' in driver.current_url):
            xpath3 = '/html/body/header/div[2]/div/div[2]/div[2]/div[1]/a[1]'
            button = driver.find_element_by_xpath(xpath3)
            driver.execute_script("arguments[0].click();", button)
            # print("Downloaded to your Desktop! ")
        time.sleep(180)

        driver.quit()
    except Exception as e:
        print(e)


link = ""

with open(os.path.dirname(__file__) + "\youtube_link.txt", "r") as file_reader:
    link = file_reader.readline()

downloadYouTubemp3(link)
