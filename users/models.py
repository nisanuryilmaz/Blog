from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

def upload_to(instance , filename):
    return '%s/%s/%s' % ('profilPhoto', instance.user.username , filename)


class UserProfile(models.Model):
    Erkek = 'E'
    Kadin  = 'K'
    Other  ='O'
    CINSIYET = ((Erkek,'Erkek') , (Kadin, 'Kadin') , (Other , 'Other'))

    user = models.OneToOneField(User , on_delete=models.CASCADE , verbose_name='User')
    telefon=models.CharField(max_length=11 , verbose_name='Telefon Numarası' , blank=True)
    cinsiyet  =models.CharField(max_length=1 , verbose_name='Cinsiyet' , choices=CINSIYET, default=3 , blank=True)
    hakkimda  = models.TextField(max_length=500 , verbose_name='Hakkımda' , blank=True)
    dogumTarihi = models.DateField(verbose_name='Doğum Tarihi' , blank=True,null=True)
    profilPhoto = models.ImageField(upload_to = upload_to , verbose_name='Profil Fotoğrafı',default='profilPhoto/userprofile.png')

    class Meta:
        verbose_name = 'Kullanıcı Bilgileri'
        verbose_name_plural='Kullanıcı Bilgileri'

    def __str__(self):
        return '%s Profile' % (self.user.username)

def create_user_profile(instance , created , **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(receiver=create_user_profile , sender=User)

