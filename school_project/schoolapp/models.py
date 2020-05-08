from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class UserProfileInfo(models.Model):

    DESIG_CHOICE=(
    ('student','Student'),
    ('faculty','Faculty')
    )
    GENDER_CHOICE=(
    ('Male','Male'),
    ('Female','Female')
    )

    user=models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)

    first_name=models.CharField(default="none",max_length=264,blank=False)

    last_name=models.CharField(default="none",max_length=264,blank=False)

    gender=models.CharField(max_length=264,choices=GENDER_CHOICE,default="male")

    mob_no=models.CharField(default="9415127397",max_length=10,blank=False,unique=True)


    designation= models.CharField(max_length=264,choices=DESIG_CHOICE, default='teacher')

    profile_pic=models.ImageField(upload_to='media/profile_pics',blank=True)

    schoolid=models.CharField(max_length=264,blank=False)

    def __str__(self):
        return self.user.username

class Notifications(models.Model):
    title=models.CharField(max_length=264,blank=False)
    text=models.CharField(max_length=264,blank=True)
    author=models.CharField(max_length=264)
    site=models.URLField(blank=True)
    create_date=models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title

class Result(models.Model):
    rollno=models.CharField(max_length=264,blank=False,unique=True)
    name=models.CharField(max_length=264,blank=False)
    std=models.IntegerField(blank=False)
    dob=models.CharField(max_length=264,blank=False)
    pf=models.CharField(max_length=264,default="Failed")


    def __str__(self):
        return self.rollno

class Subjects(models.Model):

    SUB_CHOICE=(
    ('English','English'),
    ('Maths','Maths'),
    ('Hindi','Hindi'),
    ('Science','Science'),
    ('Social Studies','Social Science'),
    ('Art','Art'),
    ('Sanskrit','Sanskrit')
    )
    MAXIMUM_MARKS=(
    (20,20),
    (50,50),
    (100,100)
    )
    subject=models.CharField(max_length=264,choices=SUB_CHOICE,default="Hindi")
    marks=models.IntegerField(blank=False)
    max_mark=models.IntegerField(choices=MAXIMUM_MARKS)
    rollno=models.CharField(max_length=264)

    def __str__(self):
        return self.subject

class CollegeId(models.Model):
    cid=models.CharField(max_length=264,blank=False)

    def __str__(self):
        return self.cid

class Quiz(models.Model):
    qid=models.CharField(max_length=20,unique=True)
    qname=models.CharField(max_length=264)
    total_que=models.IntegerField(default=0)

    def __str__(self):
        return self.qname
class Questions(models.Model):
    quiz=models.ForeignKey(Quiz,related_name="quiz",on_delete=models.CASCADE)
    queid=models.CharField(max_length=20,unique=True)
    quename=models.CharField(max_length=264)
    marks=models.IntegerField(default=0)

    def __str__(self):
        return self.quename

class Answers(models.Model):
    ANSWER_CHOICE=(
    ('1','Option1'),
    ('2','Option2'),
    ('3','Option3'),
    ('4','Option4'),
    )
    question=models.ForeignKey(Questions,related_name="question",on_delete=models.CASCADE)
    option1=models.CharField(max_length=100)
    option2=models.CharField(max_length=100)
    option3=models.CharField(max_length=100)
    option4=models.CharField(max_length=100,default="None")
    answer=models.CharField(max_length=100,choices=ANSWER_CHOICE,default="Option1")


class QuizUser(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    uname=models.CharField(max_length=264)
    clas=models.CharField(max_length=100,default=None)
    password=models.CharField(max_length=100,default="kcs")
    emailid=models.CharField(max_length=264)


    def __str__(self):
        return self.uname
class QuizSubjects(models.Model):
    name=models.CharField(max_length=100)
    quecount=models.IntegerField(default=0)
    max_marks=models.IntegerField(default=0)
    marks=models.IntegerField(default=0)
    attempts=models.IntegerField(default=0)
    uid=models.CharField(max_length=100)


    def __str__(self):
        return self.name
