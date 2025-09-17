"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('Login/', Login),
    path('Logout/', Logout),
    path('AuthError/', AuthError),
    path('AdminReg/', AdminReg),
    path('ShowAdmin/', ShowAdmin),
    path('AdminHome/', AdminHome),
    path('StudentReg/', StudentReg),
    path('StudentHome/', StudentHome),
    path('ShowStudent/', ShowStudent),
    path('StudentDash/', StudentDash),
    path('EditStudent/', EditStudent),
    path('EditStudent1/', EditStudent1),
    path('DeleteStudent/', DeleteStudent),
    path('ShowCourse/', ShowCourse),
    path('AddCourse/', AddCourse),
    path('AddCourse1/', AddCourse1),
    path('EditCourse/', EditCourse),
    path('EditCourse1/', EditCourse1),
    path('DeleteCourse/', DeleteCourse),
    path('Purchase/', Purchase),
    path('Pay/', Pay),
    path('MyCourse/', MyCourse),
    path('Payment/', Payment),
    path('ConfirmPayment/', ConfirmPayment),
    path('RejectPayment/', RejectPayment),
    path('CoursePage/', CoursePage),
    path('Cancel/', Cancel),
    path('Delete/', Delete),
    path('VideoAdd/', VideoAdd),
    path('VideoAdd1/', VideoAdd1),
    path('DeleteVideo/', DeleteVideo),
    path('AdminProfile/', AdminProfile),
    path('StudentProfile/', StudentProfile),
    path('EditStudentProfile/', EditStudentProfile),
    path('EditStudentProfile1/', EditStudentProfile1),
    path('EditAdminProfile/', EditAdminProfile),
    path('EditAdminProfile1/', EditAdminProfile1),
    path('ChangeAdminPassword/', ChangeAdminPassword),
    path('ChangeAdminPassword1/', ChangeAdminPassword1),
    path('ChangeStudentPassword/', ChangeStudentPassword),
    path('ChangeStudentPassword1/', ChangeStudentPassword1),
    path('PaymentReceive/', PaymentReceive),
    path('PaymentReceive1/', PaymentReceive1),
    path('ChangePaymentReceive/', ChangePaymentReceive),
    path('ChangePaymentReceive1/', ChangePaymentReceive1),
    path('CourseDetails/', CourseDetails),
    path('AddNotes/',AddNotes),
    path('AddNotes1/',AddNotes1),
    path('EditNotes/',EditNotes),
    path('EditNotes1/',EditNotes1),
    path('DeleteNotes/',DeleteNotes),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
