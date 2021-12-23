from django.contrib import messages
import json
from django.http.response import HttpResponse, JsonResponse
from django.db.models.fields import DateTimeCheckMixin, DateTimeField
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from studentmanagementapp.models import CustomUser, Staff
from studentmanagementapp.models import Courses
from studentmanagementapp.models import Subjects
from studentmanagementapp.models import Students
from django.core.files.storage import FileSystemStorage
from studentmanagementapp.forms import EditStudentForm
from django.urls import reverse
from studentmanagementapp.forms import AddStudentForm
from studentmanagementapp.models import SessionYearModels
from studentmanagementapp.models import Attendance
from studentmanagementapp.models import AttendanceReport

def admin_home(request):
    student_count1 = Students.objects.all().count()
    staff_count = Staff.objects.all().count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()
    student_count_list_in_course=[]
    course_all = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    for course in course_all:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        students = Students.objects.filter(course_id = course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)
    
    subjects_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subjects_all:
        course = Courses.objects.get(id=subject.course_id.id)
        student_count = Students.objects.filter(course_id = course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)



    return render(request,"hod_template/home_content.html",{"student_count":student_count1, "staff_count":staff_count, "subject_count":subject_count, "course_count":course_count, "course_name_list":course_name_list, "subject_count_list":subject_count_list, "student_count_list_in_course":student_count_list_in_course,"student_count_list_in_subject":student_count_list_in_subject,"subject_list":subject_list})

def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method not allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.create_user(username = username, password = password,email = email, last_name = last_name, first_name = first_name, user_type = 2 )
            user.staff.address = address
            user.save()
            messages.success(request,"Successfully added")
            return HttpResponseRedirect(reverse("adcd_staff"))
        except:
            # messages.error(request,"Failed to add staff")
            return HttpResponseRedirect(reverse("add_staff"))

def add_course(request):
     return render(request,"hod_template/add_course_template.html")

def add_course_save(request):
     if request.method!="POST":
        return HttpResponse("Method Not Allowed")
     else:
        course=request.POST.get("course")
        try:
            course_model=Courses(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("add_course"))

def add_student(request):
    form = AddStudentForm()
    return render(request,"hod_template/add_student_template.html",{"form":form})

def add_student_save(request):
     if request.method!="POST":
        return HttpResponse("Method Not Allowed")
     else:
        form=AddStudentForm(request.POST,request.FILES)

        if form.is_valid(): 
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            session_year_id=form.cleaned_data["session_year_id"]
            course_id=form.cleaned_data["course"]
            sex=form.cleaned_data["sex"]

            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)

            # try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
            user.students.address=address
            Course_obj=Courses.objects.get(id=course_id)
            user.students.course_id=Course_obj
            session_year=SessionYearModels.object.get(id=session_year_id)
            user.students.session_year_id=session_year
            user.students.gender=sex
            user.students.profile_pic=profile_pic_url
            user.save()
            messages.success(request,"Successfully Added Student")
            return HttpResponseRedirect(reverse("add_student"))
            # except:
            #     # messages.error(request,"Failed to Add Student")
            #     return HttpResponseRedirect(reverse("add_student"))

def add_subject(request):
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_subject_template.html",{"staffs":staffs,"courses":courses})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2> Method Not Allowed </h2>")
    else: 
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")
        courses=Courses.objects.get(id=course_id)
        staff_id=request.POST.get("staff")
        staff=CustomUser.objects.get(id=staff_id)
       

        try: 
            subject=Subjects(subject_name=subject_name,course_id=courses,staff_id=staff)
            subject.save()

            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except: 
             messages.error(request,"Failed to Add Subject")
             return HttpResponseRedirect(reverse("add_subject"))

def manage_staff(request):
    staffs = Staff.objects.all()
    return render(request,"hod_template/manage_staff_template.html",{"staffs":staffs})

def manage_student(request):
    students= Students.objects.all()
    return render(request,"hod_template/manage_student_template.html",{"students":students})
            
            
def manage_course(request):
    courses=Courses.objects.all()
    return render(request,"hod_template/manage_course_template.html",{"courses":courses})
    
def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request,"hod_template/manage_subject_template.html",{"subjects":subjects})

def edit_staff(request,staff_id): 
    staff=Staff.objects.get(admin=staff_id)

    return render(request,"hod_template/edit_staff_template.html",{"staff":staff,"id":staff_id})

def edit_staff_save(request): 
    if request.method!="POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try: 
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email    
            user.username=username
            user.address=address

            staff_model=Staff.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()

            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

        except:

             messages.error(request,"Failed to Edit Staff")
             return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

def edit_student(request,student_id):
    request.session['student_id'] = student_id
    student = Students.objects.get(admin=student_id)
    form=EditStudentForm()
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['address'].initial=student.address
    form.fields['course'].initial=student.course_id.id
    form.fields['sex'].initial=student.gender
    form.fields['session_year_id'].initial=student.session_year_id.id
    return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.session.get("student_id")
        if student_id==None:
            return HttpResponseRedirect("manage_student")

        form=EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_year_id=form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            sex = form.cleaned_data["sex"]

            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None


            try:
                user=CustomUser.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                student=Students.objects.get(admin=student_id)
                student.address=address
                session_year = SessionYearModels.objects.get(id=session_year_id)
                student.session_year_id = session_year
                student.gender=sex
                course=Courses.objects.get(id=course_id)
                student.course_id=course
                if profile_pic_url!=None:
                    student.profile_pic=profile_pic_url
                student.save()
                del request.session['student_id']
                messages.success(request,"Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=Students.objects.get(admin=student_id)
            return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})



def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id = subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type = 2) 
    return render(request,"hod_template/edit_subject_template.html",{"subject":subject, "staffs":staffs, "courses":courses, "id":subject_id})

def edit_subject_save(request):
    if request.method !="POST":
        return HttpResponse("<h2> Method Not Allowed </h2>")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        staff_id = request.POST.get("staff")
        course_id = request.POST.get("course")

        try:
            subject = Subjects.objects.get(id = subject_id)
            subject.subject_name = subject_name
            staff = CustomUser.objects.get(id = staff_id )
            subject.staff_id = staff
            course = Courses.objects.get(id = course_id)
            subject.course_id = course
            subject.save()
            messages.success(request,"Successfully Edited subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))

        except:
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))

def edit_course(request, course_id):
    course = Courses.objects.get(id = course_id)
    return render(request,"hod_template/edit_course_template.html",{"course":course, "id":course_id})
    

def edit_course_save(request):
    if request.method !="POST":
        return HttpResponse("<h2> Method Not Allowed </h2>")
    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course")

        try:
            course = Courses.objects.get(id = course_id)
            course.course_name = course_name
            course.save()
            messages.success(request,"Successfully Edited course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))

        except:
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))

def manage_session(request):
    return render(request,"hod_template/manage_session_template.html")

def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else: 
       session_start_year=request.POST.get("session_start")
       session_end_year=request.POST.get("session_end")

       try: 
            
        sessionyear=SessionYearModels(session_start_yearmodels=session_start_year,session_end_yearmodels=session_end_year)
        sessionyear.save()
        messages.success(request,"Successfully Added Session")
        return HttpResponseRedirect(reverse("manage_session"))

       except: 
             messages.error(request,"Failed to Add Session")
             return HttpResponseRedirect(reverse("manage_session"))


def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_year_id = SessionYearModels.object.all()
    return render(request,"hod_template/admin_view_attendance.html",{"subjects":subjects, "session_year_id":session_year_id})


@csrf_exempt
def admin_get_attendance_dates(request):
    subject = request.POST.get("subject")
    session_year_id = request.POST.get("session_year_id")
    subject_obj = Subjects.objects.get(id = subject)
    session_year_obj = SessionYearModels.object.get(id = session_year_id)
    attendance = Attendance.objects.filter(subject_id = subject_obj,session_year_id = session_year_obj)
    attendance_obj = []
    for attendance_single in attendance:
        data = {"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")

    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id = attendance )
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)



