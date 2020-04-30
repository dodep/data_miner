import requests
import lxml.html

def try_genius_search(song_title, artist_name):
        print(f'SEARCH...{song_title} by {artist_name}')
        try:
            print('try')
            from selenium import webdriver
            from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.by import By
            print('import done')

            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            capa = DesiredCapabilities.CHROME
            capa["pageLoadStrategy"] = "none"

            driver = webdriver.Chrome(executable_path='./chromedriver' ,desired_capabilities=capa, options=options)
            wait = WebDriverWait(driver, 10)
            print('driver ready')

            driver.get('http://genius.com/')
            print('GET')

            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="application"]/div/div[1]/form/input')))

            driver.execute_script("window.stop();")
            el = driver.find_element_by_xpath('//*[@id="application"]/div/div[1]/form/input')
            try:
                print('input found')
                el.send_keys(f"{song_title}")
                el.send_keys(Keys.ENTER)
                el.submit()
            except:
                pass
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[2]/search-result-section/div/div[2]/search-result-items/div[1]/search-result-item/div/mini-song-card/a')))
            driver.execute_script("window.stop();")
            try:
                print('song found')
                before_url = driver.current_url
                song = driver.find_element_by_xpath('/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[2]/search-result-section/div/div[2]/search-result-items/div[1]/search-result-item/div/mini-song-card/a').click()
                wait.until(EC.url_contains('-lyrics'))
                
                response = requests.get(f'{driver.current_url}')
                
                if response.status_code != 200:
                    return None
                else:
                    print('REQ TO LYRICs')
                    try:
                        lyrics_HTML = lxml.html.document_fromstring(response.text)
                        lyrics = lyrics_HTML.find_class('lyrics')[0].getchildren()[1].text_content()
                        print('lyrics found')
                        with open(f'lyrics/{song_title}.txt', 'w') as f:
                            f.write(lyrics)
                        print('lyrics wrote')
                        # driver.quit()
                        return driver.quit()
                    except:
                        print('NOT FOUND')
                        return driver.quit()
            except:
                print('REQ failed')
                return driver.quit()
        except:
            print('SEARCH failed')
            return driver.quit()