
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse, redirect, get_object_or_404, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages  # messages framework için eklediğimiz kütüphane
from .models import Post, Tag, User, FavoriteBlog , CommentChild , Comment , CommentLike
from .forms import PostForm, TagForm,LoginForm
from .forms import CommentForm
from .forms import PostFilterForm
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # sayfalama
from django.db.models import Q  # arama işlemi için eklediğimiz kütüphane
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.http import JsonResponse
from urllib.parse import quote_plus
from django.contrib.auth import authenticate, login


def form_ornek(request):
    gelen_mesaj = request.GET.get('mesaj', None)
    print(gelen_mesaj)
    return render(request, 'posts/form.html', context={'gelen_mesaj': gelen_mesaj})


def index(request):
    next = request.GET.get('next', None)
    form = LoginForm(request.POST or None)
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('post_list'))
    if form.is_valid():
        next = request.POST.get('nextt', None)
        yetkiliMi = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if yetkiliMi:
            login(request, yetkiliMi)

            if next and next != 'None':
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse('post_list'))
        else:
            hata = 'Kullanıcı adını veya parola hatalı !'
            return render(request, 'users/login.html', context={'form': form, 'hata_mesaji': hata})

    return render(request, 'users/login.html', context={'form': form, 'next': next})


@login_required(login_url='/users/login/')
def post_create(request):
    post_form = PostForm

    if request.method == 'POST' and request.user.is_authenticated:
        post_form = PostForm(request.POST or None, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Tebrikler kayıt işleminiz gerçekleştirildi.')
            # return HttpResponseRedirect(reverse('post:post_list'))
            # return redirect('post_list')   #kaydet butonuna tıklandığında listelenen sayfaya yönlendirir
            return HttpResponseRedirect(reverse('post_detail', kwargs={'pk': post_form.instance.pk}))  # kaydet butonuna tıklandığında detay sayfaya yönlendirir

    return render(request, 'posts/post_create.html', context={'form': post_form})


@login_required(login_url='/users/login/')
def tag_create(request):
    tag_form = TagForm
    tag = Tag.objects.all()
    if request.method == 'POST' and request.user.is_authenticated:
        tag_form = TagForm(request.POST or None)
        if tag_form.is_valid():
            tag_form.save(commit=True)
            return redirect('post_create')
    return render(request, 'posts/tag_create.html', context={'form': tag_form, 'tag':tag})



@login_required(login_url='/users/login/')
def tag_delete(request, pk):

    tagg = get_object_or_404(Tag, pk=pk)
    tagg.delete()
    messages.warning(request, 'Etiket silinmiştir', extra_tags='danger')
    return HttpResponseRedirect(reverse('tag_create'))


def post_list(request):
    page = request.GET.get('page', 1)
    query = request.GET.get('q', None)

    filter_form = PostFilterForm(request.GET or None)
    data = request.GET.get('secme')
    posts_list = Post.objects.all()  # bütün postları aldık şuan

    user_list = User.objects.all()

    if filter_form.is_valid():
        secme = filter_form.cleaned_data['secme']
        if secme == 'T':
            posts_list = posts_list.filter(draft=True)
        elif secme == 'TO':
            posts_list = posts_list.filter(draft=False)
            # posts_list.filter(draft=False)
    if query:
        user_list = User.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).filter(full_name__iexact=query)

        posts_list = posts_list.filter(
                                       Q(title__icontains=query) |
                                       Q(kategori__kategori_adi__icontains=query) |
                                       Q(user__last_name__icontains=query) |
                                       Q(user__first_name__iexact=query))

    paginator = Paginator(posts_list, 4)
    try:
        posts_list = paginator.page(page)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    except EmptyPage:
        posts_list = paginator.page(paginator.num_pages)

    return render(request, 'posts/post_list.html', context={'post_list': posts_list,
                                                            'filter_form': filter_form})
                                                            #'user_list' : user_list})


@login_required(login_url='/users/login/')
def fav(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user == post.user:
        return render(request, 'posts/favorite.html', context={'post': post})
    return render(request, 'posts/post_detail.html', context={'post': post})


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(data=request.POST or None, instance=post, files=request.FILES or None)
    if form.is_valid():
        form.save(commit=True)
        messages.info(request, 'Başarıyla güncelleme işleminiz gerçekleşti')
        return HttpResponseRedirect(reverse('post_detail', kwargs={'pk': form.instance.pk}))
    return render(request, 'posts/post_update.html', context={'form': form})


def post_detail(request, pk):  # unutma slug yerine ilk pk ile göndermiştik
    # post = Post.objects.get(pk=pk) #ilk kullanım pycharm kendi argüment hatsını veriyor.
    # post = get_object_or_404(Post,pk=pk)  #404 hatası veriyıor id sini bulamadığında

    try:  # id sini bulamadığında expect e düşücek.
        post = Post.objects.get(pk=pk)
        share_link = quote_plus(post.content)
        post.counter = post.counter + 1
        post.save()

    except:
        # return HttpResponse('Böyle bir sayfa bulunamadı !') #sayfa bulunamadı hatasını veriyor.
        raise Http404
    comment_form = CommentForm(data=request.POST or None)
    if request.user:
        if comment_form.is_valid():  # gelen veri doğru mu?
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            comment_form = CommentForm()  # yorum yapıldığında alanları temizler.
            messages.success(request, 'Yorum Yapıldı.')

    return render(request, 'posts/post_detail.html', context={'post': post,
                                                              'form': comment_form,
                                                              'share_link':share_link,
                                                              })


@login_required(login_url='/users/login/')
def add_child_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method =='POST':
        user = request.user
        icerik= request.POST['icerik']
        CommentChild.objects.create(user=user, comment=comment, icerik=icerik)
    return HttpResponseRedirect(reverse('post_detail' , kwargs={'pk' : comment.post.pk}))


def post_delete(request, pk):

    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.warning(request, 'Gönderi silinmiştir', extra_tags='danger')
    return HttpResponseRedirect(reverse('post_list'))


@login_required(login_url='/users/login/')
def favorite(request, pk):
    form = Post(request.POST or None)
    url = request.GET.get('next', None)
    post = get_object_or_404(Post, pk=pk)
    favori_post =FavoriteBlog.objects.filter(post=post, user=request.user)
    if favori_post.exists():

        favori_post.delete()
        messages.warning(request, 'Gönderi favorilerden çıkarılmıştır.')
    else:
        FavoriteBlog.objects.create(post=post, user=request.user)
        messages.success(request ,'Göneri favorilere eklenmiştir.')
    if not url:
        return redirect('post_detail', pk=pk)


@login_required(login_url='/users/login/')
def like(request, pk,id):
    form = Comment(request.POST or None)
    url = request.GET.get('next', None)
    comment = get_object_or_404(Comment, pk=pk)
    like_comment = CommentLike.objects.filter(comment=comment, user=request.user)

    if like_comment.exists():
        like_comment.delete()
    else:
        CommentLike.objects.create(comment=comment , user =request.user)
    if not url:
        return redirect('post_detail', pk=id)


def deneme(request):
    return render(request, 'posts/deneme.html')



def ilk(request):
    page = request.GET.get('page', 1)
    post_list= Post.objects.filter(favoriteBlog__user = request.user)


    paginator = Paginator(post_list, 4)
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'posts/favorite_2.html', context={'post_list' : post_list})



def base(request):
    return render(request, 'base.html')
