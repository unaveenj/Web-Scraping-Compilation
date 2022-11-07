from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm

titles = []
ranks = []
year = []
ratings = []
directors = []

def get_additional_info(link):
    try:
        s=requests.get(link)
        soup=BeautifulSoup(s.text,'html.parser')
        director = soup.find('a',class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link').text.strip()
        return director
    except:
        director = "None"
        return director
# https://www.imdb.com/search/title?title_type=feature&primary_language=kn&sort=moviemeter,asc&ref_=tt_dt_ln
def get_basic_info():
    try:
        s=requests.get("https://www.imdb.com/india/top-rated-indian-movies/")
        # print(s.status_code)
        soup = BeautifulSoup(s.text,'html.parser')
        movie = soup.find('tbody',class_="lister-list").find_all('tr')
        size = len(movie)
        for i in tqdm(range(0, size), desc="Getting Movies"):
            titles.append(movie[i].find('td',class_='titleColumn').find('a').text)
            ranks.append(movie[i].find('td',class_='titleColumn').get_text(strip=True).split(".")[0])
            year.append(movie[i].find('td',class_='titleColumn').span.text.strip('()'))
            ratings.append(float(movie[i].find('td',class_="ratingColumn imdbRating").text.strip()))
            link = f"https://www.imdb.com{movie[i].find('td', class_='titleColumn').find('a').get('href')}"
            directors.append(get_additional_info(link))


    except Exception as e:
        print(e)

def generate_csv():
    output = {
        'Movie':titles,
        'Rank':ranks,
        'Released Year':year,
        'Ratings':ratings,
        'Director':directors
    }
    df = pd.DataFrame(output)
    df.to_csv('Top Indian Films.csv')
    print("Data saved to Top Indian Films.csv!")

def main():
    get_basic_info()
    generate_csv()

if __name__ =='__main__':
    main()