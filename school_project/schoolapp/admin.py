from django.contrib import admin
from schoolapp.models import UserProfileInfo,Subjects,Result,CollegeId,Quiz,Questions,Answers,QuizUser,QuizSubjects,Notifications

admin.site.register(Notifications)
admin.site.register(UserProfileInfo)
admin.site.register(Subjects)
admin.site.register(Result)
admin.site.register(CollegeId)
admin.site.register(Quiz)
admin.site.register(Questions)
admin.site.register(Answers)
admin.site.register(QuizUser)
admin.site.register(QuizSubjects)




# Register your models here.
