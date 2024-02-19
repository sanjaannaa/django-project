from django.shortcuts import render, HttpResponse, redirect
from product.models import Product_Table, Cart_Table,CustomerDetails
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from product import models
from django.contrib import messages

# Create your views here.
def index(request):
    data = {}

    # modelname.objects.all() is used to fetch all data possible
    fetched_porducts = Product_Table.objects.filter(is_active=True)
    data['products'] = fetched_porducts
    #getting count of cart item for specific user
    user_id = request.user.id
    id_specific_cart_items = Cart_Table.objects.filter(uid=user_id)
    count = id_specific_cart_items.count()
    data['cart_count'] = count
    return render(request,'product/index.html', context=data)

def filter_by_catgory(request, category_value):
    data = {}
    q1 = Q(is_active = True)
    q2 = Q(category = category_value)
    Product_Table.objects.filter(q1 & q2)
    filtered_products = Product_Table.objects.filter(q1 & q2)
    data['products'] =  filtered_products
    return render(request,'product/index.html', context=data)

def sort_by_price(request, sort_value):
    data = {}
    if sort_value == 'asc':
        price = 'price'
    else:
        price = '-price'

    sorted_products = Product_Table.objects.filter(is_active=True).order_by(price)
    data['products'] = sorted_products
    return render(request,'product/index.html', context=data)

def sort_by_rating(request, rating_value):
    data = {}
    q1 = Q(is_active=True)
    # q2 = Q(rating__gt=rating_value) #solve this
    q3 = Q(rating__lt=rating_value)
    rating_product = Product_Table.objects.filter(q1 & q3)
    data['products']=rating_product
    print(rating_product)
    return render(request,'product/index.html', context=data)

def filter_by_price(request):
    data = {}
    min_value = request.GET['min']
    max_value = request.GET['max']
    q1 = Q(is_active = True)
    q2 = Q(price__gte = min_value)
    q3 = Q(price__lte = max_value)
    filtered_products = Product_Table.objects.filter(q1 & q2 & q3)
    data['products'] = filtered_products
    return render(request, 'product/index.html', context=data)

def details(request,pid):
    product = Product_Table.objects.get(id=pid)
    return render(request, 'product/details.html', {'product':product})

def register_user(request):
    data = {}
    if request.method == "POST":
        uname = request.POST['username']
        upass = request.POST['password']
        uconf_pass = request.POST['password2']

        if(uname == '' or upass == '' or uconf_pass == ''):
            data['error_msg']='Fields cannot be empty'
            return render(request,'users/register.html',context=data)
        
        elif(upass!=uconf_pass):
            data['error_msg']='Password doesnt match'
            return render(request,'users/register.html',context=data)
        
        elif(User.objects.filter(username=uname).exists()):
            data['error_msg']= 'user: '+uname+' already exists!'
            return render(request,'users/register.html',context=data)
        
        else:
            user = User.objects.create(username=uname)
            user.set_password(upass)
            user.save()
            customer=CustomerDetails.objects.create(uid=user)
            customer.save()
            # return HttpResponse("Registration Done!")
            return redirect('/users/login')
    return render(request,'users/register.html')

def login_user(request):
    data = {}
    if request.method=="POST":
        uname = request.POST['username']
        upass = request.POST['password']
        #implementing validation

        if(uname=='' or upass==''):
            data['error_msg']='Fields cant be empty'
            return render(request,'users/login.html',context=data)
        
        elif(not User.objects.filter(username=uname).exists()):
            data['error_msg']=uname+' user is not registered'
            return render(request,'users/login.html',context=data)
        
        else:
            user = authenticate(username=uname, password=upass)
            print(user)
            if user is not None:
                login(request,user)
                return redirect('/product/index')
            else:
                data['error_msg']='Wrong Password'
                return render(request,'users/login.html',context=data)
    return render(request,'users/login.html')

def user_logout(request):
    logout(request)
    return render(request,'product/index.html',{'user_data':"User"})

def add_to_cart(request,pid):
    if request.user.is_authenticated:
        uid = request.user.id
        print("user id=", uid)
        print("product id=", pid)
        user = User.objects.get(id = uid)
        product = Product_Table.objects.get(id = pid)
        # cart = Cart_Table.objects.create(pid=product, uid=user)
        # cart.save()

        q1 = Q(uid = pid)
        q2 = Q(pid = pid)
        available_products = Cart_Table.objects.filter(q1 & q2)
        print()
        if(available_products.count()>0):
            messages.error(request, 'Product is already added to cart.')
            return redirect('/product/index')
        else:
            cart = Cart_Table.objects.create(pid=product, uid=user)
            cart.save()
            messages.success(request, "Product is added to the cart.")
            return redirect('/product/index')
        # return redirect("/product/index/")
    else:
        return redirect("/users/login")
    
def view_cart(request):
    # checking whether user is authenticated user
    # if request.user.is_authenticated:
    #     u_data = {} #empty dictionary

    #     user_id = request.user.id
    #     user = User.objects.get(id=user_id)
    #     u_data['user_data'] = user.username
        
    #     # if(user_authenticated is True):
    #     cart_data = Cart_Table.objects.all()
    #         # print(cart_data)
    #     data = {
    #         'cart':cart_data,
    #         **u_data
    #     }
    #     return render(request, 'product/cart.html', context=data)
    #     # return render(request, 'product/cart.html', )
    if request.user.is_authenticated:
        data = {}
        user_id = request.user.id
        id_specific_cart_items = Cart_Table.objects.filter(uid=user_id)
        data['products']=id_specific_cart_items

        #counting cart items
        count = id_specific_cart_items.count()
        data['cart_count'] = count

        # counting total price
        total_price = 0
        for item in id_specific_cart_items:
            print(item.id)
            total_price+=item.pid.price
        data['total_price']=total_price

        return render(request, 'product/cart.html', context=data)
    else:
        return redirect("/users/login")
    
def remove_item(request,cid):
    cart_item = Cart_Table.objects.get(id=cid)
    # cart_item2 = Cart_Table.objects.filter(id=cid)
    print(cart_item)
    print(type(cart_item))
    print("--------------")
    # print(cart_item2)
    # print(type(cart_item2))
    cart_item.delete()
    return redirect("/product/view/")

# def quantity(request, cid):
#     cart_item = Cart_Table.objects.get(id=cid)

def update_quantity(request,flag,cartid):
    cart = Cart_Table.objects.filter(id=cartid)
    actual_quantiy = cart[0].quantity
    if(flag=="1"):
        cart.update(quantity = actual_quantiy+1)
        return redirect("/product/view/")
    else:
        if(actual_quantiy-1==0):
            remove_item(request,cartid)
            return redirect("/product/view/")
        else:
            cart.update(quantity = actual_quantiy-1)
            return redirect("/product/view/")
        
import calendar
import time    
from product.models import OrderTable   
# def place_order(request):
#     current_GMT=time.gmtime()
#     time_stamp=calendar.timegm(current_GMT)
#     user_id=request.user.id
#     oid=str(user_id)+"-"+str(time_stamp)
#     cart=Cart_Table.objects.filter(uid=user_id)
#     for data in cart:
#         order=OrderTable.objects.create(order_id=oid,quantity=data.quantity,pid=data.pid,uid=data.uid)
    
#     return HttpResponse('order placed')

def place_order(request):
    data={}
    user_id=request.user.id
    user=User.objects.get(id=user_id)
    id_specific_cartitems=Cart_Table.objects.filter(uid=user_id)
    customer=CustomerDetails.objects.get(uid=user_id)
    data['customer']=customer
    data['products']=id_specific_cartitems
    data['user']=user
    total_price=0
    total_quantity=0
    for item in id_specific_cartitems:
        total_price=(total_price+item.pid.price)*(item.quantity)
        total_quantity=item.quantity
    data['total_price']=total_price
    data['cart_count']=total_quantity
    return render(request,'product/order.html',context=data)

def edit_profile(request):
    data={}
    user_id=request.user.id
    customer_querySet=CustomerDetails.objects.filter(uid=user_id)
    customer = CustomerDetails.objects.get(uid=user_id)
    data['customer']=customer
    customer_detail = customer_querySet[0]
    # print(customer.uid)
    data['customerd']=customer_detail
    if request.method=="POST":
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        phone=request.POST['phone']
        email=request.POST['email']
        address_type=request.POST['address_type']
        full_address=request.POST['full_address']
        pincode=request.POST['pincode']
        print(first_name,last_name,phone,email,address_type,full_address,pincode)
        customer_querySet.update(first_name=first_name,last_name=last_name,phone=phone,email=email,address_type=address_type,full_address=full_address,pincode=pincode)
        return redirect('/product/index')
    return render(request,'users/edit_profile.html',context=data)

def make_payment(request):
    return HttpResponse("payment done")
            
    