from gettext import Catalog
from unicodedata import category
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
# from numpy import product
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm, RequestForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self, request):
        totalitem = 0
        gaming = Product.objects.filter(category='G')
        apple = Product.objects.filter(category='A')
        accessories = Product.objects.filter(category='C')

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'gaming': gaming, 'apple': apple, 'accessories': accessories, 'totalitem': totalitem })

 



class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

            item_already_in_cart = Cart.objects.filter(Q(product=product.id)&Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart' :item_already_in_cart,'totalitem':totalitem})


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user = user, product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 5.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        #print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount':totalamount, 'amount' :amount, 'totalitem':totalitem})
        else: 
            return render(request, 'app/emptycart.html',{'totalitem':totalitem})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
       
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 5.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.price)
            amount += tempamount
            

        data = {
            'quantity': c.quantity,
            'amount' :amount,    
            'totalamount': amount + shipping_amount
        }
        return  JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
       
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 5.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.price)
            amount += tempamount
            

            data = {
            'quantity': c.quantity,
            'amount' :amount,    
            'totalamount': amount + shipping_amount
        }
        return  JsonResponse(data)

def remove_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    amount = 0.0
    shipping_amount = 5.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
       tempamount = (p.quantity * p.product.price)
       amount += tempamount
      

    data = {
      'amount':amount,
      'totalamount':amount + shipping_amount
      }
    return JsonResponse(data)







def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

@login_required
def orders(request):
    totalitem =0
    totalitem = len(Cart.objects.filter(user=request.user))
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':op,'totalitem':totalitem})



def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category = 'G')
    elif data == 'Lenovo' or data == 'Acer':
        mobiles = Product.objects.filter(category='G').filter(brand=data)
    elif data == 'below' :
        mobiles = Product.objects.filter(category='G').filter(price__lt=1300)
    elif data == 'above' :
        mobiles = Product.objects.filter(category='G').filter(price__gt=1299)
    return render(request, 'app/mobile.html', {'mobiles' :mobiles})


def apple(request, data=None):
    if data == None:
        apple = Product.objects.filter(category = 'A')
    elif data == 'Mac' or data == 'Macpro':
        apple = Product.objects.filter(category='A').filter(brand=data)
    elif data == 'below' :
        apple = Product.objects.filter(category='A').filter(price__lt=1300)
    elif data == 'above' :
        apple = Product.objects.filter(category='A').filter(price__gt=1299)
    return render(request, 'app/apple.html', {'apple' :apple})


def acc(request, data=None):
    if data == None:
        acc = Product.objects.filter(category = 'C')
    elif data == 'Rapoon' or data == 'Transcend':
        acc = Product.objects.filter(category='C').filter(brand=data)
    elif data == 'below' :
        acc = Product.objects.filter(category='C').filter(price__lt=50)
    elif data == 'above' :
        acc = Product.objects.filter(category='C').filter(price__gt=49)
    return render(request, 'app/acc.html', {'acc' :acc})






class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form })

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'User Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form })




def Request(request):
    form = RequestForm
    if request.method=='POST':
        requestForm = RequestForm(request.POST)
        if requestForm.is_valid():
            
            messages.success(request, 'Form has been submitted.. Thank you')
            requestForm.save()
            return redirect('/request')
    return render(request, 'app/request.html',{'form':form})







@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 5.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.price)
            amount += tempamount
            totalamount= amount + shipping_amount

    return render(request, 'app/checkout.html', {'add':add, 'totalamount' :totalamount, 'cart_items':cart_items})


@login_required
def paymentdone(request):
    user = request.user
    custid = request.GET.get('custid')
    customer= Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product = c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")






@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            number = form.cleaned_data['number']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            reg = Customer(user= usr,name=name, number=number, city=city, state=state)
            reg.save()
            messages.success(request, 'Congratulations!!! Profile Updated Successfully')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
    






def search(request):
    if request.method == "POST":
        
        searched = request.POST.get('searched')
        searc = Product.objects.filter(title__contains = searched)
        return render(request, 'app/search.html',{'searched':searched, 'searc':searc})
    else:
        return render(request, 'app/search.html',{})


