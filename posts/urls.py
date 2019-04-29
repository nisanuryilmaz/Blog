from django.conf.urls import url
from .views import post_list, post_create, post_delete, post_detail, post_update, form_ornek, \
    deneme, base, tag_create, favorite, fav, ilk, add_child_comment , like , tag_delete

urlpatterns = [
    url(r'^$', view=post_list, name='post_list'),
    url(r'^detail/(?P<pk>[0-9]+)/$', view=post_detail, name='post_detail'),
    url(r'^add_child_comment/(?P<pk>\d+)/$', view=add_child_comment, name='add_child_comment'),
    url(r'^create/$', view=post_create, name='post_create'),
    url(r'^delete/(?P<pk>[0-9]+)/$', view=post_delete, name='post_delete'),
    url(r'^update/(?P<pk>[0-9]+)/$', view=post_update, name='post_update'),
    url(r'^form/$', view=form_ornek),
    url(r'^deneme/$', view=deneme),
    url(r'^base/$', view=base),
    url(r'^tag_cretae/$', view=tag_create, name='tag_create'),
    url(r'^tag_delete/(?P<pk>[0-9]+)/$', view=tag_delete, name='tag_delete'),
    url(r'^favorite/(?P<pk>[0-9]+)/$', view=favorite, name='favorite'),
    url(r'^like/(?P<pk>[0-9]+)/comment/(?P<id>[0-9]+)/$', view=like, name='like'),
    url(r'^fav/(?P<pk>[0-9]+)/$', view=fav, name='fav'),
    url(r'ilk/$', view=ilk, name='ilk'),
]
