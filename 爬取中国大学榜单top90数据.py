import requests
import csv
from lxml import html

BASE_URL = 'https://www.shanghairanking.cn/rankings/bcur/2026'
HEARDERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def save_details(all_details):
    with open('./data.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['排名','学校名称','英文','称号','省份','类型','总分','办学层次'])
        writer.writeheader()
        writer.writerows(all_details)

def get_details(university):
    ranking = university.xpath('./td[1]/div/text()')
    name_chinese = university.xpath('./td[2]/div/div[2]/div[1]/div/div/span/text()')
    name_english = university.xpath('./td[2]/div/div[2]/div[2]/div/div/span/text()')
    position = university.xpath('./td[2]/div/div[2]/p/text()')
    localtion = university.xpath('./td[3]/text()')
    categories = university.xpath('./td[4]/text()')
    total_grade = university.xpath('./td[5]/text()')
    level = university.xpath('./td[6]/text()')
    return {
        '排名': ranking[0].strip() if ranking else '',
        '学校名称': name_chinese[0].strip() if name_chinese else '',
        '英文': name_english[0].strip() if name_english else '',
        '称号': ','.join(position) if position else '',
        '省份': localtion[0].strip() if localtion else '',
        '类型': categories[0].strip() if categories else '',
        '总分': total_grade[0].strip() if total_grade else '',
        '办学层次': level[0].strip() if level else '',
    }

def main():
    all_details = []
    document = requests.get(BASE_URL, headers=HEARDERS,timeout=(10,30))
    document.encoding ='utf-8'
    response = html.fromstring(document.text)

    universities_list = response.xpath('/html/body/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/table/tbody/tr')

    for university in universities_list:
        details =  get_details(university)
        all_details.append(details)

    save_details(all_details)

if __name__ == '__main__':
    main()