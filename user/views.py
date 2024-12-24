from django.shortcuts import render, redirect
from .models import Member
from article.models import Article

# 회원가입 뷰
def register(request):
    if request.method == "GET":
        return render(request, 'register/register.html')

    elif request.method == "POST":
        memberID = request.POST['memberid']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        name = request.POST['username']
        email = request.POST['email']
        subject1 = request.POST.get('subject1', None)
        subject2 = request.POST.get('subject2', None)

        # ID 중복 확인
        try:
            check = Member.objects.get(memberID=memberID)
        except Member.DoesNotExist:
            check = None

        data_dic = {}
        if password1 != password2:
            data_dic['err'] = "비밀번호가 일치하지 않습니다"
        elif check:
            data_dic['err'] = '이미 등록된 아이디입니다.'
        elif not(memberID and password1 and password2 and name and email and subject1):
            data_dic['err'] = "모든 값을 입력해 주세요."
        else:
            memberregister = Member(
                memberID=memberID,
                password=password1,
                name=name,
                email=email,
                subject1=subject1,
                subject2=subject2
            )
            memberregister.save()
            return redirect('index')  # 회원가입 후 메인 페이지로 이동

        return render(request, 'register/register.html', data_dic)

# 로그인 뷰
def login(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')

    elif request.method == 'POST':
        memberID = request.POST['memberid']
        password = request.POST['password']
        try:
            check = Member.objects.get(memberID=memberID)
        except Member.DoesNotExist:
            check = None

        data_dic = {}
        if not(memberID and password):
            data_dic['err'] = '모든 값을 입력해 주세요'
        elif not check:
            data_dic['err'] = '등록된 아이디가 없습니다'
        else:
            if password == check.password:
                request.session['user'] = check.memberID
                return redirect('index')
            else:
                data_dic['err'] = '비밀번호가 잘못되었습니다.'

        return render(request, 'login/login.html', data_dic)

# 로그아웃 뷰
def logout(request):
    request.session.flush()
    return redirect('index')

def index(request):
    user_id = request.session.get("user", None)
    context = {}

    if user_id:
        try:
            # 사용자 정보 가져오기
            user_info = Member.objects.get(memberID=user_id)
            context['user_id'] = user_id
            context['userinfo'] = user_info

            # 주 관심 분야 논문 필터링
            articles_subject1 = Article.objects.filter(
                subject1__icontains=user_info.subject1
            )[:5] if user_info.subject1 else []

            # 보조 관심 분야 논문 필터링
            articles_subject2 = Article.objects.filter(
                subject1__icontains=user_info.subject2
            )[:5] if user_info.subject2 else []

            context['articles_subject1'] = articles_subject1
            context['articles_subject2'] = articles_subject2
        except Member.DoesNotExist:
            context['articles_subject1'] = []
            context['articles_subject2'] = []
    else:
        # 비로그인 상태일 경우
        context['articles_subject1'] = []
        context['articles_subject2'] = []

    return render(request, 'home/index.html', context)
