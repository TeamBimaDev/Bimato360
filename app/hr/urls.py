from django.urls import path, include

app_name = 'hr'

urlpatterns = [
    path('employee/', include('hr.employee.urls')),
    path('skill/', include('hr.skill.urls')),
    path('skill_category/', include('hr.skill_category.urls')),
    path('job_category/', include('hr.job_category.urls')),
    path('position/', include('hr.position.urls')),
    # path('applicant/', include('hr.applicant.urls')),
    # path('interview/', include('hr.interview.urls')),
    # path('step/', include('hr.step.urls')),
    # path('activitytype/', include('hr.activity_type.urls')),
    # path('activity/', include('hr.activity.urls')),
    # path('applicant_post/', include('hr.applicant_post.urls')),
    # path('refuse/', include('hr.refuse.urls')),

]
