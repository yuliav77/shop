import json
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django import forms

from .models import User, Product, Item, Order
from .forms import ProductForm
from django.core.mail import send_mail


def index(request):
	products = Product.objects.all()
	products = products.order_by("-id").all()
	return render(request, "shop/index.html", {'products': products})

@csrf_exempt	
def cart(request):	
	if request.method == "POST":
		data = json.loads(request.body)
		cart_items = data.get('cart_items')
		items = []
		
		for cart_item in cart_items:
			product_id = cart_item['id']
			amount = cart_item['count']
			try:
				product = Product.objects.get(id=product_id)
			except Product.DoesNotExist:
				return JsonResponse({
					"error": f"Product with id {product_id} does not exist."
				}, status=400)
			item = Item(
				product=product,
				amount=amount
			)
			item.save()
			items.append(item)
			
		sum = data.get('sum', '')
		comment = data.get('comment', '')
		phone = data.get('phone')
		email = data.get('email', '')
		first_name = data.get('firstname', '')
		
		# User is logged in
		if request.user.is_authenticated:
			customer = request.user
			customer.first_name = first_name
			customer.email = email
			customer.save()
		
		# User is not logged in
		else:	
			username = phone
			
			# Search if such user exists
			try:
				customer = User.objects.get(username=username)
				customer.first_name = first_name
				customer.email = email
				customer.save()
			except User.DoesNotExist:
				# Create a new user
				if len(first_name) == 0:
					first_name = username
				password = '123'
				customer = User(
					username=username,
					email=email,
					first_name=first_name,
					phone=phone
				)
				customer.save()
				customer.set_password(password)
				customer.save()
			#login(request, customer)
		
		# Create an order
		order = Order(
			customer=customer,
			sum=sum,
			comment=comment
		)
		order.save()
		
		# Add items to order
		for item in items:
			order.items.add(item)
		order.save()
		
		mail_message = "Order on sum " + str(sum) + " was sent (" + phone + ", " + first_name +")"
		client_mail_message = "Your " + mail_message + " to administrator!"  + '\n\r' "Have a nice day!"
		
		# Send email about new order to administrator
		send_mail(
			'New Marshmallow Order',
			mail_message,
			'Julia',
			['juliapythonproject@gmail.com'],
			fail_silently=False)
			
		# If user wrote his email - send him a message about his order
		if email:
			send_mail(
				'Marshmallow order created successfully',
				client_mail_message,
				'Julia',
				[email],
				fail_silently=False)
				
		# Send message about new order to administrator	via Telegram
		telegram_bot_sendtext("You have new marshmallow order! " + '\n\r' + mail_message)
		
		return JsonResponse({"message": "Order created successfully."}, status=201)
	else:
		return render(request, "shop/cart.html")

	
	
@csrf_exempt
@login_required
def admin_products(request):
	if request.method == "POST":
	
		# Add a new product
		form = ProductForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			clear_form = ProductForm()
			products = Product.objects.all()
			products = products.order_by("-id").all()
			return redirect("admin_products")
		else:
			return render(request, "shop/admin_products.html", {'form': form, 'message': "Form is invalid"})

	else:	
	
		# Show all products and a new product form
		clear_form = ProductForm()
		products = Product.objects.all()
		products = products.order_by("-id").all()
		return render(request, "shop/admin_products.html", {'form': clear_form, 'products': products})

		
@login_required
def edit_product(request, product_id):	
	try:
		product = Product.objects.get(id=product_id)
	except Product.DoesNotExist:
		return render(request, 'shop/edit_product.html', {'edit_form': form, "message": "Edit form is incorrect."})			
	
	if request.method == "POST":
	
		# Save information from an edit product form
		edit_form = ProductForm(request.POST, request.FILES, instance=product)
		if edit_form.is_valid():
			product = edit_form.save(commit=False)
			product.save()
			return redirect("admin_products")
		else:
			return render(request, 'shop/edit_product.html', {'edit_form': form, "message": "Edit form is incorrect."})	
			
	elif request.method == "GET":
	
		# Show an edit product form
		edit_form = ProductForm(instance=product)
		return render(request, 'shop/edit_product.html', {'edit_form': edit_form})	


@login_required
def delete_product(request, product_id):
	Product.objects.filter(id=product_id).delete()
	clear_form = ProductForm()
	products = Product.objects.all()
	return JsonResponse({"message": "Product was deleted successfully."}, status=201)


@login_required
def orders(request):
	if request.user.is_authenticated:
		if (request.user.is_staff):
			orders = Order.objects.all()
		else:
			orders = Order.objects.filter(customer=request.user)
		orders = orders.order_by("-timestamp").all()
	return render(request, "shop/orders.html", {'orders': [order.serialize() for order in orders]})

	
def login_view(request):
	if request.method == "POST":

        # Attempt to sign user in
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)

		# Check if authentication successful
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, "shop/login.html", {
				"message": "Invalid username and/or password."
			})
	else:
		return render(request, "shop/login.html")

	
def register(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]
		phone = request.POST["phone"]
		first_name = username

        # Ensure password matches confirmation
		password = request.POST["password"]
		confirmation = request.POST["confirmation"]
		if password != confirmation:
			return render(request, "shop/register.html", {
				"message": "Passwords must match."
			})

        # Attempt to create new user
		try:
			user = User.objects.create_user(username, email, password)
			user.phone = phone
			user.first_name = first_name
			user.save()
		except IntegrityError:
			return render(request, "shop/register.html", {
				"message": "Username already taken."
			})
		login(request, user)
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, "shop/register.html")


def logout_view(request):
	print("logout")
	logout(request)
	return HttpResponseRedirect(reverse("index"))
	
	
def telegram_bot_sendtext(bot_message):
    
    bot_token = '1449448561:AAHrqC6H8hUl5wJSS2hL47ROsB_Mzn3JXkY'
    bot_chatID = '723675859'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
