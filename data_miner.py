import datetime
import requests
import lxml.html
import threading
from second import try_genius_search

class Data_miner:
    
    current_year = datetime.datetime.now().year
    
    def start(self):
        input_date = {
            'year': self.get_year(),
            'mounth': self.get_mounth(),
            'day': self.get_day()
        }
        self.req_to_billboard(input_date)
        
    def req_to_billboard(self,input_date):
        year = input_date.get('year')
        mounth = input_date.get('mounth')
        day = input_date.get('day')
        response = requests.get(f'https://www.billboard.com/charts/hot-100/{year}-{mounth}-{day}')
        self.format_billboard_data(response.text)        
        
    def format_billboard_data(self,billboard_response_text):
        doc = lxml.html.document_fromstring(billboard_response_text)
        
        songs = [el.text_content() for el in doc.find_class('chart-element__information__song')[:20]]
        artists = [el.text_content() for el in doc.find_class('chart-element__information__artist')[:20]]
        positions = [el.text_content() for el in doc.find_class('chart-element__rank__number')[:20]]
        date = doc.find_class('date-selector__button')[0].text_content().strip()

        primary_artists = []
        feat_artists = []

        for i in artists:
            if ' & ' in i:
                primary_artists.append([artist for artist in i.split(' & ')])
            elif ' X ' in i:
                primary_artists.append([artist for artist in i.split(' X ')])
            elif ' Presents ' in i:
                primary_artists.append([artist for artist in i.split(' Presents ')])
            elif ' Duet With ' in i:
                primary_artists.append([artist for artist in i.split(' Duet With ')])
            elif ' With ' in i:
                primary_artists.append([artist for artist in i.split(' With ')])
            elif ' And ' in i:
                primary_artists.append([artist for artist in i.split(' And ')])
            elif ' / ' in i:
                primary_artists.append([artist for artist in i.split(' / ')])
            elif ' + ' in i:
                primary_artists.append([artist for artist in i.split(' + ')])
            elif ' Featuring ' in i:
                feat_artists.append([artist for artist in i.split(' Featuring ')[1:]])
                primary_artists.append([i.split(' Featuring ')[0]])
            else:
                primary_artists.append([i])
                feat_artists.append(None)

        charts_data = [{
            "song":song,
            "primary_artists":primary_artist,
            "feat_artists":feat_artist,
            "position":position,
            'date':date
        } for song, primary_artist, feat_artist, position in zip(songs,primary_artists,feat_artists,positions) ]

        with open(f'billboard_charts/{date}.txt', 'w') as f:
            for i in charts_data:
                f.write(f'{str(i)}\n')
        
        self.get_lyrics(charts_data)
    
    def get_lyrics(self,charts_data):
        
        for i in charts_data[:10]:    
            
            song_title = i.get('song')
            artist_name = i.get('primary_artists')[0]
            
            thread = threading.Thread(target=self.try_genius_url,args=(song_title, artist_name))
            thread.start()

                
    def try_genius_url(self, song_title, artist_name):
        try:
            formated_song_title = song_title.lower().replace("$", 's').replace("'", '').replace('.', '').replace('(','').replace(')','').replace('!', '').replace('[','').replace(']','').replace('-','').replace('**','uc').replace(' ', '-').replace('The ', '').replace(',', '').replace('?', '')
            formated_artist_name = artist_name.lower().replace("$", 's').replace("'", '').replace('.', '').replace('(','').replace(')','').replace('!', '').replace('p!nk', 'pink').replace('[','').replace(']','').replace(' ', '-').replace('The ', '').replace('A ', '').replace(',', '')
            print(formated_song_title, formated_artist_name)
            response = requests.get(f'https://genius.com/{formated_artist_name}-{formated_song_title}-lyrics')
            
            if response.status_code != 200:
                self.try_genius_api(song_title, artist_name)
            else:
                try:
                    lyrics_HTML = lxml.html.document_fromstring(response.text)
                    lyrics = lyrics_HTML.find_class('lyrics')[0].getchildren()[1].text_content()
                    with open(f'lyrics/{song_title}.txt', 'w') as f:
                        f.write(lyrics)
                except:
                    print('NOT FOUND')

        except:
            self.try_genius_api(song_title, artist_name)
    
    def try_genius_api(self, song_title, artist_name):
        print('API...')
        
        try:
            token = '1q_a0c-q5EV19LkQVopxDnrtE4i6LrKZC8BgffE6i-waRjGUEOCwCTsmCjPFYMyT'
            headers = {'Authorization': 'Bearer ' + token}
            search_url = f'https://api.genius.com/search?q={song_title} {artist_name}'
            response = requests.get(search_url, headers=headers)
            for i in response.json()['response']['hits']:
                if song_title in i['result']['title'] or artist_name in i['result']['primary_artist']['name']:
                    path = i['result']['path']
                    response = requests.get(f'https://genius.com{path}')

                    if response.status_code != 200:
                        self.try_genius_search(song_title, artist_name)
                    else:
                        try:
                            lyrics_HTML = lxml.html.document_fromstring(response.text)
                            lyrics = lyrics_HTML.find_class('lyrics')[0].getchildren()[1].text_content()
                            with open(f'lyrics/{song_title}.txt', 'w') as f:
                                f.write(lyrics)
                            return
                        except:
                            print('NOT FOUND')
                    break
                else:
                    return try_genius_search(song_title, artist_name)
        except:
            try_genius_search(song_title, artist_name)
        
    def get_year(self):
        year = input(f'Enter year from 1958 to {self.current_year}: ')
        return self.check_year(year)
        
    def get_mounth(self):
        mounth = input('Enter mounth: from 01 to 12: ')
        return self.check_mounth(mounth)
        
    def get_day(self):
        day = input('Enter day: from 01 to 31: ')
        return self.check_day(day)
        
    def check_year(self,year):
        if year.isnumeric():
            
            if int(year) <= self.current_year and int(year) >= 1958:
                return year
            else:
                print(f'Year must be a number from 1958 to {self.current_year}')
                self.get_year()
        else:
            print('Year must be a number')
            self.get_year()
        
    def check_mounth(self,mounth):
        if mounth.isnumeric():
            
            if int(mounth) <= 12 and int(mounth) >= 1:
                if len(mounth) != 2:
                    mounth = '0' + mounth
                return mounth
            else:
                print(f'Mounth must be a number from 1 to 12')
                self.get_mounth()
        else:
            print('Mounth must be a number')
            self.get_mounth()
    
    def check_day(self,day):
        if day.isnumeric():
            
            if int(day) <= 31 and int(day) >= 1:
                
                if len(day) != 2:
                    day = '0' + day
                return day
            else:
                print(f'Day must be a number from 1 to 31')
                self.get_day()
        else:
            print('Day must be a number')
            self.get_day()
            
instance = Data_miner().start()
# instance = Data_miner().try_genius_search('All For Love','B/Rodwart/Sting')