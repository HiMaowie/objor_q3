# Company Portal (Django)

A simple company portal where admins post job openings and users can apply with a resume upload.

## Features
- Custom User Model (fields: first_name, last_name, username, email, optional phone_number, joined_date, active default True, staff, admin)
- Registration via Django Forms with validations:
  - username unique
  - email unique and must end with @objor.com (e.g., *quiz3@objor.com*)
  - phone number optional; if provided, must be unique
- Jobs app:
  - Admins create job posts *via Django Admin*
  - ListView (FBV) with search across title/description/location
  - DetailView (FBV) requires login; shows:
    - For admins: full job info, applicants table, Edit/Delete buttons
    - For regular users: full job info + Apply (resume upload) form
  - UpdateView & DeleteView are CBVs, admin-only
  - JobApplicant model with FileField for resume and ForeignKey to user and job
- Bootstrap *local only*; no custom CSS; templates use {% extends %}.

## Quickstart

```bash
git clone https://github.com/HiMaowie/objor_q3.git
cd company_portal
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install "Django>=4.2,<5.1"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
