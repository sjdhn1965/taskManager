import sys
sys.path


from django.http import HttpResponse
import requests
import bcrypt
from .values import dbvalues

from django.contrib import messages
from django.shortcuts import render
from Post_Project.forms import Loginform
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import mysql.connector as db
from datetime import datetime
from datetime import timedelta
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import logout as auth_logout

global user, firstname, accomplished_message
dv = dbvalues.setValues()
print('dv ',dv)

def setcookies(request):
    response = HttpResponse("Cookies set")
    response.set_cookie("mycookie",max_age=87878)
    response.set_cookie('java-tutorial', 'javatpoint.com') 
    response.set_cookie('python-tutorial', 'pythontpoint.com') 
    return response

def getcookies(request):  
    tutorial  = request.COOKIES['java-tutorial']  
    tutorial = request.COOKIES['python-tutorial']
    return HttpResponse("java tutorials @: "+ tutorial  );  




def taskpage(request):

    
    # print("Session of {}".format(request.session['user']))
    return render(request, "taskdisplay.html", {"user": "Welcome " + request.session["email"]})


def submit__signup_form(request):
    messages.info(request, "Sign up here!")
    if request.method == 'POST':
        # connect to database
        
        
        mydb = db.connect(host=dv['dbHost'],user=dv['dbUsername'],
                      passwd=dv['dbPassword'], database=dv['dbName'],port=dv['dbPort'])
        print(mydb)
        cursor = mydb.cursor()

        email = request.POST.get("email")
    # To check if user already exists!

        sql = "SELECT email FROM users WHERE email = %s"
        data = email
        print(sql)

        cursor.execute(sql, (data,))
        result = cursor.fetchone()

       # for fetcheduser in result:
        print(result)

        if result:
            messages.info(request, "Acheiver already registered!")
            return render(request, "signup_page.html")

        else:

            firstname = request.POST.get("firstname")

            email = request.POST.get("email")
            password = request.POST.get("password")
            print(password)
            # encrpt the password

            b = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(
                b, bcrypt.gensalt()).decode('utf-8')

            print(hashed_password)

            datecreated = datetime.now()

            sql = ("INSERT INTO users"
                   "(firstname,email,password,datecreated) "
                   "VALUES (%s,%s,%s,%s)")
            table1 = 'users'
            data = (firstname, email, hashed_password, datecreated)
            print(data)

            cursor.execute(sql, data)

            mydb.commit()

            mydb.close()
            request.session['firstname'] = firstname
            user =  request.session["firstname"]
            request.session['email'] = email
            return render(request, "taskdisplay.html")

    return render(request, "signup_page.html")


def login_form(request):

   
    #form = Loginform()
    if request.method == 'POST':
        # #form = Loginform(request.POST or None)
        # if not form.is_valid():
        #     # print userform.errors
        #    # message = form.errors
        #     #return render(request, "login_page.html", {'form': form, 'message': message})
        
          
        # else:
        #     # connect to database
            mydb = db.connect(host=dv['dbHost'],user=dv['dbUsername'],passwd=dv['dbPassword'], database=dv['dbName'])
                              
                      
            cursor = mydb.cursor()

            email = request.POST["email"]
            password = request.POST["password"]
            # email = form.cleaned_data.get("email")
            # password = form.cleaned_data.get("password")
              

            sql = "SELECT firstname,email,password FROM users WHERE email = %s"
            print(f'email:', email)
            data = (email)
            cursor.execute(sql, (data,))
            result = cursor.fetchone()

            if result is not None:
                pass
                if bcrypt.checkpw(password.encode('utf-8'), result[2].encode('utf-8')):
                    print("my password", password.encode('utf-8'))
                    print("my db password", result[2].encode('utf-8'))
                    print("logged in")
                    request.session["firstname"] = result[0]
                    request.session["email"] = result[1]
                    user =  request.session["firstname"]
                    return redirect("/task/")

                else:
                    messages.warning(request, "Invalid Secret Key!")
                    #return render(request, "login_page.html", {'form': form, 'message': message})
                    return render(request, "login_page.html")
            else:
                messages.warning(request, "Acheiver email is Invalid!")
               # return render(request, "login_page.html", {'form': form, 'message': message})
                return render(request, "login_page.html")

    #else:
        #return render(request, "login_page.html", {'form': form, 'message': message})
    return render(request, "login_page.html")



def taskform(request):

    if not 'email' in request.session:
         return redirect("/login/")
    
    
       

    data = []

    if 'AddTask' in request.POST:

        task = request.POST["task1"]
        dt = datetime.today()
        email = request.session["email"]
        status = 0
        print("from inside taskform ", task, dt, email)
    # Add task to table *task
         
        mydb = db.connect(host=dv['dbHost'],user=dv['dbUsername'],
                      passwd=dv['dbPassword'], database=dv['dbName'])
        
        cursor = mydb.cursor()
        sql = ("INSERT INTO task"
               "(email,task,datecreated,status) "
               "VALUES (%s,%s,%s,%s)")
        table1 = 'task'
        Insertdata = (email, task, dt, 0)

        cursor.execute(sql, Insertdata)
        mydb.commit()
        mydb.close()
        return redirect('/task/')
    else:
        return render(request, "base.html")


def updateform(request):

    pass
######## VIEW tasks  - COMPLETED or INCOMPLETED 

def viewtask(request):
    if 'email' in request.session:
        print("inside of function task")
    else:
        return redirect("/login/")

    data = []
    
    email = request.session["email"]
    print("email", email)

    status = int(request.POST["status"])
    if status == 1:
        status = 0
    else:
        status = 1

    print('status from viewtask', status)

    # view task to table *task
   
    mydb = db.connect(host=dv['dbHost'],user=dv['dbUsername'],
                      passwd=dv['dbPassword'], database=dv['dbName'])
    sql = ("SELECT email,task,datecreated,status,id FROM task where email=%s AND status =%s")
    cursor = mydb.cursor()
    cursor.execute(sql, (email, status))
    result = cursor.fetchall()
    if result is None:
        pass
    else:
        for result in result:
            dt = result[2]
            print(dt)
            date_format = '%Y-%m-%d %H:%M:%S.%f'
  # Format of the input date string
            # date_format = '%d/%m/%Y'    # Desired output format

            parsed_date = datetime.strptime(result[2], date_format)
            # formatted_date = parsed_date.strftime(output_format)
            
            # Output: '15/02/2010'
            # dt = result[2].strptime('%a %d,%Y')

            # # 15 days added to date on > goal set date to check if the time is left today for task
            #  #  and display a message appropirately
            formatted_date = parsed_date.strftime('%b-%d-%Y') 
            print(formatted_date)
            deadlinedate = parsed_date + timedelta(days=3)
            print('timeleft ' ,deadlinedate)
               
            todaysdate = datetime.now()
            # print('timeleft:' ,timeLeft,'timeover:',timeover )
            if  result[3] == 1:
                                    
             accomplished_message = "Great Job!"
            elif result[3] == 0:
             if deadlinedate < todaysdate:
                accomplished_message = "Alert! Deadline Passed - Take Action"
             else:
                 accomplished_message = "task pending - Take Action soon"
            
            onetask = {'task': result[1], 'dt': formatted_date,
                       'status': result[3], 'taskid': result[4], 'task_message': accomplished_message}
            
           
            data.append(onetask)

    mydb.close

    context = {'context': data}
    print('context:',context)
    #html = render_to_string("viewdata.html", context=context,request=request)
    
   
    
    
     
    return JsonResponse(context)
    


def movetask(request):
    if 'email' in request.session:
        pass
    else:
        return redirect("/login/")

    print("inside of movetask")
    data = []
    taskid = request.POST.get("id")
    email = request.session["email"]
    status = int(request.POST.get("status"))
    print("status from movetask", status)
    print(type(status))
    taskid = int(taskid)
    print(taskid)
    print(type(taskid))

    sql = "UPDATE task SET status = %s where id = %s"
    deldata = (status, taskid)
    print('deldata', deldata)
     
    mydb = db.connect(host=dv['dbHost'],user=dv['dbUsername'],
                      passwd=dv['dbPassword'], database=dv['dbName'])
    cursor = mydb.cursor()
    cursor.execute(sql, deldata)
    mydb.commit()

    mydb.close

    return viewtask(request)


def logout(request):
    if "firstname" in request.session:
        del request.session["firstname"]
    
    if "email" in request.session:
        del request.session["email"]
    
    request.session.clear()
    
    return redirect('/login/')
    #return JsonResponse({'form': 'success'})

 
 

    

   

    
