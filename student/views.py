from distutils.log import info
from django.shortcuts import redirect, render
from . import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group

# Create your views here.
@login_required(login_url='student_login')
def home(request):
    return render(request,'student_home.html')

def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False



def register(request):
    userForm= forms.StudentForm()
    studentForm=forms.StudentInfoForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentForm(request.POST)
        studentForm=forms.StudentInfoForm(request.POST)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.is_active = True
            user.set_password(user.password)
            user.save()
           
            
            messages.success(request,"Your Student account created Successfully.",extra_tags='stud_login')

            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
            return redirect('student_register')
        
    return render(request,'student_signup.html',context=mydict)

def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if username and password:
            user = auth.authenticate(username=username, password=password)
            exist = User.objects.filter(username=username).exists()
            if exist and user:
                 isfaculty = has_group(user,"PROFESSOR")
                 if isfaculty :
                     messages.error(request,"You are trying to login as student, but you are a faculty")
                     return redirect('student_login')
                 isStudent = has_group(user,"STUDENT")
                 if isStudent:
                     if user.is_active:
                         auth.login(request,user)
                         messages.info(request, f"You are now logged in as {username}.")
                         return redirect('student_home')
                 else:
                     messages.error(request,"Invalid username or password.") 
            else:
                 messages.error(request,"Invalid username or password.") 
        
        else:
            messages.error(request, 'Please fill all fields')
            return render(request, 'student_login.html') 
    return render(request,'student_login.html')
 
    

def logout(request):
   
    auth.logout(request)
    """ messages.success(request,'You are now Logged Out') """
    return redirect('/')

				

				
				
        

    
					 
                    
    


				
				   
			   
    



