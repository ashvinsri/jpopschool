from django import forms
from django.contrib.auth.models import User
from schoolapp.models import UserProfileInfo,Notifications,Result,Subjects,Questions,Answers,QuizUser

class UserProfileInfoForm(forms.ModelForm):
    first_name=forms.CharField(widget=forms.TextInput(
    attrs={'class':'form-control','placeholder':'Enter FirstName'}),required=True)
    last_name=forms.CharField(widget=forms.TextInput(
    attrs={'class':'form-control','placeholder':'Enter LastName'}),required=True)
    mob_no=forms.RegexField(regex=r"^\d{10}$")
    class Meta():
        model=UserProfileInfo
        fields=('first_name','last_name','gender','mob_no','profile_pic','schoolid')



class UserForm(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(
    attrs={'class':'form-control','placeholder':'Enter the username'}),required=True,max_length=80)
    email=forms.CharField(widget=forms.EmailInput(
    attrs={'class':'form-control','placeholder':'Enter the EmailId'}),required=True,max_length=80)
    password=forms.CharField(widget=forms.PasswordInput(
    attrs={'class':'form-control','placeholder':'Enter the username'}),required=True,max_length=80)



    class Meta():
        model=User
        fields=['username','email','password']

class NotificationForm(forms.ModelForm):
    title=forms.CharField(widget=forms.TextInput(
    attrs={'class':'form-control','placeholder':'Enter Title'}),required=True)
    text=forms.CharField(widget=forms.TextInput(
    attrs={'class':'form-control','placeholder':'Enter Notice'}),required=True)
    author=forms.CharField(widget=forms.TextInput(
    attrs={'class':'form-control','placeholder':'Author'}),required=True)
    site=forms.CharField(widget=forms.URLInput(
    attrs={'class':'form-control','placeholder':'URL'}),required=True)


    class Meta():
        model=Notifications
        fields=['title','text','author','site']

class ResultForm(forms.ModelForm):
        rollno=forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Enter RollNo'}),required=True)
        name=forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Enter Name'}),required=True)
        std=forms.IntegerField(widget=forms.NumberInput(
        attrs={'class':'form-control','placeholder':'Enter Your Standard'}),required=True)
        dob=forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Date of Birth'}),required=True)
        class Meta():
            model=Result
            fields=['rollno','name','std','dob']

class MarksForm(forms.ModelForm):
        class Meta():
            model=Subjects
            fields=['subject','marks','max_mark']

class CheckResultForm(forms.Form):
    rollno=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Roll Number','size':40}),required=True)
    dob=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter DOB','size':40}),required=True)

class SearchFormbyclass(forms.Form):
    Class=forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Enter Class",'size':20}))
class SearchFormbyname(forms.Form):
    Name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Enter name of student",'size':20}))

class QuestionForm(forms.ModelForm):
    class Meta():
        model=Questions
        fields=['queid','quename','marks']
class AnswerForm(forms.ModelForm):
    class Meta():
        model=Answers
        fields=['option1','option2','option3','option4','answer']
class QuizForm(forms.ModelForm):
    uid=forms.CharField(label="UserId",widget=forms.TextInput(
    attrs={'class':'form-control','placeholder':'Enter Username'}),required=True)
    uname=forms.CharField(label="Username",widget=forms.TextInput(
    attrs={'class':'form-control','placeholder':'Enter Full Name'}),required=True)
    emailid=forms.CharField(label="Class",widget=forms.EmailInput(
    attrs={'class':'form-control','placeholder':'Enter mail ID'}),required=True)
    clas=forms.CharField(label="Class",widget=forms.TextInput(
    attrs={'class':'form-control','placeholder':'Class'}),required=True)
    password=forms.CharField(widget=forms.PasswordInput(
    attrs={'class':'form-control','placeholder':'Password'}),required=True)
    confirm_password=forms.CharField(widget=forms.PasswordInput(
    attrs={'class':'form-control','placeholder':'Enter Password again'}),required=True)

    class Meta():
        model=QuizUser
        fields=['uid','uname','emailid','clas','password']
    def clean(self):
        cleaned_data=super(QuizForm,self).clean()
        password=cleaned_data.get("password")
        confirm_password=cleaned_data.get("confirm_password")

        if password!=confirm_password:
            raise forms.ValidationError(
            "Password and Confirm Password don't match"
            )

class QuizLogin(forms.Form):
        uid=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter User Id','size':40}),required=True)
        password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password','size':40}),required=True)
