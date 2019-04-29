from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile



class Register(forms.ModelForm):
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]

    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

    def clean_email(self):
        email = self.cleaned_data['email']
        uzunluk = len(User.objects.filter(email=email))
        if uzunluk > 0:
            raise forms.ValidationError('Bu mail adresi daha önce kullanılmıştır.')
        return email


class UserProfileForm(forms.ModelForm):
    Erkek = 'E'
    Kadin = 'K'
    Other = 'O'
    CINSIYET = ((Erkek, 'Erkek'), (Kadin, 'Kadin'), (Other, 'Other'))

    cinsiyet = forms.CharField(widget=forms.Select(choices=CINSIYET))
    hakkimda = forms.CharField(widget=forms.Textarea, label='Hakkımda', max_length=500 , required=False)
    telefon = forms.CharField(max_length=11, label='Telefon Numarası',required=False)
    dogumTarihi = forms.DateField(input_formats=("%d.%m.%Y"),widget=forms.DateInput(format="%d.%m.%Y"), label='Doğum Tarihi' , required=False)


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telefon', 'dogumTarihi', 'cinsiyet', 'hakkimda']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

        self.fields['hakkimda'].widget.attrs['rows']=10
        self.fields['hakkimda'].widget.attrs['cols']=10


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=50, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']

        if '@' in username:
            user = User.objects.filter(email=username)
            if len(user) == 1:
                user = user.first()
                return user.username
            elif len(user) > 1:
                raise forms.ValidationError('lğtfen kullanıcı adı ile giriş yapınız.')
            else:
                raise forms.ValidationError('Böyle bir kullanıcı yoktur.')

        return username

class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self , *args , **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args , kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class' : 'form-control'}

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields =['profilPhoto']


