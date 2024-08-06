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
    path('vacation/', include('hr.vacation.urls')),
    path('contract/', include('hr.contract.urls')),
    path('activity_type/', include('hr.activity_type.urls')),
    path('activity/', include('hr.activity.urls')),
    path('question_category/', include('hr.question_category.urls')),
    path('question/', include('hr.question.urls')),
    path('vacancie/', include('hr.vacancie.urls')),
    path('candidat/', include('hr.candidat.urls')),
    path('offer/', include('hr.offer.urls')),
    path('interview_question/', include('hr.interview_question.urls')),
    path('technical_interview/', include('hr.technical_interview.urls')),
    path('Te_interview_question/', include('hr.Te_interview_question.urls')),
]
