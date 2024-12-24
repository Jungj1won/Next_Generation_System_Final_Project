# crawl/scheduler/artcrawl.py
from article.models import Article
import requests
from bs4 import BeautifulSoup
import time

def articlereg():
    """
    크롤링 함수 (PPT 예시)
    - field_var: 어떤 분야(econ, stat 등)를 긁어올지
    - resultSize_var: 몇 편을 긁어올지
    """
    field_var = 'econ'       # 예: Economics
    resultSize_var = 50      # 한 번에 가져올 논문 수
    url = f"https://arxiv.org/list/{field_var}/recent?skip=0&show={resultSize_var}"

    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        chunks = soup.find_all('div', attrs={'class': 'meta'})
        links = [link['href'] for link in soup.find_all('a', {'title': 'Abstract'})]

        for idx, paper in enumerate(chunks):
            index = links[idx].split('/')[-1]   # arXiv 논문 ID
            link = f"https://arxiv.org/abs/{index}"

            # 주제(subjects), 제목(title), 저자(author) 등 parsing
            subjects_tmp = paper.find('div', {'class': 'list-subjects'}).get_text(strip=True).replace('Subjects:', '')
            title_tmp = paper.find('div', {'class': 'list-title'}).get_text(strip=True).replace('Title:', '')
            author_tmp = paper.find('div', {'class': 'list-authors'}).get_text(strip=True).replace('Authors:', '')

            # 이미 DB에 같은 index(=paper_id) 있으면 저장 X
            if not Article.objects.filter(index=index).exists():
                articleregister = Article(
                    index=index,
                    link=link,
                    title=title_tmp[:200],
                    author=author_tmp[:200],
                    subject1=subjects_tmp[:50],
                )
                articleregister.save()
                time.sleep(0.1)  # 요청 폭주 방지
