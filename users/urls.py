from django.conf.urls import url
from .views import user_create,user_login,user_logout,user_edit_profile,password_change,user_update_photo

urlpatterns = [
    url(r'^create/$', view=user_create, name='user_create'),
    url(r'^login/$' , view = user_login , name='user_login'),
    url(r'^logout/$' , view=user_logout , name='user_logout'),
    url(r'^edit/$' , view=user_edit_profile, name='user_edit_profile'),
    url(r'^password_change/$' , view=password_change , name='password_change'),
    url(r'^user_update_photo/$' , view=user_update_photo , name='user_update_photo')

]