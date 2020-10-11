from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from app.models import UserModel,Refferal,Product,ProductLink
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import random
import string
# from django.db import DoesNotExist
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.



class DashboardView(View):

    template_name = "dashboard.html"
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        return redirect('login')


    def post(self, request):
        name = request.POST['name']
        price = request.POST['price']

        product = Product.objects.create(name=name,price=price,created_by=request.user)
        return redirect('products')



class SignUpView(View):
    template_name = "sign-up.html"
    
    def get(self, request):
        return render(request, self.template_name)
        
    def post(self, request):
        print(request.POST)
        name = request.POST['username']
        email = request.POST['email']
        if UserModel.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,'email already exists, please try login.')
            return render(request, self.template_name)
        
        user = UserModel.objects.create(username=name,email=email)
        user.username = user.email
        user.set_password(user.email)

        refferal_code = request.POST['code']
        if not refferal_code == '':
            try:
                check_code = Refferal.objects.get(code=refferal_code)
                if check_code.is_expired:
                    messages.add_message(request,messages.ERROR,'Refferal code is expired')
                    return redirect('signup')
                else:
                    owner = check_code.user
                    owner.wallet += 10.00
                    user.wallet += 100.00
                    check_code.is_expired = True
                    owner.save()
                    check_code.save()
            except ObjectDoesNotExist:
                messages.add_message(request,messages.ERROR,'Refferal code does not exist')
                return redirect('signup')
        user.save()
        login(request,user)
        return redirect('dashboard')


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)
        

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username= email, password= password)
        if user and user is not None:
            login(request,user)
            return redirect('dashboard')

        else:
            messages.error(request,"Wrong credentials!")
            return redirect('login')


def Logout(request):
    logout(request)
    return redirect('login')


class ShareAppView(View):

    template_name = "share.html"
    def get(self, request):
        code = Refferal.objects.create(code=get_random_string(8).upper(), user=request.user)
        context = {'refferal_code':code}
        return render(request, self.template_name,context)
        


class Products(View):
    template_name = "products.html"

    def get(self, request):
        products = Product.objects.all().order_by('-id')
        context = {'products':products}
        return render(request,self.template_name,context)

class ProductDetailView(View):
    template_name = "product-detail.html"

    def get(self, request, pk):
        if (type(pk)) == int:
            try:
                product = Product.objects.get(id=pk)
                return render(request,self.template_name,{'product':product,'pk':pk})
            except ObjectDoesNotExist:
                return HttpResponse('Product does not exist');
        else:
            try:
                print(pk)
                link = ProductLink.objects.get(generated_link=pk.lower())
                return render(request, self.template_name, {'product': link.product,'pk':pk})
            except ObjectDoesNotExist:
                return HttpResponse('Product does not exist')


class ShareProduct(View):
    template_name = "share-product.html"
    
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        try:
            link = ProductLink.objects.get(product=product, created_by=request.user)
        except ObjectDoesNotExist:
            link = ProductLink.objects.create(product=product, created_by=request.user,generated_link=get_random_string(48))
        context = {'id':link.product.id,'link':f"http://127.0.01:8000/product/{link.generated_link}",'commision':(link.product.price*0.2)/100}
        return render(request,self.template_name,context)


class Buy(View):
    def get(self, request, pk):
        user = request.user
        
        if (type(pk)) == int:
            try:
                product = Product.objects.get(id=pk)
                user.wallet -= product.price
                user.save()
                return redirect('dashboard')
            except ObjectDoesNotExist:
                return HttpResponse('Product does not exist');
        else:
            try:
                link = ProductLink.objects.get(generated_link=pk)
                product = link.product  
                user.wallet -= product.price
                reffer_person = link.created_by
                reffer_person.wallet += (product.price * 2) / 100
                user.save()
                reffer_person.save()
                return redirect('dashboard')
            except ObjectDoesNotExist:
                return HttpResponse('Product does not exist')



def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str