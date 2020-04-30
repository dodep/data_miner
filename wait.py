from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time



t1 = time.time()
options = Options()
options.headless = True
capa = DesiredCapabilities.FIREFOX
capa["pageLoadStrategy"] = "none"

driver = webdriver.Firefox(options=options,executable_path='./geckodriver' ,desired_capabilities=capa)
wait = WebDriverWait(driver, 10)

driver.get('http://genius.com/')
# class visibility_of_element_located(object):

wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="application"]/div/div[1]/form/input')))

driver.execute_script("window.stop();")
el = driver.find_element_by_xpath('//*[@id="application"]/div/div[1]/form/input')
try:
    el.send_keys('hello')
    el.send_keys(Keys.ENTER)
    el.submit()
except:
    pass
wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[2]/search-result-section/div/div[2]/search-result-items/div[1]/search-result-item/div/mini-song-card/a')))
driver.execute_script("window.stop();")
try:
    before_url = driver.current_url
    song = driver.find_element_by_xpath('/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[2]/search-result-section/div/div[2]/search-result-items/div[1]/search-result-item/div/mini-song-card/a').click()
    wait.until(EC.url_contains('-lyrics'))
    print(driver.current_url)
    print(time.time() - t1)
except:
    pass
driver.quit()