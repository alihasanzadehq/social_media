from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from django.contrib.auth.models import  User
from django.contrib import messages
from .forms import UserRegisterForm ,UserLoginForm , EditUserForm
from django.contrib.auth import authenticate, login, logout
from home.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse , reverse_lazy
from .models import Relation


class RegisterView(View):
    form_class = UserRegisterForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return  super().dispatch(request, *args, **kwargs)

    def get(self, request):

        form = self.form_class()
        return render(request,self.template_name,{"form":form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user=User.objects.create_user(cd["username"],cd["email"],cd["password1"])

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,user)
            messages.success(request,"You Registered Successfully", 'success')
            return  redirect('home:home')
        return render(request,self.template_name,{"form":form})


class UserLoginView(View):

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request,*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return  super().dispatch(request, *args, **kwargs)

    form_class = UserLoginForm
    template_name = 'account/login.html'
    def get(self, request):
        form = self.form_class()
        return render(request,self.template_name,{"form":form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"],password=cd["password"])
            if user is not None:
                login(request,user)
                messages.success(request,"You Loged in successfully", 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request,"username or password is wrong", 'error')
        return render(request,self.template_name,{"form":form})


class UserLogoutView(LoginRequiredMixin,View):
    # login_url = 'account/login/'
    def get(self, request):
        logout(request)
        messages.success(request,"You logged out successfully", 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin,View):
    def get(self, request,user_id):
        is_fallowing = False
        user = get_object_or_404(User,pk=user_id)
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            is_fallowing = True
        return  render(request,'account/profile.html', {'user':user, 'posts':posts,
                                                        'is_fallowing':is_fallowing})

class UserPasswordRestView(auth_views.PasswordResetView):
    template_name = 'account/password_rest_form.html'
    success_url = reverse_lazy('account:password_rest_done')
    email_template_name = 'account/password_rest_email.html'

class UserPassWordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_rest_done.html'

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/passwod_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')

class UserPasswordRestCompleteView(auth_views.PasswordResetCompleteView):
     template_name = 'account/password_reset_complete.html'


class UserFallowView(LoginRequiredMixin, View):
    def get(self, request,user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            messages.error(request,"You Already Fallowing this user", 'error')
        else :
            Relation.objects.create(from_user=request.user,to_user=user)
            messages.success(request,'You fallowed this user')
            return redirect('account:profile' , user.id)



class UserUnFallowView(LoginRequiredMixin, View):
    def get(self, request,user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request,"You UnFallow this user", "success")
        else:
            messages.error(request,"You are not fallowing this user")
        return redirect("account:profile" , user.id)

class EditUserView(LoginRequiredMixin,View):
    from_class = EditUserForm
    def get(self,request):
        form = self.from_class(instance=request.user.profile,initial={'email':request.user.email})
        return render(request, "account/edit_profile.html", {'form':form})


    def post(self,request):
        form = self.from_class(request.POST,instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request,'You edit your profile successfully','success')
        return redirect('account:profile' ,request.user.id)

