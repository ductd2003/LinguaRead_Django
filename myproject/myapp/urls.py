from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_posts_list, name='list-posts'),
    path('manager/admin-login/', views.admin_login, name='admin_login'),
    path('manager/dashboard/', views.dashboard, name='dashboard'),
    path('manager/manage-post/', views.manage_post, name='manage_post'),
    path('manager/manage-post/<int:post_id>/publish/', views.publish_post, name='publish_post'),
    path('manager/manage-post/<int:post_id>/revert/', views.revert_to_draft, name='revert_to_draft'),
    path('manager/update_image/<int:post_id>/', views.update_image, name='update_image'),
    path('manager/manage-level/', views.levels_list, name='levels_list'),
    path('manager/manage-level/save/', views.levels_save, name='levels_save'),
    path('manager/manage-language/', views.languages_list, name='languages_list'),
    path('manager/manage-language/save/', views.languages_save, name='languages_save'),
    path('manager/manage-postcontent/', views.postcontent_list, name='postcontent_list'),
    path('manager/manage-postcontent/save/', views.postcontent_save, name='postcontent_save'),
    path('manager/postcontent/<int:pk>/', views.manage_postcontent_detail, name='manage_postcontent_detail'),
    path('manager/manage-question/', views.question_manager, name='question_manager'),
    path('manager/admin-logout',views.admin_logout,name='admin_logout'),
    path('user/post-detail/', views.user_post_detail, name='post_detail'),
    path('user/about-us', views.about_us, name='about_us')
]
