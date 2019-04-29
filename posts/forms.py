from django import forms
from .models import Post, Comment , Tag
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'kategori', 'content', 'img', 'draft' , 'etiket' ]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['draft'].widget.attrs['class'] = ''
        self.fields['img'].widget.attrs['class'] = ''
        self.fields['content'].widget.attrs['rows'] = 10
        self.fields['content'].widget.attrs['cols'] = 50


    def clean_title(self):
        title = self.cleaned_data['title']

        if title.isdigit():  # isdigit sadece rakamdan oluşturuyorsa
            raise forms.ValidationError('Lütfen sadece rakam girişi yapmayınız.')
        if '@' in title:
            raise forms.ValidationError('Lütfen @ karakterini kullanmayınız')

        return title


class PostFilterForm(forms.Form):
    SECME = (
        ('H', 'Hepsi'),
        ('T', 'Taslak'),
        ('TO', 'Taslak Olmayan')
    )
    secme = forms.CharField(label='Filtre', widget=forms.Select(choices=SECME, attrs={'class': 'form-control'}))


# Comment i import etmeyi unutma!
class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['icerik'].widget.attrs['rows'] = 10
        self.fields['icerik'].widget.attrs['cols'] = 50
        self.fields['icerik'].widget.attrs['placeholder']='Yorum Yapınız..'


    class Meta:
        model = Comment
        fields=['icerik']

    #def clean_isim_soyisim(self):
        #isim_soyisim = self.cleaned_data['isim_soyisim']

        #if not isim_soyisim.isalpha():  # metinsel değer girmediyse kayır işlemini gerçekleştirmez.
            #raise forms.ValidationError('Lütfen sadece karakter girişi yapınız.')
        #return isim_soyisim


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['isim']

    def __init__(self, *args , **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}


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