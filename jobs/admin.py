from django.contrib import admin
from .models import Job, JobApplicant


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_title', 'location', 'min_offer', 'max_offer')
    search_fields = ('job_title', 'location', 'job_description')


@admin.register(JobApplicant)
class JobApplicantAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job', 'applied_date', 'resume')
    list_filter = ('applied_date', 'job')
    search_fields = ('user_username', 'useremail', 'job_job_title')


from django.contrib import admin

# Register your models here.
