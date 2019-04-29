from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    kategori_adi = models.CharField(max_length=120, verbose_name='Kategori adı')

    def __str__(self):
        return "%s" % (self.kategori_adi)

    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'
        ordering = ['id']


class PostManager(models.Manager):
    def activite(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False)

    def taslak(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=True)


class Tag(models.Model):
    # gonderi = models.ForeignKey(Post , related_name='tag' , on_delete=models.CASCADE)
    isim = models.CharField(max_length=20, verbose_name='Etiket', blank=True,unique=True)

    def __str__(self):
        return "%s" % (self.isim)

    class Meta:
        verbose_name = 'Etiket'
        verbose_name_plural = 'Etiketler'


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, verbose_name='Yazar', default=3,
                             null=True)
    kategori = models.ManyToManyField(Category, related_name='post', verbose_name='Kategoriler')
    etiket = models.ManyToManyField(Tag, related_name='post', verbose_name='Etiketler', null=True)
    title = models.CharField(max_length=120, blank=False, verbose_name='Başlık', help_text='başlık giriniz.')
    # content = models.TextField(verbose_name='İçerik')
    content = RichTextField()
    img = models.ImageField(blank=True, verbose_name='Post Resim')
    draft = models.BooleanField(default=False, verbose_name='Taslak oluşturulsun mu?')
    create_date = models.DateField(auto_now_add=True)  # ilk kayıt oluşturulduğunda
    update_date = models.DateField(auto_now=True)  # het kayıt işlemi güncellendiğinde
    objects = PostManager()
    counter = models.IntegerField(default=0, verbose_name='counter', null=False)

    def __str__(self):
        return "%s" % (self.title)

    def get_image_or_default(self):
        if self.img and hasattr(self.img, 'url'):
            return self.img.url
        # return None  # eğer resim yüklenmediyse boş gönder
        return '/static/img/default.jpg'  # varsayılan resmin yüklenmesi

    def get_add_favorite_user(self):
        return self.favoriteBlog.values_list('user__username', flat=True)

    def get_favorite_user(self):
        return self.favoriteBlog.values_list('user__username', flat=True)




    class Meta:
        verbose_name = 'Gönderi'
        verbose_name_plural = 'Gönderilerim'
        ordering = ['-id']

    def comment_count(self):
        yorum_sayisi = self.comment.count()
        if yorum_sayisi > 0:
            return yorum_sayisi
        return 0

    def favori_count(self):

        favori_sayisi = self.favoriteBlog.count()

        if favori_sayisi >0:
            return favori_sayisi
        return 0


class Comment(models.Model):
    # vithout related_name = post.comment_set.all() bütün torumları çeker
    # bir gönderinin birden fazla yorumu olabilir.

    post = models.ForeignKey(Post, verbose_name='Post', related_name='comment', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='user', related_name='users_comment', on_delete=models.CASCADE)
    icerik = models.TextField(verbose_name='Yorum', max_length=1000)
    tarih = models.DateField(auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.post, self.user)

    class Meta:
        verbose_name = 'Yorumlar'
        verbose_name_plural = 'Yorumlar'
        ordering = ['-tarih']

    def comment_like_count(self):

        like_count = self.comment_like.count()
        if like_count >0:
            return like_count
        else:
            return 0


class CommentChild(models.Model):
    comment = models.ForeignKey(Comment , related_name='comment_child' , on_delete=models.CASCADE , verbose_name='Yorum')
    user = models.ForeignKey(User , related_name='comment_child', on_delete=models.CASCADE , verbose_name='User')
    icerik = models.TextField(max_length=1000 , verbose_name='İçerik')
    tarih = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='İç İçe Yorum'
        verbose_name_plural='İçe İçe Yorumlar'
        ordering = ['tarih']

    def __str__(self):
        return "%s" % (self.comment)


class FavoriteBlog(models.Model):
    user = models.ForeignKey(User, verbose_name='user', related_name='favoriteBlog', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='Post', related_name='favoriteBlog', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Favorilere Eklenen Gönderiler'
        verbose_name_plural = 'Favorilere Eklenen Gönderiler'

    def __str__(self):
        return "%s - %s" % (self.user, self.post.title)


class CommentLike(models.Model):
    user = models.ForeignKey(User, related_name='comment_like', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='comment_like', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Beğenilen Yorumlar'
        verbose_name_plural = 'Beğenilen Yorumlar'

    def __str__(self):
        return "%s - %s" % (self.user, self.comment.icerik)