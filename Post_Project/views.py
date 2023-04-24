from django.http import HttpResponse
import requests

from django.shortcuts import render
from Post_Project.forms import Loginform
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import mysql.connector as db
from datetime import datetime
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import logout as auth_logout

global user


def taskpage(request):

    # print("Session of {}".format(request.session['user']))
     return render(request, "taskdisplay.html", {"user": "Welcome " + request.session["user"]})


def submit__signup_form(request):
    message = "Sign up here!" 
    if request.method == 'POST':
        # connect to database
        mydb = db.connect(host="localhost", user="root",
                          passwd="bismi7867", database="members")
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
            message = "User already exists!"
            return render(request, "signup_page.html", {'message':message})

        else:

            fname = request.POST.get("firstname")

            email = request.POST.get("email")
            password = request.POST.get("password")
            datecreated = datetime.now()

            sql = ("INSERT INTO users"
                   "(firstname,email,password,datetcreated) "
                   "VALUES (%s,%s,%s,%s)")
            table1 = 'users'
            data = (fname, email, password, datecreated)
            print(data)

            cursor.execute(sql, data)

            mydb.commit()
            
            mydb.close()

            request.session['user'] = email
            user = request.session['user']
            # return HttpResponseRedirect("/taskpage")
            return render(request, "taskdisplay.html", {'user': user})

    return render(request, "signup_page.html", {'action': 'Sign UP!'})


def login_form(request):
    message = "Login here!"
    if request.method == 'POST':
        
        # connect to database
        mydb = db.connect(host="localhost", user="root",
                          passwd="bismi7867", database="members")
        cursor = mydb.cursor()

        email = request.POST["email"]
        password = request.POST["password"]
        sql = "SELECT email,password FROM users WHERE email = %s"
        print(f'email:', email)
        data = (email)
        cursor.execute(sql, (data,))
        result = cursor.fetchone()

        if result is not None:
            pass
            if result[1] == password:
                print("logged in")
                request.session["user"] = email
                user = request.session["user"]

                # return render(request, "blogpost_page.html", {'email':request.session["email"]})
                return redirect("/task/")
                # return render(request, "blogpost_page.html", {'email':request.session["email"]})
            else:
                message = "Invalid password!"
        else:
            message = "Invalid username!"
    userform = Loginform()
    return render(request, "login_page.html", {'form': userform,'message':message})


def taskform(request):
    
    if 'user' in request.session:
        
        print("inside of function task")
    else:
       return redirect("/login/")

    data = []

    if 'AddTask' in request.POST:
        
        task = request.POST["task1"]
        dt = datetime.today()
        email = request.session["user"]
        status = 0
        print ("from inside taskform ",task,dt,email)
     # Add task to table *task
        mydb = db.connect(host="localhost", user="root",
                          passwd="bismi7867", database="members")
        cursor = mydb.cursor()
        sql = ("INSERT INTO task"
                   "(email,task,datecreated,status1) "
                   "VALUES (%s,%s,%s,%s)")
        table1 = 'task'
        Insertdata = (email, task, dt, False)

        cursor.execute(sql, Insertdata)
        mydb.commit()
        mydb.close()

    
    user = request.session["user"]
    return render(request, "taskdisplay.html", {'user': user})


def updateform(request):

    pass


def viewtask(request):
        if 'user' in request.session:
                print("inside of function task")
        else:
                return redirect("/login/")

        data = []

        email = request.session["user"]
        print("email", email)

        status = int(request.POST["status"])
        if status == 1:
         status = 0
        else:
         status=1
        
        print('status from viewtask', status)
                       
        #view task to table *task
        mydb = db.connect(host="localhost", user="root",
                            passwd="bismi7867", database="members")
        sql = ("SELECT email,task,datecreated,status1,taskid FROM task where email=%s AND status1 =%s")
        cursor = mydb.cursor()
        cursor.execute(sql, (email,status))
        result = cursor.fetchall()
        if result is None:
                pass
        else:
                for result in result:
                    dt = result[2].strftime('%a %d,%Y')
                    onetask = {'task':result[1],'dt':dt,'status':result[3],'taskid':result[4]}
                    
                    data.append(onetask)
                    

        mydb.close
        
        context = {'context':data}
              
        html = render_to_string( "viewdata.html", context)
           
        return JsonResponse(html, safe=False)
            #return render(request, "taskdisplay.html",context=context)
        
   

def movetask(request):
    if 'user' in request.session:
                pass
    else:
            return redirect("/login/")
    
    print("inside of movetask")
    data=[]
    taskid = request.POST.get("tid")
    email = request.session["user"]
    status = int(request.POST.get("status"))
    print("status from movetask" , status)  
    print(type(status))   
    taskid = int(taskid)
    print(taskid)
    print(type(taskid))
           
           
    sql = "UPDATE TASK SET status1 = %s where taskid = %s"
    deldata = (status,taskid)
    print('deldata', deldata)
    mydb = db.connect(host="localhost", user="root",
                            passwd="bismi7867", database="members")
    cursor = mydb.cursor()
    cursor.execute(sql,deldata)
    mydb.commit()
           
    mydb.close 
    

    return viewtask(request)

def logout(request):
    auth_logout(request)
   # request.session.clear()
    print("logged out")
    
    
    return JsonResponse({'form': 'success'})
              
                
        
       
       
