import lxml.html
import requests
import threading
from genius_app import Genius

class Billboard:
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
            elif '/' in i:
                primary_artists.append([artist for artist in i.split('/')])
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
        
    def get_lyrics(self, charts_data):
        for i in charts_data[:10]:    
            
            song_title = i.get('song')
            artist_name = i.get('primary_artists')[0]
            date = i.get('date')
            
            thread = threading.Thread(target=Genius(date, song_title, artist_name).try_genius_url,args=())
            thread.start()