import requests
import lxml.html
import os

class Genius:
    def __init__(self, date, song_title, artist_name):
        self.date = date
        self.song_title = song_title
        self.artist_name = artist_name
    
    def try_genius_url(self):
        try:
            formated_song_title = self.song_title.lower().replace("$", 's').replace("'", '').replace('.', '').replace('(','').replace(')','').replace('!', '').replace('[','').replace(']','').replace('-','').replace('**','uc').replace(' ', '-').replace('The ', '').replace(',', '').replace('?', '')
            formated_artist_name = self.artist_name.lower().replace("$", 's').replace("'", '').replace('.', '').replace('(','').replace(')','').replace('!', '').replace('p!nk', 'pink').replace('[','').replace(']','').replace(' ', '-').replace('The ', '').replace('A ', '').replace(',', '')
            url = f'https://genius.com/{formated_artist_name}-{formated_song_title}-lyrics'
            try:
                response = requests.get(url)
                lyrics_HTML = lxml.html.document_fromstring(response.text)
                lyrics = lyrics_HTML.find_class('lyrics')[0].getchildren()[1].text_content()
                song_title = self.song_title.replace('/','-')
                artist_name = self.artist_name.replace('/','-')
                filename = f'lyrics/{self.date}/{song_title}-{artist_name}.txt'
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, 'w') as f:
                    f.write(lyrics)
            except:
                self.try_genius_api()
        except:
            self.try_genius_api()
    
    def try_genius_api(self):
        try:
            token = '1q_a0c-q5EV19LkQVopxDnrtE4i6LrKZC8BgffE6i-waRjGUEOCwCTsmCjPFYMyT'
            headers = {'Authorization': 'Bearer ' + token}
            search_url = f'https://api.genius.com/search?q={self.song_title} {self.artist_name}'
            response = requests.get(search_url, headers=headers)
            
            url = None
            
            for i in response.json()['response']['hits']:
                if self.song_title in i['result']['title'] or self.artist_name in i['result']['primary_artist']['name']:
                    url = i['result']['url']
                    break
            if url is not None:
                try:
                    response = requests.get(url)
                    lyrics_HTML = lxml.html.document_fromstring(response.text)
                    lyrics = lyrics_HTML.find_class('lyrics')[0].getchildren()[1].text_content()
                    song_title = self.song_title.replace('/','-')
                    artist_name = self.artist_name.replace('/','-')
                    filename = f'lyrics/{self.date}/{song_title}-{artist_name}.txt'
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, 'w') as f:
                        f.write(lyrics)
                except:
                    self.try_genius_search()
            else:
                self.try_genius_search()
        except:
            self.try_genius_search()
            
    def try_genius_search(self):
        try:
            from selenium import webdriver
            from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.by import By

            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            capa = DesiredCapabilities.CHROME
            capa["pageLoadStrategy"] = "none"

            driver = webdriver.Chrome(executable_path='./chromedriver' ,desired_capabilities=capa, options=options)
            wait = WebDriverWait(driver, 10)

            driver.get('http://genius.com/')

            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="application"]/div/div[1]/form/input')))

            driver.execute_script("window.stop();")
            el = driver.find_element_by_xpath('//*[@id="application"]/div/div[1]/form/input')
            try:
                el.send_keys(f"{self.song_title}")
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
                try:
                    response = requests.get(driver.current_url)
                    lyrics_HTML = lxml.html.document_fromstring(response.text)
                    lyrics = lyrics_HTML.find_class('lyrics')[0].getchildren()[1].text_content()
                    song_title = self.song_title.replace('/','-')
                    artist_name = self.artist_name.replace('/','-')
                    filename = f'lyrics/{self.date}/{song_title}-{artist_name}.txt'
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, 'w') as f:
                        f.write(lyrics)
                    return driver.quit()
                except:
                    print('F_A_I_L_E_D')
            except:
                print('REQ failed')
                return driver.quit()
        except:
            print('SEARCH failed')
            return driver.quit()