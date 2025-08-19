from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView

from .models import Job, JobApplicant
from .forms import JobApplicantForm

# Example queryset/object note as requested:
# Example objects or queryset "objor" and "foo": jobObjor

def job_list(request):
    q = request.GET.get('q', '').strip()
    jobs = Job.objects.all()
    if q:
        jobs = jobs.filter(
            Q(job_title__icontains=q) |
            Q(job_description__icontains=q) |
            Q(location__icontains=q)
        )
    return render(request, 'jobs/jobs_list.html', {'jobs': jobs, 'q': q})


def job_detail(request, pk):
    # Auth required for DetailView
    if not request.user.is_authenticated:
        # Either show unauthorized OR redirect to admin login; we redirect:
        messages.error(request, "You are unauthorized! Please sign in.")
        return redirect('admin:login')

    job = get_object_or_404(Job, pk=pk)
    is_company_admin = getattr(request.user, 'staff', False) or getattr(request.user, 'admin', False) or request.user.is_superuser

    # Regular users get an apply form; admins see applicants table + edit/delete CTAs
    applicant_form = None
    applicants = None
    if is_company_admin:
        applicants = JobApplicant.objects.filter(job=job).select_related('user')
    else:
        applicant_form = JobApplicantForm()

    return render(request, 'jobs/jobs_detail.html', {
        'job': job,
        'is_company_admin': is_company_admin,
        'applicants': applicants,
        'form': applicant_form,
    })


class JobUpdateView(UpdateView):
    model = Job
    fields = ['job_title', 'job_description', 'min_offer', 'max_offer', 'location']
    template_name = 'jobs/jobs_update.html'
    success_url = reverse_lazy('jobs:list')

    def dispatch(self, request, *args, **kwargs):
        # Only company admin can edit
        user = request.user
        if not (user.is_authenticated and (getattr(user, 'staff', False) or getattr(user, 'admin', False) or user.is_superuser)):
            return HttpResponseForbidden("You are unauthorized!")
        return super().dispatch(request, *args, **kwargs)


class JobDeleteView(DeleteView):
    model = Job
    template_name = 'jobs/jobs_confirm_delete.html'
    success_url = reverse_lazy('jobs:list')

    def dispatch(self, request, *args, **kwargs):
        # Only company admin can delete
        user = request.user
        if not (user.is_authenticated and (getattr(user, 'staff', False) or getattr(user, 'admin', False) or user.is_superuser)):
            return HttpResponseForbidden("You are unauthorized!")
        return super().dispatch(request, *args, **kwargs)


@login_required
def apply_view(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    # Company admins should not apply
    if getattr(request.user, 'staff', False) or getattr(request.user, 'admin', False) or request.user.is_superuser:
        messages.error(request, "Company admins cannot apply for jobs.")
        return redirect('jobs:detail', pk=job_id)

    if request.method == 'POST':
        form = JobApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            # Prevent duplicates (unique_together also helps)
            exists = JobApplicant.objects.filter(user=request.user, job=job).exists()
            if exists:
                messages.info(request, "You already applied to this job.")
            else:
                JobApplicant.objects.create(
                    user=request.user,
                    job=job,
                    resume=form.cleaned_data['resume']
                )
                messages.success(request, "Application submitted!")
        else:
            messages.error(request, "Please fix errors in the form.")
    return redirect('jobs:detail', pk=job_id)