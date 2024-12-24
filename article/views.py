from django.shortcuts import render
from .models import Article
import requests
from bs4 import BeautifulSoup
import time
from user.models import Member


def articlereg(request):
    field_vars = ['econ', 'stat']  # 주 관심분야와 보조 관심분야
    resultSize_var = 50  # 한 번에 가져올 논문 수

    for field_var in field_vars:
        url = f"https://arxiv.org/list/{field_var}/recent?skip=0&show={resultSize_var}"
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            meta_divs = soup.find_all('div', class_='meta')

            for item in meta_divs:
                title = item.find('div', class_='list-title')
                author = item.find('div', class_='list-authors')
                subject = item.find('div', class_='list-subjects')
                
                title = title.text.replace('Title:', '').strip() if title else ""
                author = author.text.replace('Authors:', '').strip() if author else ""
                subject1 = subject.text.replace('Subjects:', '').strip() if subject else ""

                link_tag = item.find_previous('a', href=True)
                if link_tag:
                    paper_id = link_tag['href'].split('/')[-1]
                    link = f"https://arxiv.org/abs/{paper_id}"
                else:
                    paper_id = None
                    link = None

                if paper_id and not Article.objects.filter(index=paper_id).exists():
                    articleregister = Article(
                        index=paper_id,
                        link=link,
                        title=title[:200],
                        author=author[:200],
                        subject1=subject1[:50],
                    )
                    articleregister.save()
                    time.sleep(0.1)

    return render(request, 'home/index.html')




def subject(request):
    user_id = request.session.get("user", None)
    field = request.GET.get('field', '')  # Fetch selected field from query params
    context = {}

    if user_id:
        try:
            # Fetch user information
            user_info = Member.objects.get(memberID=user_id)
            context['user_id'] = user_id
            context['userinfo'] = user_info

            # If a field is selected, filter articles based on the field
            if field:
                context['articles'] = Article.objects.filter(subject1__icontains=field)
            else:
                # Fetch more articles for the user's primary subject
                context['articles'] = Article.objects.filter(
                    subject1__icontains=user_info.subject1
                )[:20] if user_info.subject1 else []
        except Member.DoesNotExist:
            context['articles'] = []
    else:
        # For non-logged-in users, show generic articles
        context['articles'] = Article.objects.all()[:20]

    return render(request, 'article/subject.html', context)
