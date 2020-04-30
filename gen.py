import lxml.html
import requests

# min value 1958-08-04(YYYY-MM-DD), max date.now()
year = input('Enter year from 1958 up to current: ')
mounth = input('Enter mounth: ')
day = input('Enter day from: ')
position = input('Enter song position from 1 to 100: ')
print(f'https://www.billboard.com/charts/hot-100/{year}-{mounth}-{day}')
response = requests.get(f'https://www.billboard.com/charts/hot-100/{year}-{mounth}-{day}')

doc = lxml.html.document_fromstring(response.text)

songs = [el.text_content() for el in doc.find_class('chart-element__information__song')]
artists = [el.text_content() for el in doc.find_class('chart-element__information__artist')]
positions = [el.text_content() for el in doc.find_class('chart-element__rank__number')]
date = doc.find_class('date-selector__button')[0].text_content().strip()

main_artists = []
feat_artists = []

def fa(a):
    return a.replace(' & ', ', ').replace(' X ', ', ').replace(' Presents ', ', ').replace(' Duet With ', ', ').replace(' With ', "', '").replace(' And ', ', ')

for i in artists:
    if ' & ' in i:
        main_artists.append([artist for artist in i.split(' & ')])
    elif ' X ' in i:
        main_artists.append([artist for artist in i.split(' X ')])
    elif ' Presents ' in i:
        main_artists.append([artist for artist in i.split(' Presents ')])
    elif ' Duet With ' in i:
        main_artists.append([artist for artist in i.split(' Duet With ')])
    elif ' With ' in i:
        main_artists.append([artist for artist in i.split(' With ')])
    elif ' And ' in i:
        main_artists.append([artist for artist in i.split(' And ')])
    elif ' Featuring ' in i:
        feat_artists.append([artist for artist in i.split(' Featuring ')[1:]])
        main_artists.append([i.split(' Featuring ')[0]])
    else:
        main_artists.append([i])
        feat_artists.append(None)

data = [{"song":song, "main_artists":main_artist, "feat_artists":feat_artist, "position":position, 'date':date} for song, main_artist, feat_artist, position in zip(songs,main_artists,feat_artists,positions)]
with open('data.txt', 'w') as f:
    for i in data:
        f.write(f'{str(i)}\n')
        
# a = data[int(position)-1]
# song_title = a.get('song')
# artist_name = a.get('main_artists')[0]

# def f_title(a):
#     return a.lower().replace("'", '').replace('.', '').replace('(','').replace(')','').replace('!', '').replace('[','').replace(']','').replace('-','').replace('**','uc').replace(' ', '-').replace('The ', '').replace(',', '').replace('?', '')
# def f_name(a):
#     return a.lower().replace("'", '').replace('.', '').replace('(','').replace(')','').replace('!', 'i').replace('[','').replace(']','').replace(' ', '-').replace('The ', '').replace('A ', '').replace(',', '')
# print(f'https://genius.com/{f_name(artist_name)}-{f_title(song_title)}-lyrics')
# lyrics_response = requests.get(f'https://genius.com/{f_name(artist_name)}-{f_title(song_title)}-lyrics')

# try:
#     doc = lxml.html.document_fromstring(lyrics_response.text)
#     lyrics = doc.find_class('lyrics')[0].getchildren()[1].text_content()
#     with open('lyrics.txt', 'w') as f:
#         f.write(lyrics)

# except Exception as err:
#     print('fail')
#     print(err)
