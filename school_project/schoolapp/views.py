from django.shortcuts import render,redirect,reverse
from . import forms
from django.contrib.auth.models import User
from schoolapp.forms import UserForm,UserProfileInfoForm,NotificationForm,ResultForm,MarksForm,CheckResultForm,SearchFormbyname,SearchFormbyclass,QuestionForm,AnswerForm,QuizForm,QuizLogin
from schoolapp.models import UserProfileInfo,Notifications,Result,Subjects,CollegeId,Quiz,Questions,Answers,QuizSubjects,QuizUser

#These lot of libraries will help us to login

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
#from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from  django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.views import View
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import random
# Create your views here.

def base(request):
    f=Notifications.objects.all().count()
    return render(request,'base.html',{'f':f})

def user_logout(request):
    logout(request)
    return render(request,'base.html')

def register(request):

    registered=False
    if request.method=="POST":
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            col=[colid for colid in CollegeId.objects.all()]
            cid=[c.cid for c in col]

            if profile_form.cleaned_data["schoolid"] in cid:


                user=user_form.save(commit=False)
                user.set_password(user.password)
                user.save()

                profile=profile_form.save(commit=False)
                profile.user=user

                if 'profile_pic' in request.FILES:
                    profile.profile_pic=request.FILES['profile_pic']

                profile.save()

                registered=True
                instance=CollegeId.objects.get(cid=profile_form.cleaned_data["schoolid"])
                instance.delete()
            else:
                messages.error(request,"SchoolId doesn't match")
                return render(request,'Registration.html',{'userform':user_form,'profile_form':profile_form,'registered':registered})

        else:
            print(user_form.errors,profile_form.errors)
    else:
            user_form=UserForm()
            profile_form=UserProfileInfoForm()


    return render(request,'Registration.html',{'userform':user_form,'profile_form':profile_form,'registered':registered})

def user_login(request):

    if request.method=='POST':
        username=request.POST.get('username')
        password= request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)                                #If user is active then redirect him to the home page
                return render(request,'base.html')

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            return HttpResponse("Invalid Detail supplied")

    else:
        return render(request,'login.html',{})


def notice(request):
    flag=False
    if request.method=="POST":
        notice_form=NotificationForm(data=request.POST)

        if notice_form.is_valid():
             notice=notice_form.save(commit=False)
             notice.save()
             flag=True
        else:
            print(notice_form.errors)
    else:
        notice_form=NotificationForm()
    return render(request,"Notice.html",{'notice_form':notice_form,'flag':flag})

def notifications(request):
    modal=Notifications.objects.all().order_by('-create_date')
    return render(request,'notifications.html',{'modal':modal})

def NoticeDetail(request,pk=None):
    notice=Notifications.objects.get(pk=pk)
    args={'notice':notice}
    return render(request,'NoticeDetail.html',args)



class UploadMarksView(View):
    #We are creating a formset out of the ContactForm
    Marks_FormSet=formset_factory(MarksForm)
    result_form=ResultForm()
    #The Template name where we are going to display it
    template_name="uploadmarks.html"

    #Overiding the get method
    def get(self,request,*args,**kwargs):
        #Creating an Instance of formset and putting it in context dict
        context={
                'marks_form':self.Marks_FormSet(),
                'result_form':self.result_form,
                }

        return render(request,self.template_name,context)
    def post(self,request,*args,**kwargs):

      result_form=ResultForm(self.request.POST)
      if result_form.is_valid():
          result_form.save();
      else:
          messages.error(request,"Roll Number already Exists")
          return render(request,self.template_name,{'marks_form':self.Marks_FormSet(),'result_form':self.result_form})


      marks_formset=self.Marks_FormSet(self.request.POST)

      #Checking the if the form is valid

      if marks_formset.is_valid():
          #To save we have loop through the formset
          for marks in marks_formset:
              #Saving in the contacts models
              if marks.cleaned_data["marks"]<=marks.cleaned_data["max_mark"]:

                  obj=marks.save()
                  obj.rollno=result_form.cleaned_data["rollno"]
                  obj.save()
              else:
                  messages.error(request,"Marks greater than MaximumMarks")
                  return render(request,self.template_name,{'marks_form':self.Marks_FormSet(),'result_form':self.result_form})
          messages.success(request,'Marks Uploaded Successfully')





      else:
          print(marks_formset.errors)

      return render(request,self.template_name,{'marks_form':self.Marks_FormSet(),'result_form':self.result_form})

def CheckResult(request):
    if request.method=='POST':
        checkresultform=CheckResultForm(data=request.POST)

        if checkresultform.is_valid():
            rno=checkresultform.cleaned_data['rollno']
            dob=checkresultform.cleaned_data['dob']
            userdetail=[user for user in Result.objects.all()]
            rollnos=[rn.rollno for rn in userdetail]

            if rno in rollnos:
                data=Result.objects.get(rollno=rno)
                if data.dob==dob:
                    lst=[sub for sub in Subjects.objects.filter(rollno=rno)]
                    totalmarks=0
                    totalmaxmarks=0
                    flag=0
                    flag,totalmarks,totalmaxmarks,percentage=calcsum(lst,rno,totalmarks=0,totalmaxmarks=0,flag=0)
                    return render(request,"getResult.html",{'data':data,'lst':lst,'total':totalmarks,'totalmax':totalmaxmarks,'percent':percentage,'flag':flag})
                else:
                    messages.error(request,"BirthDate is wrong")

                    return render(request,"CheckResult.html",{"checkresult":checkresultform})
            else:
                messages.error(request,"Roll number not found")
                return render(request,"CheckResult.html",{"checkresult":checkresultform})
        else:
            messages.error(checkresultform.errors)
            return render(request,"CheckResult.html",{"checkresult":checkresultform})
    else:
        checkresultform=CheckResultForm()
    return render(request,"CheckResult.html",{"checkresult":checkresultform})
def calcsum(lst,rno,totalmarks=0,totalmaxmarks=0,flag=0):
    for m in lst:
        totalmarks=totalmarks+m.marks
        totalmaxmarks=totalmaxmarks+m.max_mark
        if((m.marks/m.max_mark)*100<40):
            flag=1

    percentage=round(((totalmarks/totalmaxmarks)*100),2)
    data=Result.objects.get(rollno=rno)
    if flag==1:
        flag="Failed"
        data.pf=flag
    else:
        flag="Passed"
        data.pf=flag
    data.save()
    return flag,totalmarks,totalmaxmarks,percentage

class NoticeDeleteView(DeleteView):
    model=Notifications;
    success_url=reverse_lazy('notifications')

def resultlist(request):
    dt=[]
    ash=[1,2,3,4,5]
    searchformbyclass=SearchFormbyclass(data=request.POST)
    searchformbyname=SearchFormbyname(data=request.POST)
    if request.method=="POST" and "sbc" in request.POST:
        if searchformbyclass.is_valid():
                Class=searchformbyclass.cleaned_data["Class"]
                dt=[d for d in Result.objects.filter(std=int(Class))]

        else:
                print(searchformbyname.errors)
    elif request.method=="POST" and "sbn" in request.POST:
        if searchformbyname.is_valid():
                Name=searchformbyname.cleaned_data["Name"]
                dt=[d for d in Result.objects.filter(name__icontains=str(Name))]
        else:
                print(searchformbyname.errors)
    else:
        searchformbyclass=SearchFormbyclass()
        searchformbyname=SearchFormbyname()
    return render(request,"resultlist.html",{"searchformbyclass":searchformbyclass,"searchformbyname":searchformbyname,"data":dt})

def quizpanel(request):
    modal=Quiz.objects.all()
    return render(request,"quizpanel.html",{'quiz':modal})

def addquestions(request,pk):
    if request.method=="POST":
        qform=QuestionForm(data=request.POST)
        aform=AnswerForm(data=request.POST)

        if qform.is_valid() and aform.is_valid():
            ques=qform.save(commit=False)
            q=Quiz.objects.get(pk=pk)
            ques.quiz=q
            ques.save()
            ans=aform.save(commit=False)
            ans.question=ques
            ans.save()
            count=int(q.total_que)
            count=count+1
            q.total_que=count;
            q.save()
            messages.success(request,"Question Uploaded Succesfully")
        else:
            print("Hey")
            print(qform.errors,aform.errors)
    else:
        qform=QuestionForm()
        aform=AnswerForm()

    return render(request,"addQuestions.html",{'qform':qform,'aform':aform})
que_list=[]
marks=dict()
sub=""
def QuizSubject(request):
    global que_list
    global sub
    global marks
    subjects=Quiz.objects.all()
    if request.method=="POST":
        myvar=str(request.POST.get("subjects"))
        sub=myvar
        marks=dict()
        que=Questions.objects.filter(quiz__qname__contains=myvar)
        que_list=[q for q in que]
        que_list=random.sample(que_list,k=3)
        return HttpResponseRedirect(reverse('userlist'))
    return render(request,"QuizSubject.html",{'subjects':subjects})
timer="20"
def userlist(request):
    global marks
    global timer
    ans_list=Answers.objects.all()
    page=request.GET.get('page',1)
    if request.method=='POST':
            queid=str(request.POST.get("queid"))
            myvar=str(request.POST.get("answer"))
            correct=str(request.POST.get("correct"))
            score=str(request.POST.get("score"))
            timer=str(request.POST.get("puttimer"))
            if(myvar==correct):
                marks[queid]=int(score)
            else:
                marks[queid]=0
            print(marks)



    paginator=Paginator(que_list,1)
    try:
        users=paginator.page(page)
    except PageNotAnInteger:
        users=paginator.page(1)
    except EmptyPage:
        users=paginator.page(paginator.num_pages) #last page if page request is empty
    return render(request,"user_list.html",{'users':users,'page':page,'ans_list':ans_list,'timer':timer})

def registerfortest(request):
    registered=False
    if request.method=='POST':
        quizform=QuizForm(data=request.POST)
        if quizform.is_valid():
            quizform.save()
            registered=True
    else:
        quizform=QuizForm()
    return render(request,"registerfortest.html",{'quizform':quizform,'registered':registered})
savepk=""
def starttest(request):
    global savepk
    if request.method=='POST':
        quizloginform=QuizLogin(data=request.POST)
        if quizloginform.is_valid():
            id=quizloginform.cleaned_data["uid"]
            password=quizloginform.cleaned_data["password"]
            userdetail=[user for user in QuizUser.objects.all()]
            uids=[us.uid for us in userdetail]
            if id in uids:
                data=QuizUser.objects.get(uid=id)
                savepk=str(id)
                if data.password==password:
                    return HttpResponseRedirect(reverse('quizsubject'))
                else:
                    messages.error(request,"Password Incorrect")
                    return render(request,"quizlogin.html",{"quizloginform":quizloginform})
            else:
                messages.error(request,"ID Incorrect")
                return render(request,"quizlogin.html",{"quizloginform":quizloginform})

    else:
        quizloginform=QuizLogin()
    return render(request,"quizlogin.html",{"quizloginform":quizloginform})

def testdoneview(request):
    global sub
    global marks
    global savepk
    user=QuizUser.objects.get(uid=savepk)
    sum=0
    for i in marks:
        sum=sum+marks[i];
    qcount=len(marks)
    corrq=[x for x in marks.values() if x!=0]
    corrque=len(corrq)

    subject=QuizSubjects.objects.filter(uid=savepk)
    if(len(subject)==0):
        subject=QuizSubjects(uid=savepk,name=sub,marks=sum,quecount=qcount,attempts=1)
        subject.save()
    else:
        s=[i for i in subject if i.name==sub and i.uid==savepk]
        if(len(s)==1):
            s[0].name=sub
            s[0].marks=sum
            s[0].quecount=qcount
            x=int(s[0].attempts)
            s[0].attempts=x+1
            s[0].save()
        else:
            subject=QuizSubjects(uid=savepk,name=sub,marks=sum,quecount=qcount,attempts=1)
            subject.save()
    marks=dict()
    if(sum>40):
        result="pass"
    else:
        result="fail"
    return render(request,"testdone.html",{'sub':sub,'total':sum,'corrque':corrque,'user':user,'qcount':qcount,'result':result})

def leaderboard(request):
    sub=QuizSubjects.objects.all().order_by('-marks','attempts')
    if request.method=="POST":
        uid=str(request.POST.get("uid"))
        u=QuizUser.objects.get(uid=uid)
        s=QuizSubjects.objects.filter(uid=uid)
        s=[i for i in s]
        return render(request,"rankerdetail.html",{'u':u,'s':s})
    return render(request,"leaderboard.html",{'sub':sub})

def contactus(request):
    return render(request,"contactus.html")












# Create your views here.
