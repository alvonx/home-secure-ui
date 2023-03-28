from django.contrib import messages,auth
from django.shortcuts import render,redirect
from accounts.forms import RegistrationForm
from accounts.models import Account
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests
from carts.models import Cart, CartItem
from carts.views import _cart_id

# User Registration Functionality !
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split("@")[0]
            confirm_password =form.cleaned_data['confirm_password']
            print(confirm_password)
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            user.phone_number=phone_number
            user.save()
            #  user activation
            current_site = get_current_site(request)
            mail_subject ="please activate your account"
            message =render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Account Createed successfully! please check your email ad verify your account')
            return redirect('login')
    else:
        form = RegistrationForm()
    context={
        'form':form,
    }
    return render(request,'accounts/register.html',context)

# User Registration Activation Link Functionality !
def activate(request,uidb64,token):
    try:
        uid =urlsafe_base64_decode(uidb64).decode()
        user =Account._default_manager.get(pk =uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user =None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active =True
        user.save()
        messages.success(request,'Congratulations your account is activated')
        return redirect('login')
    else:
        messages.error(request,"Invalid activation link")   
        return redirect('register')

# User Logout Functionality !
@login_required(login_url ='login')
def logout(request):
    auth.logout(request)
    messages.warning(request,'Logged Out , Successfully !')
    return redirect('login')

# User Login Functionality !
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        email =request.POST.get('email')
        password =request.POST.get('password')
        

       
        user= auth.authenticate(email=email,password=password)
        if user is not None:
            try:
                cart=Cart.objects.get(cart_id =_cart_id(request))
                is_cart_item_exist =CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exist:
                    cart_item =CartItem.objects.filter(cart=cart)

                    product_variation=[]
                    for item in cart_item:
                        variation =item.variations.all()
                        product_variation.append(list(variation))


                    cart_item =CartItem.objects.filter(user=user)
                    ex_var_list=[]
                    id =[]

                    for item in cart_item:
                        existing_variation =item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index=ex_var_list.index(pr)
                            item_id =id[index]
                            item =CartItem.objects.get(id = item_id)
                            item.quantity += 1
                            item_user =user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user =user
                                item.save()

            except:
                pass
            auth.login(request,user)
            url =request.META.get('HTTP_REFERER')
            try:
                query =requests.utils.urlparse(url).query
                params =dict(x.split('=') for x in query.split('&'))

                if 'next' in params:
                    nextpage =params['next']
                    return redirect(nextpage)
            except:
                return redirect('home')
        else:
            messages.error(request,"username or password does not exist")

            return redirect('login')
    context={
        
    }

    return render(request,'accounts/login.html',context)

# User Forget Password Functionality !
def forgetpassword(request):
    if request.method =="POST":
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact =email)

            current_site = get_current_site(request)
            mail_subject ="Please reset your password"
            message =render_to_string('accounts/reset_password.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email =email
            send_email =EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password reset mail has been sent your Mail !')
            return redirect('login')

        else:
            messages.error(request,'Account does not exist !')
            return redirect('forgetpassword')

    return render(request,"accounts/forgetpassword.html")

# User Reset Password Link Functionality !
def resetpassword_validate(request,uidb64,token):
    try:
        uid =urlsafe_base64_decode(uidb64).decode()
        user =Account._default_manager.get(pk =uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user =None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please reset your password...')
        return redirect('resetpassword')
    else:
        messages.error(request,'This link has been expired !')
        return redirect ('login')

# User Reset Password Functionality !
def resetpassword(request):
    if request.method =="POST":
        password =request.POST['password']
        confirm_password =request.POST['confirm_password']

        if password == confirm_password:
            uid =request.session.get('uid')
            user =Account.objects.get(pk =uid)
            user.set_password(password)
            user.save()
            messages.success(request,'password reset successfull')
            return redirect('login')
        else:
            messages.error(request,'Password do not match')
            return redirect('resetpassword')
    return render(request,'accounts/resetpassword.html')