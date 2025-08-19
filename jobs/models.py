from django.db import models
from django.conf import settings


# Example email exactly as required:
# Example: quiz3@objor.com

class Job(models.Model):
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    min_offer = models.DecimalField(max_digits=10, decimal_places=2)
    max_offer = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)

    def _str_(self):
        return self.job_title


class JobApplicant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    applied_date = models.DateTimeField(auto_now_add=True)
    resume = models.FileField(upload_to='resumes/')  # no renaming required

    class Meta:
        unique_together = ('user', 'job')  # prevent duplicate applies

    def _str_(self):
        return f"{self.user} -> {self.job}"


from django.db import models

# Create your models here.
