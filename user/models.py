from django.db import models

# Create your models here.
class Member(models.Model):    
    memberID = models.CharField(max_length=15, verbose_name='아이디')
    password = models.CharField(max_length=15, verbose_name='비밀번호')   
    name = models.CharField(max_length=30, verbose_name='사용자명')    
    email = models.EmailField(max_length=30, verbose_name='이메일')    
    subject1 = models.CharField(max_length=1000, verbose_name='주제1',null =True)    
    subject2 = models.CharField(max_length=1000, verbose_name='주제2', null =True)    
    register_dttm = models.DateTimeField(auto_now_add=True, verbose_name='회원가입일자')    

    class Meta:       
        db_table = 'MEMBER'
