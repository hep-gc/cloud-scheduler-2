from django.conf.urls import url

from . import views, user_views, cloud_views, group_views

urlpatterns = [
    url(r'^user/create', user_views.create, name='create'),
    url(r'^user/delete', user_views.delete, name='delete'),
    url(r'^user/list', user_views.manage, name='manage'),
    url(r'^user/update', user_views.update, name='update'),

    url(r'^clouds/',       cloud_views.list,    name='list'),
    url(r'^cloud/prepare', cloud_views.prepare, name='prepare'),
    url(r'^$',             cloud_views.status,  name='list'),
    url(r'^status/',       cloud_views.status,  name='status'),
    url(r'^cloud/update',  cloud_views.update,  name='update'),

    url(r'^groups/', group_views.list, name='list'),
    url(r'^group/update', group_views.update, name='update'),

]
