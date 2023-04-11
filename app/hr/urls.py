from django.urls import path, include

app_name = 'hr'

urlpatterns = [
        path('interview/', include('hr.interview.urls')),
        path('step/', include('hr.step.urls')),
        path('applicant/', include('hr.applicant.urls')),
        path('skill/', include('hr.skill.urls')),
        path('skillcategory/', include('hr.skill_category.urls')),
        path('skilllevel/', include('hr.skill_level.urls')),
        path('activitytype/', include('hr.activity_type.urls')),
        path('activity/', include('hr.activity.urls')),
        path('condidatposte/', include('hr.condidatposte.urls')),
        path('refuse/', include('hr.refuse.urls')),

]
