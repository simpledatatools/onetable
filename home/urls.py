from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('about/', views.about, name='about'),
    path('organizations/', views.organizations, name='organizations'),
    path('organizations/add/', views.add_organization, name='add_organization'),
    path('organizations/<organization_pk>/settings/', views.organization_settings, name='organization_settings'),
    path('organizations/<organization_pk>/edit/', views.edit_organization, name='edit_organization'),
    path('organizations/<organization_pk>/archive/', views.archive_organization, name='archive_organization'),
    path('organizations/<organization_pk>/apps/', views.apps, name='apps'),
    path('organizations/<organization_pk>/apps/add/', views.add_app, name='add_app'),
    path('organizations/<organization_pk>/apps/<app_pk>/', views.app_details, name='app_details'),
    path('organizations/<organization_pk>/apps/<app_pk>/settings/', views.app_settings, name='app_settings'),
    path('organizations/<organization_pk>/apps/<app_pk>/edit/', views.edit_app, name='edit_app'),
    path('organizations/<organization_pk>/apps/<app_pk>/archive/', views.archive_app, name='archive_app'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/', views.lists, name='lists'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/create-list/', views.create_list, name='create_list'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/', views.list, name='list'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/edit/', views.edit_list, name='edit_list'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/settings/', views.list_settings, name='list_settings'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/archive/', views.archive_list, name='archive_list'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/add-record/', views.add_record, name='add_record'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/save-record/', views.save_record, name='save_record'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/records/<record_pk>/', views.record, name='record'), # Forward without details to details
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/records/<record_pk>/details/', views.record_details, name='record_details'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/records/<record_pk>/details/post_comment/', views.post_record_comment, name='post_record_comments'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/records/<record_pk>/details/post_file/', views.post_record_file, name='post_record_file'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/records/<record_pk>/details/delete_comment/<record_comment_pk>/', views.delete_record_comment, name='delete_record_comment'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/records/<record_pk>/details/edit_comment/<record_comment_pk>/', views.edit_record_comment, name='edit_record_comment'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/records/<record_pk>/details/delete_file/<record_file_pk>/', views.delete_record_file, name='delete_record_file'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/records/<record_pk>/details/edit_file/<record_file_pk>/', views.edit_record_file, name='edit_record_file'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/records/<record_pk>/links/', views.record_links, name='record_links'),
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/records/<record_pk>/edit/', views.edit_record, name='edit_record'),

    path('organizations/<organization_pk>/apps/<app_pk>/dashboard/', views.dashboard, name='dashboard'),

   
    path('organizations/<organization_pk>/apps/<app_pk>/lists/<list_pk>/record/<record_pk>/', views.archive_record, name='archive_record'),
]
