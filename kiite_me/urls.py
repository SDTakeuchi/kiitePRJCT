
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from km.views import homeView, loginView, signupView, logoutView, indexView,showView, newView, editView, deleteCommentView, deleteView, commentView, userListView, userMypageView, userMypageEditView, termsOfUseView, privacyPolicyView, contactFormView, userDeleteView, commentBackView, adminNotificationView, crop_image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homeView, name='home'),

    path('signup/', signupView, name='signup'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),

    path('posts/index/', indexView, name='postIndex'),
    path('posts/new/', newView, name='postNew'),
    path('posts/show/<str:pk>', showView, name='postShow'),
    path('posts/edit/<str:pk>', editView, name='postEdit'),
    path('posts/comment/<str:pk>', commentView, name='postComment'),
    path('posts/comment/delete/<str:pk>', deleteCommentView, name='postCommentDelete'),
    path('posts/delete/<str:pk>', deleteView, name='postDelete'),
    path('posts/comment/back/<str:pk>', commentBackView, name='postCommentBack'),

    path('user/list/<str:pk>', userListView, name="userList" ),  #######################
    path('user/mypage/', userMypageView, name="mypage" ),
    path('user/mypage/edit/', userMypageEditView, name="mypageEdit" ),
    path('user/delete_user_data', userDeleteView, name="userDelete" ),
    path('<user_id>/edit/cropImage/', crop_image, name="crop_image" ),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset/password_reset_sent.html"), name="password_reset_complete"),

    path('policies/terms_of_use/', termsOfUseView, name="terms_of_use"),
    path('policies/privacy_policy/', privacyPolicyView, name="privacy_policy"),

    path('contact/form/', contactFormView, name="contactForm"),
    path('staff_only/', adminNotificationView, name="adminNotificationForm"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)