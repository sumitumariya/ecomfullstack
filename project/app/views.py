from django.shortcuts import render,redirect
from .models import Product, AddItem
from django.conf import settings
from project.settings import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

# Create your views here.
def Index(request):
    # addtocart = request.session.get('addtocart')
    
  
    return render(request,'index.html')

def About(request):
    # addtocart = request.session.get('addtocart')
   
    
    return render(request,'about.html')

def AddProduct(request):
    # addtocart = request.session.get('addtocart')
    
    
    return render(request,'Additem.html')


def Productdata(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.FILES.get('img')

        AddItem.objects.create(Name = name,
                                 Price = price,
                                  Image = image)
        
        addtocart = request.session.get('addtocart')
        
        return render(request,'AddItem.html')

def allProduct(request):
    item = AddItem.objects.all()
    addtocart = request.session.get('addtocart')
    
   
    return render(request,'Products.html',{'item':item, 'media_url':settings.MEDIA_URL})
  


def AddToCart(request,pk):
    if request.method == "POST":
        
        
        addtocart = request.session.get('addtocart',[])
        addtocart.append(pk)
        request.session['addtocart'] = addtocart   # for again put change value in session
     
        return redirect('Product')
    
def Cart(request):
    addtocart = request.session.get('addtocart')
    
    Cartdetails = []
    TotalAmount = 0
  
    for i in addtocart:
        data = AddItem.objects.get(id=i)
        
        
        context={
            'id':data.id,
            'Nm':data.Name,
            'Pr':data.Price,
            'Img':data.Image,
            
        }
        TotalAmount+=data.Price
        Cartdetails.append(context)
    return render(request,'Cart.html',{'Cartdetails':Cartdetails,'media_url':settings.MEDIA_URL,'TotalAmount':TotalAmount })

def Delete(request,pk):
    addtocart = request.session.get('addtocart')
    
    addtocart.remove(pk)
    request.session['addtocart'] = addtocart
    
    Cartdetails = []
    TotalAmount = 0
   
    
    for i in addtocart:
        data = AddItem.objects.get(id=i)
        context={
            'id':data.id,
            'Nm':data.Name,
            'Pr':data.Price,
            'Img':data.Image,
        }
        TotalAmount+=data.Price
        Cartdetails.append(context)
    return render(request,'Cart.html',{'Cartdetails':Cartdetails,'media_url':settings.MEDIA_URL,'TotalAmount':TotalAmount})


def Payment(request):
    global payment
    amount = int(request.POST.get('amount'))
    amunts=amount*100

    client = razorpay.Client(auth=("rzp_test_CEScT0iMoToG7A","Jy8sqnJJ7jSOphGRxdSe3Iag"))

    data = { "amount": amunts, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)

    Product.objects.create(amount=amount, order_id=payment['id'])

    addtocart = request.session.get('addtocart')
    Cartdetails = []
    TotalAmount = 0
  
    for i in addtocart:
        data = AddItem.objects.get(id=i)
        context={
            'id':data.id,
            'Nm':data.Name,
            'Pr':data.Price,
            'Img':data.Image,
        }
        TotalAmount+=data.Price
        Cartdetails.append(context)
    return render(request,'Cart.html',{'Cartdetails':Cartdetails,'media_url':settings.MEDIA_URL,'TotalAmount':TotalAmount,'payment':payment})


@csrf_exempt
def payment_status(request):
    if request.method == "POST":
        response = request.POST

        razorpay_data = {
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_signature': response['razorpay_signature']
        }

        # client instance
        client = razorpay.Client(auth =("rzp_test_3LJ7CBlMbFfwT" , "4thIATbNrfvi0N6mdFDThupO"))

        try:
            status = client.utility.verify_payment_signature(razorpay_data)
            product = Product.objects.get(order_id=response['razorpay_order_id'])
            product.razorpay_payment_id = response ['razorpay_payment_id']
            product.paid = True
            product.save()
            
            return render(request, 'success.html', {'status': True})
        except:
            return render(request, 'success.html', {'status': False})


def Contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('msg')

        # addtocart = request.session.get('addtocart')
       

         #  For mail    
        name = name
        subject='mail from user contact'
        message=message
        from_email="sumitumariya11@gmail.com"
        recipient_list=['sumitumariya11@gmail.com ']
        # recipient_list=['sumitumariya11@gmail.com ','arpitkhare14@gmail.com']
        send_mail(subject, message, from_email, recipient_list)

    return render(request,'Contact.Html')
