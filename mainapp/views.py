import shutil
import tempfile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *

from zipfile import ZipFile
from shutil import make_archive
from django.core.files.storage import FileSystemStorage
import os
import pandas as pd

# Create your views here.
global downloadFlag
global filelink
downloadFlag=''

def home(request):
    # global filelink
    # global downloadFlag
    # global Username

    # filelink="./media/" + Username + "/" + Username + "_" +  "chunked_CSV.zip"
    #  {"username":Username, "filelink":filelink, "downloadFlag":downloadFlag}
    
    return render(request, 'mainapp/home.html', {"username":Username})

def processfile(request):
    global Username
    global downloadFlag
    global filelink
    global file_name

    if request.method == "POST":

        uploaded_file = request.FILES["formFile"]
        chunksize = request.POST["chunksize"]
        # c=uploaded_file
        # fs = FileSystemStorage()
        # fs.save(uploaded_file.name, uploaded_file)
        # print(uploaded_file.name)
        # print(uploaded_file.size)
        new_field=file(file=uploaded_file)
        new_field.save()


        os.makedirs(name="./media/" + Username + "/", exist_ok=True)
        os.makedirs(name=Username, exist_ok=True)

        
        downloadFlag=''

        new_field=usercsv.objects.get(Email=email)
        files=new_field.file_set.all()

        
        # filelink=files
        file_n = str(uploaded_file).replace(" ", "_")
        file_name = file_n.replace(",", "")
        with open ('./media/'+ file_name, "r") as f:
            csvFile=f.read()
            print(csvFile)

        with open(Username + "/" + Username + "_" + "tempfile" + ".csv" , "w") as tempfile:
            tempfile.write(csvFile)


        batch_no=1
        chunk_size = int(chunksize)

        with ZipFile("./media/" + Username + "/" + Username + "_" +  file_name + "chunked_CSV.zip", "w") as newZip:
            for chunk in pd.read_csv(Username + "/" + Username + "_" + "tempfile" + ".csv", chunksize=chunk_size):
                chunk.to_csv(Username + "/" + str(batch_no) + "_" + file_name, index=False)
                batch_no += 1
            for i in range(1, batch_no):
                newZip.write(Username + "/" + str(i) + "_" + file_name)

        messages.success(request, "Done")
        downloadFlag='True'
            # return redirect('home')
        # downloadFlag='True'
        # return redirect('home')
    filelink="./media/" + Username + "/" + Username + "_" +  file_name + "chunked_CSV.zip"
    filename = Username + "_" +  file_name + "chunked_CSV.zip"
    
    return render(request, 'mainapp/processfile.html', {"username":Username, "filelink":filelink, "filename":filename, "downloadFlag":downloadFlag})

def signup(request):
    if request.method == "POST":
        #you can also get the variables using this method also...
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['password2']

        if pass1 != pass2:
            messages.warning(request, 'Password does not match')
            return redirect('signup')

        
        t_data=User.objects.all()

        is_found = False
        for data in t_data:
            temp_data=data.username
            if temp_data.lower() == username.lower():
                is_found = True
                break

        if is_found==True:
            messages.warning(request, "Username already used!")
            return redirect('signup')


        # temp_email=usercsv.objects.get(Email=email)
        t_email=usercsv.objects.all()

        is_found = False
        for data in t_email:
            temp_email=data.Email
            if temp_email.lower() == email.lower():
                is_found = True
                break

        if is_found==True:
            messages.warning(request, "Email already used!")
            return redirect('signup')
        

        new_field=usercsv(Email=email)
        new_field.save()

        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()

        messages.success(request, "Your account has been sucessfully created")

        return redirect('signin')

    return render(request, "mainapp/signup.html")

def signin(request):
    global alreadycleared
    global email
    global filelink
    global Username

    if request.method == "POST":
        Username = request.POST['username']
        pass1 = request.POST['password']

        User = authenticate(request, username=Username, password=pass1)

        if User is not None:
            login(request, User)

            email = User.email
            alreadycleared=False
            
            return redirect('home')

        else:
            messages.warning(request, "Invalid login credentials!")
            return redirect('signin')
    return render(request, "mainapp/signin.html")

def signout(request):
    global downloadFlag
    global alreadycleared

    if downloadFlag == "True":
        shutil.rmtree("./media/" + Username + "/")
        os.remove("./media/" + file_name)
        shutil.rmtree("./" + Username)
        downloadFlag=''


    messages.success(request, "Logged out sucessful")
    return redirect('signin')

def download(request):
    global downloadFlag
    global alreadycleared
    downloadFlag=''
    alreadycleared=True

    shutil.rmtree("./media/" + Username + "/")
    os.remove("./media/" + file_name)
    shutil.rmtree("./" + Username)

    return redirect('home')