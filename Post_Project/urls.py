from django.contrib import admin
from django.urls import path,include
from Post_Project import views



urlpatterns = [
    path('admin-panel/', admin.site.urls),
     
    path('viewtask/', views.viewtask),

    path('taskpage/', views.taskpage, name="taskpage"),
    path('submitform/', views.submit__signup_form,name="submitform"),
    path('login/',views.login_form,name="login"),
    path('task/', views.taskform, name="taskform"),
    path('movetask/',views.movetask,name='movetask'),
    path('update/', views.updateform, name="updateform"),
    path('logout/', views.logout, name="logout")
   ]