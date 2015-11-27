from django.conf.urls import url
from restaurants import views

app_name = 'restaurants'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/?', views.signup, name='signup'),
    url(r'^login/?', views.login, name='login'),
    url(r'^register/?', views.register, name='register'),
    url(r'^activation/?', views.activation, name='activation'),
    url(r'^activate/(?P<uid>.+)/(?P<token>.+)/?', views.activate, name='activate'),
    url(r'^profile/?', views.profile, name='profile'),
    url(r'^status-check/?', views.StatusCheck.as_view(), name='status-check'),
]
