
from django.http import request
from django.shortcuts import render, redirect, HttpResponseRedirect
from pyexpat.errors import messages
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import os
import os

import qrcode

from .models import *




# Create your views here.
def index(request):
    obj = coursedata.objects.all()
    obj1 = videodata.objects.all()
    return render(request,'index.html',{'obj':obj,'obj1':obj1})


def Login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = logindata.objects.filter(email=email, password=password).first()

        if user:
            request.session['email'] = user.email
            request.session['usertype'] = user.usertype

            if user.usertype == "admin":
                return HttpResponseRedirect('/AdminHome/')
            else:
                return HttpResponseRedirect('/StudentHome/')
        else:
            return render(request,'Login.html',{'msg':'Invalid email or password !  Please try again'})
    return render(request, 'login.html')


def AdminHome(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        email = request.session['email']
        return render(request, 'AdminHome.html', {'email': email})
    else:
        return  HttpResponseRedirect('/AuthError/')



def StudentHome(request):
    if 'email' in request.session and request.session['usertype'] == "student":
        email = request.session['email']
        obj = coursedata.objects.all()
        return render(request, 'StudentHome.html', {'email': email, 'obj': obj})
    else:
        return redirect('login')

def AuthError(request):
    return render(request, 'AuthError.html')

def Logout(request):
    request.session.flush()
    return HttpResponseRedirect('/Login/')

def AdminReg(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            name = request.POST['name']
            address = request.POST['address']
            contact = request.POST['contact']
            email = request.POST['email']
            password = request.POST['password']
            usertype ="admin"
            obj2 = logindata.objects.filter(email=email)
            if obj2:
                return render(request, 'AdminReg.html', {'msg': 'User Already Exist'})
            else:
                obj = admindata(name=name,address=address,contact=contact,email=email)
                obj1 = logindata(email=email,password=password,usertype=usertype)
                obj.save()
                obj1.save()
                return render(request, 'AdminReg.html', {'msg': 'Registered successfully'})
        else:
            return render(request,'AdminReg.html')
    else:
        return HttpResponseRedirect('/Login/')
def ShowAdmin(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        obj = admindata.objects.all()
        if obj:
            return render(request,'ShowAdmin.html',{'obj':obj})
        else:
            return render(request,'ShowAdmin.html',{'obj':'Data not Found'})
    else:
        return HttpResponseRedirect('/Login/')

def StudentReg(request):
    if request.method == "POST":
        name = request.POST['name']
        contact = request.POST['contact']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        gender = request.POST['gender']
        password = request.POST['password']
        usertype ="student"
        obj = studentdata(name=name, contact=contact, email=email, phone=phone, address=address, gender=gender)
        obj1 = logindata(email=email, password=password, usertype=usertype)
        obj.save()
        obj1.save()
        return render(request, 'StudentReg.html', {'msg': 'Registered successfully'})
    else:
        return render(request,'StudentReg.html')

def ShowStudent(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        obj = studentdata.objects.all()
        if obj:
            return render(request,'ShowStudent.html',{'obj':obj})
        else:
            return render(request,'ShowStudent.html',{'msg':'Data not Found'})
    else:
        return HttpResponseRedirect('/AuthError/')

def StudentDash(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            e1 = request.POST['email']
            obj = studentdata.objects.filter(email=e1)
            obj1 = paydata.objects.filter(student_email=e1)
            data = []
            for p in obj1:
                try:
                    course = coursedata.objects.get(course_id=p.course_id)
                except coursedata.DoesNotExist:
                    course = None
                data.append({"payment": p, "course": course})
            return render(request,'StudentDash.html ',{'obj':obj,'data':data})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')
def EditStudent(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            e1 = request.POST['email']
            obj = studentdata.objects.filter(email=e1)
            return render(request,'EditStudent.html ',{'obj':obj})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')

def EditStudent1(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            name = request.POST['name']
            contact = request.POST['contact']
            email = request.POST['email']
            phone = request.POST['phone']
            address = request.POST['address']
            gender = request.POST['gender']
            obj = studentdata.objects.get(email=email)
            obj.name = name
            obj.contact = contact
            obj.phone = phone
            obj.address = address
            obj.gender = gender
            obj.save()
            msg = "Edit Successfully"
            return render(request,'EditStudent.html ',{'msg':msg})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')

def DeleteStudent(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        e1 = request.POST['email']
        obj = studentdata.objects.filter(email=e1)
        obj.delete()
        return HttpResponseRedirect('/ShowStudent/')
    else:
        return HttpResponseRedirect('/AuthError/')
def ShowCourse(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        obj = coursedata.objects.all()
        if obj:
            return render(request,'ShowCourse.html',{'obj':obj})
        else:
            return render(request,'ShowCourse.html',{'msg':'Data not Found'})
    else:
        return HttpResponseRedirect('/AuthError/')
def AddCourse(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        return render(request,'AddCourse.html')
    else:
        return HttpResponseRedirect('/AuthError/')
def AddCourse1(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            c_name = request.POST['course_name']
            desc = request.POST['desc']
            price = request.POST['price']
            details = request.POST['details']
            pic = request.FILES['course_pic']

            obj = coursedata(coursename=c_name,desc=desc,price=price,details=details,pic=pic)
            obj.save()
            return render(request,'AddCourse.html ',{'msg':'Course added successfully'})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')

def EditCourse(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            id = request.POST['id']
            obj = coursedata.objects.filter(course_id=id)
            obj1 = videodata.objects.filter(course_id=id)
            obj2 = notesdata.objects.filter(course_id=id)
            return render(request,'EditCourse.html ',{'obj':obj,'obj1':obj1,'obj2':obj2})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')
def EditCourse1(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            course_id = request.POST['course_id']
            name = request.POST['course_name']
            desc = request.POST['desc']
            price = request.POST['price']
            details = request.POST['details']

            new_pic = request.FILES.get('course_pic')
            obj = coursedata.objects.get(course_id=course_id)

            if new_pic:
                if obj.pic and os.path.isfile(obj.pic.path):
                    os.remove(obj.pic.path)
                obj.pic = new_pic

            obj.coursename = name
            obj.desc = desc
            obj.price = price
            obj.details = details







            obj.save()
            return render(request,'EditCourse.html ',{'msg':'Course edited successfully'})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')
def DeleteCourse(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            course_id = request.POST['course_id']
            obj = coursedata.objects.get(course_id=course_id)
            obj.delete()
            return HttpResponseRedirect('/ShowCourse/')
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')
def Purchase(request):
    if 'email' in request.session and request.session['usertype'] == "student":
        email = request.session['email']
        if request.method == "POST":
            course_id = request.POST['course_id']
            obj = coursedata.objects.get(course_id=course_id)
            course_name = obj.coursename


            import qrcode
            import os


            folder_path = "media/qr"  # Already exist
            obj1 = upidata.objects.all()

            for d in obj1:
                a = d.upi
                b = d.upi_name
                break
            print(a)
            print(b)
            upi_id = a
            name = b
            note = "Course Payment"


            upi_url = f"upi://pay?pa={upi_id}&pn={name}&tn={note}&am={obj.price}&cu=INR"
            print(upi_url)
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(upi_url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # Save in existing folder
            file_path = os.path.join(folder_path, "upi_payment.png")
            img.save(file_path)

            print(f"✅ UPI QR Code saved at {file_path}")

            return render(request,'Purchase.html',{'course_id':course_id,'email':email,'price':obj.price,'upi_id':upi_id,'course_name':course_name})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')
def Pay(request):
    if 'email' in request.session and request.session['usertype'] == "student":
        email = request.session['email']
        if request.method == "POST":
            course_id = request.POST['course_id']
            utr= request.POST['utr']
            course_name = request.POST['course_name']
            status = "pending"

            obj = paydata(course_id=course_id,utr=utr,student_email=email,status=status,course_name=course_name)
            obj.save()
            return HttpResponseRedirect('/MyCourse/')
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')

def MyCourse(request):
    if 'email' in request.session and request.session['usertype'] == "student":
        email = request.session['email']
        obj = paydata.objects.filter(student_email=email)
        data = []
        for p in obj:
            try:
                course = coursedata.objects.get(course_id=p.course_id)
            except coursedata.DoesNotExist:
                course = None
            data.append({"payment": p, "course": course})

        return render(request, 'MyCourse.html', {'data': data})
    else:
        return HttpResponseRedirect('/AuthError/')




def Payment(request):

    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            category = request.POST.get('category')
            print(category)
            if category=='access':
                obj = paydata.objects.filter(status=category)
                objs = paydata.objects.filter(status="access")
                obje = paydata.objects.filter(status="reject")
                sold = objs.count()
                print(sold)
                rejects = obje.count()
                total = 0
                if objs:
                    for d in objs:
                        j = coursedata.objects.filter(course_id=d.course_id)
                        for p in j:
                            total += p.price
                print(f'total:{total}')
                obj1 = upidata.objects.all()
                if obj1:
                    return render(request, 'Payment.html', {'obj': obj, 'obj1': obj1,'sold':sold,'rejects':rejects,'total':total})
                else:
                    return render(request, 'Payment.html', {'obj': obj})
            elif category=='reject':
                obj = paydata.objects.filter(status=category)
                objs = paydata.objects.filter(status="access")
                obje = paydata.objects.filter(status="reject")
                sold = 0
                print(sold)
                rejects = obje.count()
                total = 0

                obj1 = upidata.objects.all()
                if obj1:
                    return render(request, 'Payment.html', {'obj': obj, 'obj1': obj1,'sold':sold,'rejects':rejects,'total':total})
                else:
                    return render(request, 'Payment.html', {'obj': obj})
            else:
                obj = paydata.objects.all().order_by('-dates')
                objs = paydata.objects.filter(status="access")
                obje = paydata.objects.filter(status="reject")
                sold = objs.count()
                print(sold)
                rejects = obje.count()
                total = 0
                if objs:
                    for d in objs:
                        j = coursedata.objects.filter(course_id=d.course_id)
                        for p in j:
                            total += p.price
                print(f'total:{total}')
                c = obj.count()
                print(c)
                obj1 = upidata.objects.all()
                if obj1:
                    return render(request, 'Payment.html', {'obj': obj, 'obj1': obj1,'sold':sold,'rejects':rejects,'total':total})
                else:
                    return render(request, 'Payment.html', {'obj': obj})
        else:
            obj = paydata.objects.all().order_by('-dates')
            objs = paydata.objects.filter(status="access")
            total = 0
            if objs:
                for d in objs:
                    j = coursedata.objects.filter(course_id=d.course_id)
                    for p in j:
                        total += p.price
            print(f'total:{total}')

            obje = paydata.objects.filter(status="reject")
            sold = objs.count()
            print(sold)
            rejects = obje.count()
            print(rejects)
            obj1 = upidata.objects.all()
            if obj1:
                return render(request, 'Payment.html', {'obj': obj,'obj1':obj1,'sold':sold,'rejects':rejects,'total': total})
            else:
                return render(request, 'Payment.html', {'obj': obj})
    else:
        return HttpResponseRedirect('/AuthError/')



def ConfirmPayment(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            id = request.POST.get('id')
            student_email = request.POST.get('student_email')
            paydata.objects.filter(id=id, student_email=student_email).update(status="access")
            return HttpResponseRedirect('/Payment/')
        else:
            return HttpResponseRedirect('/Payment/')
    else:
        return HttpResponseRedirect('/AuthError/')



def RejectPayment(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            id = request.POST.get('id')
            student_email = request.POST.get('student_email')
            try:
                payment=paydata.objects.filter(id=id, student_email=student_email).update(status="reject")

            except paydata.DoesNotExist:
                pass

            return HttpResponseRedirect('/Payment/')
        else:
            return HttpResponseRedirect('/Payment/')
    else:
        return HttpResponseRedirect('/AuthError/')
def CoursePage(request):
    if 'email' in request.session and request.session['usertype'] == "student":
        email = request.session['email']
        if request.method == "POST":
            status = request.POST.get('status')
            if status == "access":
                course_id = request.POST['course_id']
                print(course_id)
                obj = coursedata.objects.filter(course_id=course_id)
                obj1 = videodata.objects.filter(course_id=course_id)
                obj2 = notesdata.objects.filter(course_id=course_id)

                return render(request,'CoursePage.html',{'obj': obj,'obj1':obj1,'obj2':obj2})
            else:
                return HttpResponseRedirect('/AuthError/')
        else:
            return HttpResponseRedirect('/Payment/')
    else:
        return HttpResponseRedirect('/AuthError/')
def Cancel(request):
    if 'email' in request.session and request.session['usertype'] == "student":
        email = request.session['email']
        if request.method == "POST":
            id = request.POST['id']
            obj = paydata.objects.get(id=id)
            obj.delete()
            return HttpResponseRedirect('/MyCourse/')
        else:
            return HttpResponseRedirect('/AuthError/')
    elif 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            id = request.POST['id']
            obj = paydata.objects.get(id=id)
            obj.delete()
            return HttpResponseRedirect('/Payment/')
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')


def Delete(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            id = request.POST['id']
            obj = paydata.objects.get(id=id)
            obj.delete()
            return HttpResponseRedirect('/ShowStudent/')
        else:
            return HttpResponseRedirect('/StudentDash/')
    else:
        return HttpResponseRedirect('/AuthError/')
def VideoAdd(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            course_id = request.POST.get('course_id')
            return render(request,'VideoAdd.html',{'course_id': course_id})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')
def VideoAdd1(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            course_id = request.POST.get('course_id')
            video = request.FILES['video']
            thum = request.FILES['thum']
            topic = request.POST.get('topic')
            obj = videodata(course_id=course_id, video_file=video,thum=thum,topic=topic)
            obj.save()
            return render(request, 'VideoAdd.html', {'msg': 'Video Add Successful'})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')


def DeleteVideo(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            video_id = request.POST.get("id")
            obj = get_object_or_404(videodata, id=video_id)


            if obj.video_file and obj.video_file.path:
                if os.path.exists(obj.video_file.path):
                    os.remove(obj.video_file.path)

            if obj.thum and obj.thum.path:
                if os.path.exists(obj.thum.path):
                    os.remove(obj.thum.path)


            obj.delete()

            return HttpResponseRedirect('/ShowCourse/')
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')
def StudentProfile(request):
    if 'email' in request.session and request.session['usertype'] == "student":
        email = request.session['email']
        obj = studentdata.objects.filter(email=email)
        return render(request,'StudentProfile.html',{'obj': obj})
    else:
        return HttpResponseRedirect('/AuthError/')

def EditStudentProfile(request):
    if 'email' in request.session and request.session['usertype'] == "student":
        email = request.session['email']
        if request.method == "POST":
            obj = studentdata.objects.filter(email=email)
            return render(request,'EditStudentProfile.html',{'obj': obj})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')

def EditStudentProfile1(request):
    if 'email' in request.session and request.session['usertype'] == "student":
        if request.method == "POST":
            email  = request.session['email']
            name = request.POST['name']
            contact = request.POST['contact']
            address = request.POST['address']
            phone = request.POST['phone']
            gender = request.POST['gender']
            obj = studentdata.objects.get(email=email)
            obj.name = name
            obj.contact = contact
            obj.address = address
            obj.phone = phone
            obj.gender = gender
            obj.save()
            return render(request, 'EditStudentProfile.html', {'msg': 'Save Successfully'})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')
def AdminProfile(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        email = request.session['email']
        obj = admindata.objects.filter(email=email)
        return render(request,'AdminProfile.html',{'obj': obj})
    else:
        return HttpResponseRedirect('/AuthError/')
def EditAdminProfile(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        email = request.session['email']
        if request.method == "POST":
            obj = admindata.objects.filter(email=email)
            return render(request,'EditAdminProfile.html',{'obj': obj})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')
def EditAdminProfile1(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            email  = request.session['email']
            name = request.POST['name']
            contact = request.POST['contact']
            address = request.POST['address']
            obj = admindata.objects.get(email=email)
            obj.name = name
            obj.contact = contact
            obj.address = address
            obj.save()
            return render(request, 'EditAdminProfile.html', {'msg': 'Save Successfully'})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')

def ChangeAdminPassword(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            return render(request, 'ChangeAdminPassword.html')
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')
def ChangeAdminPassword1(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        email = request.session['email']
        if request.method == "POST":
            old = request.POST['old_password']
            new = request.POST['new_password']
            try:
                obj = logindata.objects.get(email=email,password=old)
                obj.password = new
                obj.save()
                return render(request, 'ChangeAdminPassword.html', {'msg': 'Save Successfully'})
            except logindata.DoesNotExist:
                return render(request, 'ChangeAdminPassword.html', {'msg': 'Old Password Wrong'})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')

def ChangeStudentPassword(request):
    if 'email' in request.session and request.session['usertype'] == "student":
        if request.method == "POST":
            return render(request, 'ChangeStudentPassword.html')
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')

def ChangeStudentPassword1(request):
    if 'email' in request.session and request.session['usertype'] == "student":
        email = request.session['email']
        if request.method == "POST":
            old = request.POST['old_password']
            new = request.POST['new_password']
            try:
                obj = logindata.objects.get(email=email,password=old)
                obj.password = new
                obj.save()
                return render(request, 'ChangeStudentPassword.html', {'msg': 'Save Successfully'})
            except logindata.DoesNotExist:
                return render(request, 'ChangeStudentPassword.html', {'msg': 'Old Password Wrong'})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')





def PaymentReceive(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            return render(request, 'PaymentReceive.html')
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')

def PaymentReceive1(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            upi = request.POST['upi']
            upi_name = request.POST['upi_name']
            obj = upidata(upi=upi, upi_name=upi_name)

            obj.save()
            return render(request, 'PaymentReceive.html',{'msg': 'Save Successfully'})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')

def ChangePaymentReceive(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            return render(request, 'ChangePaymentReceive.html')
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')

def ChangePaymentReceive1(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            upi = request.POST['upi']
            old_upi = request.POST['old_upi']
            upi_name = request.POST['upi_name']
            try:

                obj = upidata.objects.get(upi=old_upi)

                obj.upi= upi
                obj.upi_name=upi_name

                obj.save()
                return render(request, 'ChangePaymentReceive.html', {'msg': 'Save Successfully'})

            except upidata.DoesNotExist:
                return render(request, 'ChangePaymentReceive.html', {'msg': 'Old Upi Incorrect'})

        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')

def CourseDetails(request):
    if request.method == 'POST':
        if 'email' in request.session and request.session['usertype'] == "student":
            course_id = request.POST['course_id']
            print(course_id)


            obj = coursedata.objects.filter(course_id=course_id)
            return render(request, 'CourseDetailsSession.html', {'obj': obj})
        else:
            course_id = request.POST['course_id']
            print(course_id)
            obj = coursedata.objects.filter(course_id=course_id)
            return render(request, 'CourseDetails.html',{'obj':obj})
    else:
        return HttpResponseRedirect('/AuthError/')

def AddNotes(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            course_id = request.POST.get('course_id')
            return render(request, 'AddNotes.html', {'course_id': course_id})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')

def AddNotes1(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            course_id = request.POST.get('course_id')
            note = request.FILES['note']
            title = request.POST['title']
            obj = notesdata(course_id=course_id, note_file=note,title=title)
            obj.save()
            return render(request, 'AddNotes.html', {'msg': ' Add Notes Successful'})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')

def EditNotes(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            id = request.POST.get('id')
            obj = notesdata.objects.filter(id=id)
            return render(request, 'EditNotes.html', {'obj': obj})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')

def EditNotes1(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            id = request.POST.get('id')
            new_note = request.FILES['note']
            title = request.POST['title']
            obj = notesdata.objects.get(id=id)
            if new_note:
                if obj.note_file and os.path.isfile(obj.note_file.path):
                    os.remove(obj.note_file.path)
                obj.note_file = new_note
            obj.title = title
            obj.save()
            return render(request, 'EditNotes.html', {'msg': ' Save Notes Successful'})
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')

def DeleteNotes(request):
    if 'email' in request.session and request.session['usertype'] == "admin":
        if request.method == "POST":
            id = request.POST.get('id')
            obj = notesdata.objects.filter(id=id)
            obj.delete()
            return HttpResponseRedirect('/ShowCourse/')
        else:
            return HttpResponseRedirect('/AuthError/')
    else:
        return HttpResponseRedirect('/AuthError/')