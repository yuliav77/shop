document.addEventListener('DOMContentLoaded', function() {

		var product_plus_buttons = document.querySelectorAll(".product_plus");
		var product_minus_buttons = document.querySelectorAll(".product_minus");
		var product_add_to_cart_buttons = document.querySelectorAll(".product_add_to_cart");
		var cart_list = document.querySelector("#cart_list");
		var cart_link = document.querySelector('#cart_link');
		
		var delete_buttons = document.querySelectorAll(".delete_button");
					
		var user_cart_form = document.querySelector("#user_cart_form");

		if (localStorage.cart){
			var cart_items = JSON.parse( localStorage.cart );	
				if (cart_items.length > 0){
					cart_link.innerText = cart_items.length + " items in cart";
					cart_link.style.color = "#c31363";
				}
				else if (document.documentElement.clientWidth <= 768){
					document.querySelector('#cart_link').innerText = "";
				}
		}	
		else{
			var cart_items = [];
		}	

		// MOBILE version of products list - show part of list and "load more" button	
			if (document.documentElement.clientWidth <= 768){
				$("#products_list > ul > li").slice(0, 3).show();
		
				$("#load_more").on('click', function (e) {
					e.preventDefault();
					$("#products_list > ul > li:hidden").slice(0, 3).slideDown();
					if ($("#products_list > ul > li:hidden").length == 0) {
						document.querySelector("#load_more").style.background = "#aaa6a6";
					}
				/*	$('html,body').animate({
						scrollTop: $(this).offset().top
					}, 2500);*/
				});
			}
			
		
		// MOBILE menu click
		document.querySelector('#mob_menu_button').onclick = function(el) {
			mob_menu_click()
		}
		document.querySelector('.mob_link').style.borderTop = "1px dashed #ffa9db";
		
		var mob_links = document.querySelectorAll('.mob_link');
		if (mob_links){
			[].forEach.call(mob_links, function(el) {
				el.onclick = function(e) {
					mob_menu_click()
				}			
			});
		}


		// PHONE mask 
		$("#phone").mask("+380(99)999-9999");

		// CART form SUBMIT
		if (user_cart_form){
			document.querySelector('#user_cart_form').onsubmit = () => {
				
				let cart_items_order = []
				
				for (let i = 0; i < cart_items.length; i++){
				
						let cart_item_order = {
							id: cart_items[i].id,
							count: cart_items[i].count
						}
				
					cart_items_order.push(cart_item_order);
				}
				
				let phone = document.querySelector("#phone").value;
					phone = phone.replace(/[^\d]/g, '');
				let firstname = document.querySelector("#firstname").value;
				let email = document.querySelector("#email").value;
				let sum = parseFloat(document.querySelector(".total_sum span").innerText);
				let comment = document.querySelector("#comment").value;
				
				fetch('/cart', {
					method: 'POST',
					body: JSON.stringify({
						firstname: firstname,
						phone: phone,
						email: email,
						cart_items: cart_items_order,
						sum: sum,
						comment: comment
					})
				})
				.then(response => response.json())
				.then(result => {
					alert(result["message"]);
					cart_items = [];
					localStorage.cart = JSON.stringify(cart_items);
					window.location.href = "/"
				});
				return false;
			}
		}
				
		// 	DELETE PRODUCT button (for administrator)
		if (delete_buttons){
			[].forEach.call(delete_buttons, function(el) {
				el.onclick = function(e) {
					let product_li = e.currentTarget.parentNode.parentNode; 
					var product_id = product_li.dataset.id;
					
					let confirm_delete = confirm("Are you sure you want to delete the product?");
					if (confirm_delete){
						product_li.style.display = "none";
						delete_product(product_id);
					}	
					
					return false
					
				}			
			});
		}

		
		// "ADD TO CART" button
		if (product_add_to_cart_buttons){
			[].forEach.call(product_add_to_cart_buttons, function(el) {
				el.onclick = function(e) {
					let product_buttons_div = e.currentTarget.parentNode; 
					let product_li = product_buttons_div.parentNode; 
					let product_id = product_li.dataset.id;
					let product_count = parseInt(product_buttons_div.querySelector('.product_count').innerText);
					let product_name = product_li.querySelector('.product_name_div').innerText;
					let product_price = parseFloat(product_li.querySelector('.product_price_span').innerText);
									
					let cart_item = {
							id: product_id,
							count: product_count,
							name: product_name,
							price: product_price
						}
						
					cart_items.push(cart_item);
					cart_link.innerText = cart_items.length + " items in cart";
					cart_link.style.color = "#c31363";
					
					localStorage.cart = JSON.stringify(cart_items)
					
				}			
			});
		}
		
		// Product PLUS MINUS buttons
		if (product_plus_buttons){
			[].forEach.call(product_plus_buttons, function(el) {
				el.onclick = function(e) {
					let product_buttons_div = e.currentTarget.parentNode; 
					let product_count = parseInt(product_buttons_div.querySelector('.product_count').innerText);
					product_buttons_div.querySelector('.product_count').innerText = ++product_count;
				}			
			});
		}
		
		if (product_minus_buttons){
			[].forEach.call(product_minus_buttons, function(el) {
				el.onclick = function(e) {
					let product_buttons_div = e.currentTarget.parentNode; 
					let product_count = parseInt(product_buttons_div.querySelector('.product_count').innerText);
					if (product_count > 1)
						product_buttons_div.querySelector('.product_count').innerText = --product_count;
				}			
			});
		}

		
		// CART link - show chosen products 
		if (document.location.pathname == "/cart"){
			cart_list.innerHTML = "";
			
			if (cart_items.length > 0){
				var cart_sum = 0;
				
				if (document.querySelector("#user_cart_form").style.display != "block"){
					document.querySelector(".order_button").style.display = "inline-block";				
				}	

				for (let i = 0; i < cart_items.length; i++){

					cart_sum += cart_items[i].count * cart_items[i].price;
					let tr = document.createElement('tr');
					let td_name = document.createElement('td');
						td_name.append(cart_items[i].name);
						tr.append(td_name);
					let td_amount = document.createElement('td');
						td_amount.append(cart_items[i].count, " x ", cart_items[i].price, " = ", cart_items[i].count * cart_items[i].price);
						tr.append(td_amount);
					let td_button = document.createElement('td');
					let del_cart_button	= document.createElement('button');
						del_cart_button.setAttribute("class","del_cart_button");
						del_cart_button.append("x");
						td_button.append(del_cart_button);
						tr.append(td_button);
					cart_list.append(tr);
				}	
				
				let total_sum = document.querySelector('.total_sum');
					total_sum.innerHTML = "";
				let total_sum_span = document.createElement('span');
					total_sum_span.append(cart_sum);
					total_sum.append("Total price: ",total_sum_span);
					
				
				let make_order_button = document.querySelector('.order_button');
					
				make_order_button.onclick = function(e) {
					e.currentTarget.style.display = "none";
					let user_cart_form = document.querySelector("#user_cart_form");
					user_cart_form.style.display = "block";
				}
						
		
				// DELETE ITEM FROM CART
				let del_cart_buttons = document.querySelectorAll('.del_cart_button');
				[].forEach.call(del_cart_buttons, function(el) {
					el.onclick = function(e) {
						let product_tr = e.currentTarget.parentNode.parentNode; 
						let k = e.currentTarget.parentNode.parentNode.rowIndex;
						cart_list.deleteRow(k);
						
						let total_sum_span = document.querySelector(".total_sum span").innerText;
						let total_sum = parseFloat(total_sum_span) - (cart_items[k].price * cart_items[k].count);
							if (total_sum > 0)
								document.querySelector(".total_sum span").innerText = total_sum;
							else {	
								document.querySelector(".total_sum").innerHTML = "Cart is empty!";
								document.querySelector(".order_button").style.display = "none";
								document.querySelector("#user_cart_form").style.display = "none";
								document.querySelector("#cart_link").innerText = "Cart";
							}
						cart_items.splice(k, 1);
						localStorage.cart = JSON.stringify(cart_items);
						if (cart_items.length > 0){
							cart_link.innerText = cart_items.length + " items in cart";
						}	
						else {	
							if (document.documentElement.clientWidth <= 768){
								document.querySelector('#cart_link').innerText = "";
							}
							else{
								cart_link.innerText = "Cart";
							}
							cart_link.style.color = "#00000080";
						}

						
						return false
						
					}			
				});

				
				
			}
			else {
				document.querySelector(".total_sum").innerHTML = "Cart is empty!";
				document.querySelector(".order_button").style.display = "none";
				cart_list.display = "none";
			}
			
			let opened_menu = document.querySelector(".opened");
			if (opened_menu)
				mob_menu_click();
		}
		
		
		
		
});



function delete_product(product_id){

	fetch('/admin_products/' + product_id)
	.then(response => response.json())

}



//TOGGLE BLOCK (for mobile menu click)
function getRealDisplay(elem) {
	if (elem.currentStyle) {
		return elem.currentStyle.display
	} else if (window.getComputedStyle) {
		var computedStyle = window.getComputedStyle(elem, null )

		return computedStyle.getPropertyValue('display')
	}
}

function hide(el) {
	if (!el.getAttribute('displayOld')) {
		el.setAttribute("displayOld", el.style.display)
	}
	el.style.display = "none";
}

displayCache = {}

function isHidden(el) {
	var width = el.offsetWidth, height = el.offsetHeight,
		tr = el.nodeName.toLowerCase() === "tr"

	return width === 0 && height === 0 && !tr ?
		true : width > 0 && height > 0 && !tr ? false :	getRealDisplay(el)
}

function toggle(el) {
	isHidden(el) ? show(el) : hide(el)
}


function show(el) {

	if (getRealDisplay(el) != 'none') return

	var old = el.getAttribute("displayOld");
	el.style.display = old || "";

	if ( getRealDisplay(el) === "none" ) {
		var nodeName = el.nodeName, body = document.body, display

		if ( displayCache[nodeName] ) {
			display = displayCache[nodeName]
		} else {
			var testElem = document.createElement(nodeName)
			body.appendChild(testElem)
			display = getRealDisplay(testElem)

			if (display === "none" ) {
				display = "block"
			}

			body.removeChild(testElem)
			displayCache[nodeName] = display
		}

		el.setAttribute('displayOld', display)
		el.style.display = display
	}
}



function mob_menu_click(){
		let mob_menu = document.querySelector('.navbar > div');
		let mob_menu_outer = document.querySelector(".navbar")
		let mob_menu_button = document.querySelector('#mob_menu_button');
		toggle(mob_menu);
		mob_menu_outer.classList.toggle("opened");
		mob_menu_button.style.transform == "rotate(180deg)";
		(mob_menu_button.style.transform == "rotate(180deg)") ? mob_menu_button.style.transform = "rotate(0deg)" : mob_menu_button.style.transform = "rotate(180deg)"
}



// ADD/REMOVE phone link in fixed top menu
window.onscroll = function() {
	if (document.documentElement.clientWidth > 768){
		posTop = (window.pageYOffset !== undefined) ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body).scrollTop;
		if (posTop > 150){
			document.querySelector('.phone_link').style.display = "block";
		}
		else{
			document.querySelector('.phone_link').style.display = "none";
		}
	}
}



// TOP SALES slider

$(document).ready(function(){
	hit_slider_init()
});


function hit_slider_init(){
  $('.hits_slider').slick({
	  infinite: true,
	  slidesToShow: 4,
	  slidesToScroll: 1,
	  autoplay: true,
	  autoplaySpeed: 2000,
	  responsive: [
		{
		  breakpoint: 1200,
		  settings: {
			slidesToShow: 3,
			slidesToScroll: 1
		  }
		},
		{
		  breakpoint: 600,
		  settings: {
			slidesToShow: 2,
			slidesToScroll: 1
		  }
		},
		{
		  breakpoint: 450,
		  settings: {
			slidesToShow: 1
		  }
		}
	  ]
  });

}


