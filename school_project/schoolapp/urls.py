from django.conf.urls import url,include
from schoolapp import views

urlpatterns=[
url(r'^register/$',views.register,name='register'),
url(r'^login/$',views.user_login,name='login'),
url(r'^logout/$',views.user_logout,name='logout'),
url(r'^notice/$',views.notice,name='notice'),
url(r'^notifications/$',views.notifications,name='notifications'),
url(r'^notifications/(?P<pk>\d+)/$',views.NoticeDetail,name='noticedetail'),
url(r'^uploadmarks/$',views.UploadMarksView.as_view(),name='uploadmarks'),
url(r'^checkresult/$',views.CheckResult,name='checkresult'),
url(r'^notice/(?P<pk>\d+)/remove/$',views.NoticeDeleteView.as_view(), name='notice_remove'),
url(r'^resultlist/$',views.resultlist,name="resultlist"),
url(r'^addquestions/(?P<pk>\d+)/$',views.addquestions,name='addquestions'),
url(r'^quizpanel/$',views.quizpanel,name='quizpanel'),
url(r'^userlist/$',views.userlist,name='userlist'),
url(r'^registerfortest/$',views.registerfortest,name='registerfortest'),
url(r'^starttesttest/$',views.starttest,name='starttest'),
url(r'^quizsubject/$',views.QuizSubject, name='quizsubject'),
url(r'^testdone/$',views.testdoneview, name='testdone'),
url(r'^leaderboard/$',views.leaderboard, name='leaderboard'),
url(r'^contactus/$',views.contactus,name='contactus'),

#url(r'^uploadmarks/$',views.uploadmarks,name='uploadmarks'),
]
