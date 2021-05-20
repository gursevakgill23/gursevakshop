from django.shortcuts import render, HttpResponse,HttpResponseRedirect,redirect
from datetime import datetime
from .models.product import Product
from django.contrib import messages
from .models.customer import Customer
from .models.category import Categories
from .models.contact import Contact
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from .models.orders import Order
from MyApp.middlewares.middleware import auth_middleware
from MyApp.middlewares.cart_middleware import auth_middleware1


def index(request):
    if request.method == "POST":
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect("/")

    #products=Product.get_all_products()
    #return render(request,"index.html",{'products':products})
    if request.method=='GET':
        products = None
        categories = Categories.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()

        data = {}
        data['products'] = products
        data['categories'] = categories

        print('you are : ', request.session.get('email'))
        return render(request, 'index.html', data)
def register(request):
    error_message = None
    if request.method=='GET':
        return render(request, 'register.html')
    elif request.method=='POST':
        first_name=request.POST.get('fname')
        last_name = request.POST.get('lname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password=request.POST.get('password')
        customer = Customer(fname=first_name,
                            lname=last_name, phone=phone, email=email, password=password)
        #Validate
        if not first_name:
            error_message="First Name Required"
        elif len(first_name) < 4:
            error_message="Length of First Name shouldn't be less than 4.."
        elif not last_name:
            error_message="Last Name Required"
        elif len(last_name) < 4:
            error_message = "Length of Last Name shouldn't be less than 4.."
        elif not phone:
            error_message="Phone Number Required"
        elif len(phone) < 10:
            error_message = "Length of Phone Number shouldn't be less than 10.."
        elif customer.isExists():
            error_message = "Email already Registered"

        if not error_message:            
            customer.password=make_password(customer.password)

            customer.save()
            messages.success(request,'Your Account has been successfully created')
        else:
            return render(request, 'register.html', {'error': error_message})
    return redirect('login')

def login(request):
    return_url = None

    if request.method=='GET':
        return_url = request.GET.get('return_url')
        return render(request,'login.html')
    elif request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if return_url:
                    return HttpResponseRedirect(return_url)
                else:
                    return_url = None
                    return redirect('/')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'
        return render(request, 'login.html', {'error': error_message})
def about(request):
    return render(request,'about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        contact = Contact(name=name, phone=phone, email=email,
                          desc=desc, date=datetime.today())
        
        contact.save()
        messages.success(request, 'Your message has been sent')

    return render(request, 'contact.html')


def logout(request):
    request.session.clear()
    return redirect('/login')


@auth_middleware1
def cart(request):
    ids = list(request.session.get('cart').keys())
    products = Product.get_products_by_id(ids)
    print(products)
    return render(request, 'cart.html', {'products': products})
    



def checkout(request):
    if request.method=="POST":
        cart=request.session.get('cart')
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        customer=request.session.get('customer')
        products=Product.get_products_by_id(list(cart.keys()))
        for product in products:
            order = Order(customer=Customer(id=customer),
                        product=product,
                        price=product.price,
                        address=address,
                        phone=phone,
                        quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart']={}
    return redirect('cart')
@auth_middleware
def orders(request):
    customer=request.session.get('customer')
    orders=Order.get_orders_by_customer(customer)
    return render(request,'orders.html',{'orders':orders})
