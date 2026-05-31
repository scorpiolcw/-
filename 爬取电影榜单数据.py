import requests
import csv
from lxml import html
import re

TOP_MOVIE_URL = 'https://www.themoviedb.org/movie/top-rated'
BASE_URL = 'https://www.themoviedb.org'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.themoviedb.org/movie/top-rated",
    "Origin": "https://www.themoviedb.org",
    "X-Requested-With": "XMLHttpRequest",
}


def get_clean_date(movie_dates):
    date = re.search(r'\d{4}-\d{2}-\d{2}',movie_dates[0].strip() if movie_dates else '')
    return date.group() if date else ''

def get_clean_year(movie_years):
    return movie_years[0].strip().replace('(','').replace(')','') if movie_years else ''

def get_total_time(movie_times):
    time = movie_times[0].strip() if movie_times else '0'
    re_h = re.search(r'\d+h',time)
    h = int(re_h.group()[:-1]) if re_h else 0
    re_m = re.search(r'\d+m',time)
    m = int(re_m.group()[:-1]) if re_m else 0
    return h*60 + m

def get_details(movie_full_url):

    if not movie_full_url:
        return None
    movie_response = requests.get(movie_full_url,timeout=(10,30),headers=HEADERS)
    movie_doc = html.fromstring(movie_response.text)
    movie_names = movie_doc.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/a/text()')
    movie_years = movie_doc.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/span/text()')
    movie_dates = movie_doc.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="release"]/text()')
    movie_types = movie_doc.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="genres"]/a/text()')
    movie_scores = movie_doc.xpath('//*[@id="consensus_pill"]/div/div[1]/div/div/@data-percent')
    movie_slogans = movie_doc.xpath('//*[@id="original_header"]/div[2]/section/div[3]/h3[1]/text()')
    movie_directors = movie_doc.xpath('//*[@id="original_header"]/div[2]/section/div[3]/ol/li[1]/p/a/text()')
    movie_actors = movie_doc.xpath('//*[@id="original_header"]/div[2]/section/div[3]/ol/li[2]/p/a/text()')
    movie_times = movie_doc.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="runtime"]/text()')
    print(movie_names)
    print(movie_years)
    print(movie_dates)
    print(movie_types)
    print(movie_scores)
    print(movie_slogans)
    print(movie_directors)
    print(movie_actors)
    print(movie_times)



    return {
        '电影名': movie_names[0].strip() if movie_names else '',
        '上映年份': get_clean_year(movie_years),
        '上映日期': get_clean_date(movie_dates),
        '电影类型': ','.join(movie_types) if movie_types else '',
        '电影评分': movie_scores[0].strip() if movie_scores else '',
        '宣传语': movie_slogans[0].strip() if movie_slogans else '',
        '电影导演': ','.join(movie_directors) if movie_directors else '',
        '电影演员': ','.join(movie_actors) if movie_actors else '',
        '电影时长': get_total_time(movie_times),
    }

def save_details(all_movies):
    with open('./data/01.csv', 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=['电影名','上映年份','上映日期','电影类型','电影评分','宣传语','电影导演','电影演员','电影时长'])
        writer.writeheader()
        writer.writerows(all_movies)

def main():
    all_movies = []
    for i in range(1,6):
        response = requests.get(f'{TOP_MOVIE_URL}?page={i}',timeout=(10,30),headers=HEADERS)
        document = html.fromstring(response.text)
        print(f'初始请求{i}')

        movie_lists = document.xpath('/html/body/div[1]/main/section/div/div/div/div[2]/div[2]/div/section/div/div/div[1]/div/div/div/div[2]/div/a/@href')
        print(movie_lists)
        for movie in movie_lists:
            movie_full_url = BASE_URL + movie
            movie_details = get_details(movie_full_url)
            all_movies.append(movie_details)
            print('电影细节请求')

    save_details(all_movies)
    print('保存文件')


if __name__ == '__main__':
    main()