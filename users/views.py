from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, HttpResponseRedirect, Http404
from .forms import Register, LoginForm,UserProfileForm,UserPasswordChangeForm,UserUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
#from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse


def user_create(request):
    form = Register(request.POST or None)
    # kullanıcı varsa post işlemi yoksa none değerini alır.
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])

        user.save()
        yetkiliMi = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        print(yetkiliMi)
        if yetkiliMi:
            login(request, user)
            return HttpResponseRedirect(reverse('post_list'))

    return render(request, 'users/register.html', context={'form': form})


def user_login(request):
    next = request.GET.get('next',None)
    form = LoginForm(request.POST or None)
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('post_list'))
    if form.is_valid():
        next = request.POST.get('nextt',None)
        yetkiliMi = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if yetkiliMi:
            login(request, yetkiliMi)

            if next and next != 'None':

                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse('post_list'))
        else:
            hata = 'Kullanıcı adını veya parola hatalı !'
            return render(request, 'users/login.html', context={'form': form, 'hata_mesaji': hata})

    return render(request, 'users/login.html', context={'form': form , 'next' : next})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


def user_edit_profile(request):
    data = { 'cinsiyet' : request.user.userprofile.cinsiyet , 'dogumTarihi' : request.user.userprofile.dogumTarihi,
             'hakkimda' : request.user.userprofile.hakkimda , 'telefon' : request.user.userprofile.telefon,
             #'profilPhoto' : request.user.userprofile.profilPhoto

           }
    print(request.user.userprofile.profilPhoto,"-----")
    user_profil_form=UserProfileForm(request.POST or None , instance = request.user  , initial = data )

    if user_profil_form.is_valid():
        user_profil_form.save(commit=True)
        hakkimda = user_profil_form.cleaned_data['hakkimda']
        cinsiyet = user_profil_form.cleaned_data['cinsiyet']
        telefon = user_profil_form.cleaned_data['telefon']
        dogumTarihi = user_profil_form.cleaned_data['dogumTarihi']
        #profilPhoto = user_profil_form.cleaned_data['profilPhoto']

        request.user.userprofile.hakkimda = hakkimda
        request.user.userprofile.cinsiyet = cinsiyet
        request.user.userprofile.telefon  = telefon
        request.user.userprofile.dogumTarihi = dogumTarihi
        #request.user.userprofile.profilPhoto = profilPhoto

        request.user.userprofile.save()
        messages.success(request,'Tebrikler güncelleme işleminiz başarıyla gerçekleşti')
        return HttpResponseRedirect(reverse('post_list'))

    return render(request , 'users/user_edit_profile.html' , context={'form':user_profil_form})


def password_change(request):
    form = UserPasswordChangeForm(request.user , request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user =form.save(commit=True)
            update_session_auth_hash(request ,user)
            messages.success(request , 'Tebrikler şifreniz başarıyla güncellenmiştir.')
    return render(request, 'users/password_change.html' , context={'form':form})


def user_update_photo(request):
    if request.method == "POST":
        form = UserUpdateForm(instance=request.user.userprofile,data=request.POST , files=request.FILES)  #var olan  kullanıcının fotoğrafını düzenlemede instance ile userpile ini belirtiriz.
        if form.is_valid():
            userprofile= form.save(commit=True)
            data = {'is_valid': True, 'image-url': userprofile.profilPhoto.url, 'success' :'Profil fotoğrafı güncellendi.'}
            return JsonResponse(data=data)
        else:
            return JsonResponse(data=
                                {'is_valid':False})
    else:
        return HttpResponseRedirect(reverse('user_edit_profile'))

