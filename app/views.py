from django.shortcuts import render,redirect

# Create your views here.

from app.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from secretsharing import PlaintextToHexSecretSharer
# from secretsharingpy import PlaintextToHexSecretSharer
from app.crypto_utils import *



def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')



def registration(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        conform_password=request.POST['conform_password']
        role= request.POST['role']
        contact=request.POST['contact']
        address = request.POST['address']
        profile=request.FILES.get('profile')

        if password==conform_password:
            if UserModel.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect('registration')
        
            if UserModel.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return redirect('/registration')
            
            UserModel.objects.create(username=username,email=email,password=password,role=role , contact=contact,address=address,profile=profile)
            messages.success(request,'Registration Successfully')
            return redirect('/login')
        
        else:
            messages.error(request,'Password is Not Matching!!!')
            return redirect('/registration')

    return render(request,'registration.html')



def login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        # role=request.POST['role']
        
        try:
            user = UserModel.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            request.session['role'] = user.role
            request.session['email'] = user.email

            if user.role == 'do':
                return redirect('data_owner_dashboard')
            elif user.role == 'du':
                return redirect('data_user_dashboard')
        except UserModel.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request,'login.html')


def forgot_password(request):
    context = {}
    
    if request.method == "POST":
        # If user submits email to verify
        if 'email_submit' in request.POST:
            email = request.POST.get('email')
            try:
                user = UserModel.objects.get(email=email)
                context['email_verified'] = True
                context['email'] = email
            except UserModel.DoesNotExist:
                messages.error(request, "Email not found.")
        
        # If user submits new password to reset
        elif 'password_submit' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                context['email_verified'] = True
                context['email'] = email
            else:
                try:
                    user = UserModel.objects.get(email=email)
                    user.password = password  # Storing plain text as per your registration
                    user.save()
                    messages.success(request, "Password updated successfully. Please login.")
                    return redirect('login')
                except UserModel.DoesNotExist:
                    messages.error(request, "Invalid email.")

    return render(request, 'forgot_password.html', context)

def view_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = UserModel.objects.get(id=user_id)

    context = {
        'user': user,
        'login': user.role  # Make sure this is 'do' or 'du' exactly as string
    }
    return render(request, 'view_profile.html', context)

def update_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = UserModel.objects.get(id=user_id)
    except UserModel.DoesNotExist:
        return redirect('login')
    
    context = {
        'user': user,
        'login': user.role  # This must be a string 'do' or 'du'
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        profile = request.FILES.get('profile')

        # Check if username/email changed and if already taken
        if username != user.username and UserModel.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, 'Username already exists.')
            return redirect('update_profile')

        if email != user.email and UserModel.objects.filter(email=email).exclude(id=user_id).exists():
            messages.error(request, 'Email already registered.')
            return redirect('update_profile')

        # Update fields
        user.username = username
        user.email = email
        user.contact = contact
        user.address = address

        if profile:
            user.profile = profile

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('update_profile')
    return render(request,'update_profile.html' , context)

def data_owner_dashboard(request):
    if request.session.get('role') != 'do':
        return redirect('login')
    return render(request, 'owner_dashboard.html')

def data_user_dashboard(request):
    if request.session.get('role') != 'du':
        return redirect('login')
    return render(request, 'user_dashboard.html')

# def logout(request):
#     del request.session['email']
#     redirect('/login')


def logout(request):
    if 'email' in request.session:
        del request.session['email']
    request.session.flush()  # Optional: clears all session data
    return redirect('/')



def serverA_login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        if email=='serverA@gmail.com' and password == 'server':
            request.session['email'] = email
            request.session['login'] = 'serverA'
            return redirect('serverA_dashboard')
        else:
            return render('/sereverA_login')
        
    return render(request,'serverA_login.html')


def server_login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        if email=='serverA@gmail.com' and password == 'server':
            request.session['email'] = email
            request.session['login'] = 'serverA'
            return redirect('serverA_dashboard')
        
        elif email=='serverB@gmail.com' and password == 'server':
            request.session['email'] = email
            request.session['login'] = 'serverB'
            return redirect('serverB_dashboard')
        
        elif email=='serverC@gmail.com' and password == 'server':
            request.session['email'] = email
            request.session['login'] = 'serverC'
            return redirect('serverC_dashboard')
        else:
            return redirect('server_login')

    return render(request,'server_login.html')

from django.core.paginator import Paginator
def serverA_dashboard(request):
    return render(request,'serverA_dashboard.html')

def serverB_dashboard(request):
    return render(request, 'serverB_dashboard.html')

def serverC_dashboard(request):
    return render(request,'serverC_dashboard.html')

def serverA_files(request):
    all_files=Server_A.objects.all()
    paginator = Paginator(all_files, 4)  # Show 4 files per page
    page_number = request.GET.get('page')
    files = paginator.get_page(page_number)
    return render(request,'serverA_files.html', {'files':files})

def serverB_files(request):
    all_files=Server_B.objects.all()
    paginator = Paginator(all_files, 4)  # Show 4 files per page
    page_number = request.GET.get('page')
    files = paginator.get_page(page_number)
    return render(request,'serverB_files.html',{'files':files})

def serverC_files(request):
    all_files=Server_C.objects.all()
    paginator = Paginator(all_files, 4)  # Show 4 files per page
    page_number = request.GET.get('page')
    files = paginator.get_page(page_number)
    return render(request,'serverC_files.html',{'files':files})

def dashboard(request):
    return render(request,'dashboard.html')




from django.shortcuts import render, redirect
from django.contrib import messages



def upload(request):
    if 'email' not in request.session:
        messages.error(request, "You must be logged in to upload.")
        return redirect('/login/')

    try:
        owner = UserModel.objects.get(email=request.session['email'])
    except UserModel.DoesNotExist:
        messages.error(request, "Invalid session. Please log in again.")
        return redirect('/login/')

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        filename = request.POST.get('filename') or uploaded_file.name
        keyword = request.POST['keyword'].strip().lower()

        try:
            # Read the uploaded file content as text
            file_data = uploaded_file.read().decode('utf-8', errors='ignore')

            # Encrypt the file content
            encrypted_content = encrypt_file_content(file_data)

            # Save encrypted content to temp path
            temp_file_path = os.path.join('static/assets/Files', filename)
            os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
            with open(temp_file_path, 'wb') as ef:
                ef.write(encrypted_content.encode())  # ✅ Encrypted text -> bytes

            # Split into 3 parts
            part1, part2, part3 = split_data(encrypted_content)

            # Encrypt the keyword
            encrypted_keyword = abks_encrypt(keyword, public_key)

            # Save Document to DB (original file kept for reference)
            doc = Document.objects.create(
                filename=filename,
                file=uploaded_file,  # optional; you can omit this if saving .enc only
                filedata=encrypted_content.encode(),
                keyword=keyword,
                encrypted_keyword=encrypted_keyword,
                owner=owner
            )

            # Store encrypted parts with keyword in servers
            Server_A.objects.create(file_part=part1, doc_id=doc.id, keyword=keyword)
            Server_B.objects.create(file_part=part2, doc_id=doc.id, keyword=keyword)
            Server_C.objects.create(file_part=part3, doc_id=doc.id, keyword=keyword)

            messages.success(request, 'File encrypted and saved successfully.')
            return redirect('/upload')

        except Exception as e:
            messages.error(request, f"Upload failed: {str(e)}")
            return render(request, 'upload.html')

    return render(request, 'upload.html')

#  + '.enc'

def search(request):
    if request.method == 'POST':
        keyword=request.POST['keyword'].strip().lower()
        
        results = Document.objects.filter(keyword__iexact=keyword)

        return render(request,'search.html',{'results':results})
    return render(request,'search.html')


def request_file(request, doc_id):
    if 'email' not in request.session:
        messages.error(request, "You must be logged in to request files.")
        return redirect('/login/')

    try:
        requester_email = request.session['email']
        document = get_object_or_404(Document, id=doc_id)

        # Prevent duplicate requests
        if RequestFile.objects.filter(document=document, requester_email=requester_email).exists():
            messages.warning(request, "You have already requested this file.")
            return redirect('/search')

        RequestFile.objects.create(
            document=document,
            owner=document.owner,  # the data owner
            requester_email=requester_email,  # the data user requesting
            status='pending'
        )

        messages.success(request, "File request sent successfully.")
        return redirect('/search')

    except Document.DoesNotExist:
        messages.error(request, "Requested document does not exist.")
        return redirect('/search')


def view_request(request):
    # requests=RequestFile.objects.filter(owner=request.user)
    # return render('view_request.html',{'requests':requests})
    
    if 'email' not in request.session:
        messages.error(request, "You must be logged in to view requests.")
        return redirect('/login/')

    try:
        user = UserModel.objects.get(email=request.session['email'])
    except UserModel.DoesNotExist:
        messages.error(request, "Invalid session. Please log in again.")
        return redirect('/login/')

    requests = RequestFile.objects.filter(owner=user)
    return render(request, 'view_request.html', {'requests': requests})

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.conf import settings

import random
def generate_download_key(length=6):
    return ''.join(random.choices('0123456789', k=length))


def accept_req(request,id):
    if request.method == 'POST':
        req=get_object_or_404(RequestFile,id=id)
        req.status ='accepted'
        key = generate_download_key()
        req.download_key = key
        req.save()
        subject = f"Your access to '{req.document.filename}' has been approved"
        message = (
            f"Dear Data User,\n\n"
            f"Your request for the file '{req.document.filename}' has been accepted by the Data Owner ({req.owner.email}).\n"
            f"Please use the following download key along with the original keyword to access the file:\n\n"
            f"🔑 Download Key: {key}\n\n"
            f"Regards,\nSecure File Sharing System"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # owner’s email
            [req.requester_email],
            fail_silently=False
        )

        messages.success(request, f"Request accepted. Download key sent to {req.requester_email}.")
        messages.success(request, f'Request for "{req.document.filename}" accepted.')
        return redirect('/view_request')
    
def reject_req(request,id):
    if request.method == 'POST':
        req = get_object_or_404(RequestFile,id=id)
        req.status='rejected'
        req.save()
        messages.error(request, f'Request for "{req.document.filename}" rejected')
        return redirect('view_request')
    


def view_file(request):
    files=Document.objects.all()
    return render(request,'view_file.html',{'files':files})

def view_requestfile(request):
    if 'email' not in request.session:
        return redirect('/login/')

    email = request.session['email']
    files=RequestFile.objects.all()
    return render(request,'view_requestfile.html',{'files':files})

def view_response(request):

    if 'email' not in request.session:
        return redirect('/login/')

    email = request.session['email']
    responses=RequestFile.objects.filter(requester_email=email)
    return render(request,'view_response.html',{'responses':responses})

# status='accepted'



from django.http import FileResponse
def download(request, doc_id):
    if 'email' not in request.session:
        messages.error(request, "Login required to download.")
        return redirect('/login/')

    if request.method == 'POST':
        keyword = request.POST.get('keyword','').strip().lower()
        key = request.POST.get('key','').strip()
        email = request.session['email']


        req = get_object_or_404(RequestFile, document_id=doc_id, requester_email=email, status='accepted')

        if req.download_key == key and req.document.keyword == keyword:
            
            return FileResponse(req.document.file, as_attachment=True, filename=req.document.filename)
        else:
            messages.error(request, "Invalid keyword or download key.")
            return redirect('view_response')

    return render(request,'download.html')

from django.http import HttpResponse
from mimetypes import guess_type
# def download(request, doc_id):
#     if 'email' not in request.session:
#         messages.error(request, "Login required to download.")
#         return redirect('/login/')

#     if request.method == 'POST':
#         keyword = request.POST.get('keyword','').strip().lower()
#         key = request.POST.get('key','').strip()
#         email = request.session['email']

#         req = get_object_or_404(RequestFile, document_id=doc_id, requester_email=email, status='accepted')

#         if req.download_key == key and req.document.keyword == keyword:
#             # Decrypt the stored encrypted content
#             encrypted_content = req.document.filedata  # Assuming bytes stored here
#             decrypted_content = decrypt_file_content(encrypted_content.decode() if isinstance(encrypted_content, bytes) else encrypted_content)
#             # Prepare HTTP response with appropriate headers
#             mime_type, _ = guess_type(req.document.filename)
#             response = HttpResponse(decrypted_content, content_type=mime_type or 'application/octet-stream')
#             response['Content-Disposition'] = f'attachment; filename="{req.document.filename}"'
#             return response
#         else:
#             messages.error(request, "Invalid keyword or download key.")
#             return redirect('view_response')

#     return render(request,'download.html')