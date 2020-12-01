# Final project - Capstone

Marshmallow Online Shop

## Description

File name  		 	   				| Content
------------------------------------|----------------------
db.sqlite3							| The created database 
manage.py							| Django's command-line utility for administrative tasks
/final/								| Project folder
	settings.py						| Project configuration
	urls.py							| The root URL configuration of the project
	wsgi.py							| WSGI config for the project
	asgi.py							| ASGI config for the project
/media/pic_folder/						| Folder for products images
/media/pic_folder/None/no-img.jpg 				| Default image for products created without image
/shop/								| Application folder
	views.py						| Functions file
	urls.py							| The URL configuration of the application
	models.py						| Database structure file
	forms.py						| File where form classes for the project are defined
	apps.py							| Application configuration
	admin.py						| Admin module configuration
/shop/templates/shop						| Templates  folder
	layout.html 						| Template for other pages (including head,header,footer sections)
	index.html      					| Main page 
	cart.html       					| Cart page
	login.html  						| login page
	register.html   					| Page for user registration
	orders.html						| Page where authorized user can see all his orders, administrator can see ALL orders of all users
	admin_products.html					| Administrator page for adding new products, deleting products - accessible only for users with "is_staff" role
	edit_product.html					| Administrator page for editing products - accessible only for users with "is_staff" role
shop/static/shop/css						| CSS folder
	styles.css     						| CSS stylesheet for desktop
	media.css						| CSS stylesheet for mobile devices
	script.js						| Script file 
	/img/							| Folder for images
	/slick/							| Slick Slider folder for initialisation of Top Sales Carousel on the main page
	
	
## Usage

Both authorized/nonauthorized user is able to make an order. While sending order nonauthorized user should write a phone number (it's required field). 
As nonauthorized user has submitted the order, a new user is being made in database, with username equal specified phone number and password equal "123". If such user has already existed, an order is being attached to this user.
Administrator receives message about new order via Telegram and email. User receives email about his order (if he has specified email address while making order).
In order to get access to administrator tools (managing products) please log in using "administrator"/"qwerty" (user name/password)

This project is also loaded to http://juliavozovikova.pythonanywhere.com/
