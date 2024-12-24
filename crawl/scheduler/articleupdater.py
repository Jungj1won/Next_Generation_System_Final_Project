from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .artcrawl import articlereg

def start():
    """
    APScheduler를 시작하는 함수.
    - cron 설정에 따라 articlereg 함수를 특정 시각/주기로 실행
    """
    scheduler = BackgroundScheduler(timezone="Asia/Seoul")  # 타임존 설정
    # 매주 월요일 15시 30분에 실행, 등 원하는 스케줄 작성
    scheduler.add_job(articlereg, 'cron', day_of_week='mon', hour=15, minute=30)
    
    scheduler.start()
