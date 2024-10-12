from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path("register", views.RegisterView.as_view() , name="register", ),
    path("login/", views.UserLoginView.as_view() , name="login", ),
    path("logout/", views.UserLogoutView.as_view() , name="logout", ),
    path('profile/<int:user_id>/',views.UserProfileView.as_view() , name="profile",),
    path('reset', views.UserPasswordRestView.as_view() , name="reset_password",),
    path('reset/done/', views.UserPassWordResetDoneView.as_view() , name="password_rest_done",),
    path('confirm<uidb64><token>/', views.UserPasswordResetConfirmView.as_view() , name="password_reset_confirm",),
    path('reset/complete/', views.UserPasswordRestCompleteView.as_view() , name="password_reset_complete",),
    path('fallow/<int:user_id>',views.UserFallowView.as_view() , name="fallow"),
    path('unfallow/<int:user_id>',views.UserUnFallowView.as_view() , name="unfallow"),
    path('edit_user', views.EditUserView.as_view() , name="edit_user",),


]