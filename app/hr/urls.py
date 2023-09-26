from django.urls import path, include

app_name = 'hr'

urlpatterns = [
    path('employee/', include('hr.employee.urls')),
    path('skill/', include('hr.skill.urls')),
    path('skill_category/', include('hr.skill_category.urls')),
    path('job_category/', include('hr.job_category.urls')),
    path('position/', include('hr.position.urls')),
    path('applicant/', include('hr.applicant.urls')),
    path('interview/', include('hr.interview.urls')),
    path('interview_step/', include('hr.interview_step.urls')),
    # path('activity_type/', include('hr.activity_type.urls')),
    # path('activity/', include('hr.activity.urls')),
]
