from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from .models import Note
from django.forms.models import model_to_dict


# admin
# @Admin123

def login_page(request):
    if request.method == 'POST':
        # print(request.POST) # thông tin về mã csrf, email, password
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        # print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')
    return render(request, 'note_app/login.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm-password')

        # mật khẩu 1 và 2 giống nhau
        if password1 == password2:
            # kiểm tra user đã tồn tại hay chưa?
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username has already existed!!!")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email has already existed!!!")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                auth.login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Password does not match!!!")
            return redirect('register')

    return render(request, 'note_app/register.html')


@login_required(login_url='/login/')
def logout_page(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def home_page(request):
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, 'note_app/index.html', {'username': username})
    else:
        return redirect('login')


@login_required(login_url='/login/')
def note_view(request):
    # notes = Note.objects.get(user=request.user)  # chỉ lấy được 1 note
    notes = list(Note.objects.filter(user=request.user).order_by('-created_at').values()) # lấy được tất cả các note
    return JsonResponse({'notes': notes})


@login_required(login_url='/login/')
def create_note(request):
    new_note = Note.objects.create(user=request.user, content='')
    note = model_to_dict(new_note)
    return JsonResponse({'message': 'Note Created Successfully!', 'note': note})


@login_required(login_url='/login/')
def save_note(request, pk):
    note = Note.objects.get(id=pk)

    if request.method == 'POST':
        content = request.POST['content']
        # print(note)
        if note:
            note.content = content
            note.save()
            return JsonResponse({'message': 'Note Updated Successfully!'})
        else:
            return JsonResponse({'message': 'Invalid Content'}, status=400)


@login_required(login_url='/login/')
def delete_note(request, pk):
    note = Note.objects.get(id=pk)
    
    if request.method == 'POST':
        if note:
            note.delete()
            return JsonResponse({'message': 'Note Deleted Successfully!'})
        else:
            return JsonResponse({'message': 'Invalid Note'}, status=400)

# Tài khoản test       
# abc123
# @abc1234
 
