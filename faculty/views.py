import csv
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import logout
from careers.models import JobPost
from events.models import Event
from events.forms import EventForm
from authentication.models import User, Course
import random
import string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from .models import WebsiteSettings, Official

def generate_student_number():
    while True:
        years = [f"{i:04d}" for i in range(0, 9999)]
        year = random.choice(years)
        unique_number = str(random.randint(1, 99999)).zfill(5)
        suffix = ''.join(random.choices(string.ascii_uppercase, k=2))
        random_digits = str(random.randint(0, 9)).zfill(1)

        student_number = f"{year}.{unique_number}.{suffix}.{random_digits}"

        if not User.objects.filter(student_number=student_number).exists():
            return student_number


@login_required(login_url='/faculty/')
def faculty_dashboard(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))  # Check if message exists

        return redirect(reverse('authentication:faculty'))
    
    context = {
        'active_page':'dashboard',
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }

    return render(request, 'faculty_dashboard.html', context)
    

def faculty_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('/faculty') 

@login_required(login_url='/faculty/')
def alumni_management(request):\
    
    courses = Course.objects.all()

    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))  # Check if message exists

        return redirect(reverse('authentication:faculty'))

    context = {
        'active_page':'alumni',
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'courses': courses
    }

    return render(request, 'faculty/alumni_management.html', context)

@login_required(login_url='/faculty/')
def alumni_view(request, id):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    alumni = get_object_or_404(User, id=id)

    context = {
        "alumni": alumni
    }
    return render(request, 'faculty/alumni_view.html', context)

@login_required(login_url='/faculty/')
def careers_management(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))
        return redirect(reverse('authentication:faculty'))

    context = {
        'active_page':'careers',
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    return render(request, 'faculty/careers_management.html', context)

@login_required(login_url='/faculty/')
def careers_edit(request, id):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    try:
        job_post = JobPost.objects.get(id=id)
    except JobPost.DoesNotExist:
        messages.error(request, "Job post not found.")
        return redirect(reverse('faculty:careers_management'))
    
    if request.method == 'POST':
        job_post.title = request.POST['title']
        job_post.company = request.POST['company']
        job_post.location = request.POST['location']
        job_post.job_type = request.POST['job_type']
        job_post.description = request.POST['description']
        job_post.responsibilities = request.POST['responsibilities']
        job_post.qualifications = request.POST['qualifications']
        job_post.benefits = request.POST['benefits']
        job_post.salary = request.POST['salary']
        job_post.is_active = 'is_active' in request.POST
        job_post.save()
        messages.success(request, "Job post updated successfully.")
        return redirect(reverse('faculty:career_edit', kwargs={'id': id}))
    
    context = {
        'job_post': job_post,
    }
    return render(request, 'faculty/careers_edit.html', context)

@login_required(login_url='/faculty/')
def careers_view(request, id):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    try:
        job_post = JobPost.objects.get(id=id)
    except JobPost.DoesNotExist:
        messages.error(request, "Job post not found.")
        return redirect(reverse('faculty:careers_management'))
    
    # Dictionary to map job type abbreviations to full labels
    job_type_labels = {
        'FT': 'Full-Time',
        'PT': 'Part-Time',
        'CT': 'Contract',
        'IN': 'Internship',
        # Add other job types here
    }
    
    # Add full job type label to job post
    job_post_with_label = {
        'id': job_post.id,
        'date_posted': job_post.created_at,
        'location': job_post.location,
        'is_active': job_post.is_active,
        'title': job_post.title,
        'company': job_post.company,
        'description': job_post.description,
        'responsibilities': job_post.responsibilities,
        'qualifications': job_post.qualifications,
        'benefits': job_post.benefits,
        'job_type_label': job_type_labels.get(job_post.job_type, job_post.job_type),
        # Add other fields as needed
    }
    
    context = {
        'job_post': job_post_with_label,
    }
    return render(request, 'faculty/careers_view.html', context)

@login_required(login_url='/faculty/')
def events_management(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    context = {
        'active_page':'events',
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    return render(request, 'faculty/events_management.html', context)

@login_required(login_url='/faculty/')
def events_add(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event added successfully.")
            return redirect(reverse('faculty:events_management'))
    else:
        form = EventForm()
    
    context = {
        'form': form,
    }
    return render(request, 'faculty/events_add.html', context)

@login_required(login_url='/faculty/')
def events_edit(request, slug):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    event = get_object_or_404(Event, slug=slug)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect(reverse('faculty:events_edit', kwargs={'slug': slug}))
    else:
        form = EventForm(instance=event)
    
    context = {
        'event': event,
        'form': form,
    }
    return render(request, 'faculty/events_edit.html', context)

@login_required(login_url='/faculty/')
def articles_management(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    context = {
        'active_page':'articles',
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    return render(request, 'faculty/articles_management.html', context)

@login_required(login_url='/faculty/')
def story_management(request):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    context = {
        'active_page':'alumni_stories',
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    return render(request, 'faculty/story_management.html', context)

@login_required(login_url='/faculty/')
def alumni_import(request):
    if not request.user.is_staff or not request.user.is_active:
        return JsonResponse({
            'success': False,
            'message': "Access denied. You must be an active faculty member to proceed."
        }, status=403)

    if request.method == 'POST':
        # Expect a JSON payload with row data
        try:
            # If sent as form data with 'data' key containing JSON string
            data_json = request.POST.get('data')
            if not data_json:
                return JsonResponse({'success': False, 'message': 'No data provided'}, status=400)

            row = json.loads(data_json)

            # Validate required keys exist in row dictionary
            required_keys = ['Student Number', 'Email Address', 'Course Code', 'First Name', 'Last Name']
            for key in required_keys:
                if key not in row:
                    return JsonResponse({'success': False, 'message': f"Missing required field: {key}"}, status=400)

            # Handle Student Number generation
            student_number = row.get('Student Number')
            if not student_number:
                student_number = generate_student_number()

            # Check duplicates
            if User.objects.filter(email=row['Email Address']).exists():
                return JsonResponse({'success': False, 'message': f"Email {row['Email Address']} already exists."}, status=409)

            if User.objects.filter(student_number=student_number).exists():
                return JsonResponse({'success': False, 'message': f"Student number {student_number} already exists."}, status=409)

            # Get course
            try:
                course = Course.objects.get(course_code=row['Course Code'])
            except Course.DoesNotExist:
                return JsonResponse({'success': False, 'message': f"Course code '{row['Course Code']}' not found."}, status=400)

            # Format birthday and start date
            def format_date(value):
                if not value:
                    return None
                # Try to parse if string or date format expected
                return value  # adjust if needed

            birthday = format_date(row.get('Birthday'))
            start_date = format_date(row.get('Start Date'))

            work_exp = [{
                "company": row.get('Company', ''),
                "position": row.get('Position', ''),
                "startDate": start_date,
                "endDate": None
            }]

            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            user = User.objects.create(
                first_name=row.get('First Name', ''),
                middle_name=row.get('Middle Name', ''),
                last_name=row.get('Last Name', ''),
                student_number=student_number,
                suffix=row.get('Suffix', ''),
                email=row.get('Email Address', ''),
                birthday=birthday,
                mobile=row.get('Mobile Number', ''),
                civil_status=row.get('Civil Status', ''),
                sex=row.get('Sex', ''),
                course=course,
                school_year=row.get('School Year', ''),
                work_experience=work_exp
            )
            user.set_password(password)
            user.save()

            try:
                send_email_import_user(user, password)
            except Exception as e:
                # User created but email failed, return warning
                return JsonResponse({'success': True, 'warning': f"User created but email sending failed: {str(e)}"})

            return JsonResponse({
                'success': True,
                'message': "User imported successfully.",
                'student_number': student_number,
                'email': row.get('Email Address', '')
            })

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': "Invalid JSON format."}, status=400)

        except Exception as e:
            return JsonResponse({'success': False, 'message': f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({'success': False, 'message': "Invalid request method."}, status=405)

@login_required(login_url='/faculty/')
def alumni_export(request):
    if not request.user.is_staff or not request.user.is_active:
        return JsonResponse({
            'success': False,
            'message': "Access denied. You must be an active faculty member to proceed."
        }, status=403)

    if request.method == 'POST':
        try:
            data_json = request.POST.get('data')

            print(data_json)

            if not data_json:
                return JsonResponse({'success': False, 'message': "No data provided."}, status=400)

            data = json.loads(data_json)
            selected_fields = data.get('fields', [])
            selected_year = data.get('school_year')
            selected_course = data.get('course')

            # Validate selected fields
            model_fields = {
                'name': ['last_name', 'first_name', 'middle_name', 'suffix'],
                'birthday': 'birthday',
                'address': 'address',
                'telephone': 'telephone',
                'mobile': 'mobile',
                'email': 'email',
                'civil_status': 'civil_status',
                'sex': 'sex',
                'school_year': 'school_year',
                'course': 'course',
                'employment': 'jobs',  # assuming jobs is a JSONField
            }

            queryset = User.objects.all()

            if 'school_year' in selected_fields:
                if selected_year:
                    queryset = queryset.filter(school_year=selected_year)
            if 'course' in selected_fields:
                if selected_course:
                    queryset = queryset.filter(course=selected_course)


            # Prepare response
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="alumni_export.csv"'
            writer = csv.writer(response)

            # Header
            header = []
            for field in selected_fields:
                if field == 'name':
                    header.extend(['Last Name', 'First Name', 'Middle Name', 'Suffix'])
                else:
                    header.append(field.replace('_', ' ').title())
            writer.writerow(header)

            # Data rows
            for user in queryset:
                row = []
                for field in selected_fields:
                    if field == 'name':
                        row.extend([user.last_name, user.first_name, user.middle_name or '', user.suffix or ''])
                    elif field == 'course':
                        row.append(user.course.course_code if user.course else '')
                        row.append(user.course.course_name if user.course else '')
                    elif field == 'employment':
                        # This can be expanded depending on how you want to export JSONField data
                        jobs = user.jobs
                        row.append(", ".join([job.get('position', '') for job in jobs]) if jobs else '')
                    else:
                        value = getattr(user, model_fields[field], '')
                        row.append(value if value is not None else '')
                writer.writerow(row)

            return response
        
        except Exception as e:
                import traceback
                traceback.print_exc()  # For console
                return JsonResponse({'success': False, 'message': f"Error: {str(e)}"}, status=500)

        except Exception as e:
            return JsonResponse({'success': False, 'message': f"Error: {str(e)}"}, status=500)

    return JsonResponse({'success': False, 'message': "Invalid request method."}, status=405)

def send_email_import_user(user, password):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = f"{settings.DOMAIN_URL}/verify-email/{uid}/{token}/"

    subject = 'Verify your Alumni Portal account'
    message = f'Hi {user.email},\n\nPlease click the link below to verify your account:\n\n{verification_url}\nYour temporary password is: {password}\n\nThank you!'
    
    send_mail(
    subject,
    message,
    settings.DEFAULT_FROM_EMAIL,
    [user.email],
    fail_silently=False,
    )

@login_required(login_url='/faculty/')
def system_settings(request):

    websettings = WebsiteSettings.objects.first()

    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    context = {
        'active_page':'settings',
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'settings':websettings
    }
    return render(request, 'system_settings.html', context)

@login_required(login_url='/faculty/')
def officials_management(request):

    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        # Debug: Print stored messages before redirecting
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))

        return redirect(reverse('authentication:faculty'))
    
    context = {
        'active_page':'officials',
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    return render(request, 'officials_management.html', context)

@login_required(login_url='/faculty/')
def handle_officials_form(request):

    official = Official.objects.first()

    if request.method == 'POST':
        print(request.POST)
        director_name = request.POST.get('director_name')
        director_photo = request.FILES.get('director_photo')

        return JsonResponse({'message': 'Success'})

    return JsonResponse({'error': 'Invalid request'}, status=400)