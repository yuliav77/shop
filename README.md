# Final project - Capstone

Marshmallow Online Shop

## Description

File name  		 	   				| Content
----------------------------------------------------------------|----------------------
db.sqlite3							| The created database 
manage.py							| Django's command-line utility for administrative tasks
final/								| Project folder
final/settings.py						| Project configuration
final/urls.py							| The root URL configuration of the project
final/wsgi.py							| WSGI config for the project
final/asgi.py							| ASGI config for the project
media/pic_folder/						| Folder for products images
media/pic_folder/None/no-img.jpg 				| Default image for products created without image
shop/								| Application folder
shop/views.py							| Functions file
shop/urls.py							| The URL configuration of the application
shop/models.py							| Database structure file
shop/forms.py							| File where form classes for the project are defined
shop/apps.py							| Application configuration
shop/admin.py							| Admin module configuration
shop/templates/shop						| Templates  folder
shop/templates/shop/layout.html 				| Template for other pages (including head,header,footer sections)
shop/templates/shop/index.html      				| Main page 
shop/templates/shop/cart.html       				| Cart page
shop/templates/shop/login.html  				| login page
shop/templates/shop/register.html   				| Page for user registration
shop/templates/shop/orders.html					| Page where authorized user can see all his orders, administrator can see ALL orders of all users
shop/templates/shop/admin_products.html				| Administrator page for adding new products, deleting products - accessible only for users with "is_staff" role
shop/templates/shop/edit_product.html				| Administrator page for editing products - accessible only for users with "is_staff" role
shop/static/shop/css						| CSS folder
shop/static/shop/styles.css     				| CSS stylesheet for desktop
shop/static/shop/media.css					| CSS stylesheet for mobile devices
shop/static/shop/script.js					| Script file 
shop/static/shop/img/						| Folder for images
shop/static/shop/slick/						| Slick Slider folder for initialisation of Top Sales Carousel on the main page
	
	
## Usage

Both authorized/nonauthorized user is able to make an order. While sending order nonauthorized user should write a phone number (it's required field). 
As nonauthorized user has submitted the order, a new user is being made in database, with username equal specified phone number and password equal "123". If such user has already existed, an order is being attached to this user.
Administrator receives message about new order via Telegram and email. User receives email about his order (if he has specified email address while making order).
In order to get access to administrator tools (managing products) please log in using "administrator"/"qwerty" (user name/password)

This project is also loaded to http://juliavozovikova.pythonanywhere.com/
