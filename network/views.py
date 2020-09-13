import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import User, Post
	

def index(request):
	return render(request, "network/index.html")

@csrf_exempt	
def posts_view(request):

	# Add new post
	if request.method == "POST":
		if request.user.is_authenticated:
			data = json.loads(request.body)
			post_text = data.get("post_text", "")
			likes_counter = 0
			author = request.user
			post = Post(
				author=author,
				text=post_text,
				counter=likes_counter
			)
			post.save()
			return JsonResponse({"message": "Post created successfully."}, status=201)
	
	# Show all posts
	else:
		posts = Post.objects.all()
		posts = posts.order_by("-timestamp").all()
		page = request.GET.get('page', 1)
		paginator = Paginator(posts, 10)
		num_pages = paginator.num_pages
		try:
			page_posts = paginator.page(page)
		except PageNotAnInteger:
			page_posts = paginator.page(1)
		except EmptyPage:
			page_posts = paginator.page(num_pages)
		
		number = page_posts.number
		
		data = {
			'previous_page': page_posts.has_previous() and page_posts.previous_page_number() or None,
			'next_page': page_posts.has_next() and page_posts.next_page_number() or None,
			'num_pages': num_pages,
			'number': page_posts.number,
			'data': list(post.serialize() for post in page_posts)
		}	
		return JsonResponse(data, safe=False)

@csrf_exempt
@login_required	
def user_view(request, user_name):		

	try:
		user = User.objects.get(username=user_name)
	except User.DoesNotExist:
		return JsonResponse({"error": "User not found."}, status=404)	
		
	# Show user info	
	if request.method == "GET":
		return JsonResponse(user.serialize())

	# Change(add or remove) followers/following
	elif request.method == "PUT":
		data = json.loads(request.body)
		who_follow = data.get("who_follow")
		try:
			current_user = User.objects.get(username=who_follow)
		except User.DoesNotExist:
			return JsonResponse({"error": "User not found."}, status=404)	
		
		follow_flag = data.get("follow_flag")
		
		if follow_flag:
			user.followers.remove(current_user)
			current_user.following.remove(user)
		else:
			user.followers.add(current_user)
			current_user.following.add(user)
			
		user.save()
		current_user.save()
		return HttpResponse(status=204)	

		
@csrf_exempt
@login_required	
def userposts_view(request, user_name):	

	try:
		user = User.objects.get(username=user_name)
	except User.DoesNotExist:
		return JsonResponse({"error": "User not found."}, status=404)	

	# Show user posts	
	if request.method == "GET":
		try:
			posts = Post.objects.filter(author=user)
			posts = posts.order_by("-timestamp").all()
		except Post.DoesNotExist:
			return JsonResponse({"error": "Posts not found."}, status=404)
		
		page = request.GET.get('page', 1)
		paginator = Paginator(posts, 10)
		num_pages = paginator.num_pages
		try:
			page_posts = paginator.page(page)
		except PageNotAnInteger:
			page_posts = paginator.page(1)
		except EmptyPage:
			page_posts = paginator.page(num_pages)
		
		number = page_posts.number
		
		data = {
			'previous_page': page_posts.has_previous() and page_posts.previous_page_number() or None,
			'next_page': page_posts.has_next() and page_posts.next_page_number() or None,
			'num_pages': num_pages,
			'number': page_posts.number,
			'data': list(post.serialize() for post in page_posts)
		}	
		
		return JsonResponse(data, safe=False)
				
@csrf_exempt
@login_required	
def following_view(request):		
	try:
		user = User.objects.get(username=request.user.username)
	except User.DoesNotExist:
		return JsonResponse({"error": "User not found."}, status=404)	
	
	# Show following posts
	following = user.following.all()
	summary_posts = []
	for item in following:
		try:
			posts = list(Post.objects.filter(author=item))
			summary_posts += posts
		except Post.DoesNotExist:
			return JsonResponse({"error": "Posts not found."}, status=404)
	
	summary_posts.sort(key=lambda x: x.timestamp, reverse=True)

	page = request.GET.get('page', 1)
	paginator = Paginator(summary_posts, 10)
	num_pages = paginator.num_pages
	try:
		page_posts = paginator.page(page)
	except PageNotAnInteger:
		page_posts = paginator.page(1)
	except EmptyPage:
		page_posts = paginator.page(num_pages)
		
	number = page_posts.number
	
	data = {
        'previous_page': page_posts.has_previous() and page_posts.previous_page_number() or None,
        'next_page': page_posts.has_next() and page_posts.next_page_number() or None,
		'num_pages': num_pages,
		'number': page_posts.number,
        'data': list(post.serialize() for post in page_posts)
    }	
		
	return JsonResponse(data, safe=False)

				
@csrf_exempt	
@login_required	
def post_view(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
	except Post.DoesNotExist:
		return JsonResponse({"error": "Post not found."}, status=404)

	# Get and change post "like"	
	if request.method == "GET":
		try:
			user = User.objects.get(id=request.user.id)
		except User.DoesNotExist:
			return JsonResponse({"error": "User not found."}, status=404)
		
		try:
			picked_post = user.liked.get(id=post_id)
			user.liked.remove(post_id)
			counter = post.counter - 1	
		except	Post.DoesNotExist:
			user.liked.add(post)
			counter = post.counter + 1	
			
		user.save()
		liked = user.liked.all()
		post.counter = counter
		post.save()
		return JsonResponse({"counter": counter})
	
	# Edit post text
	if request.method == "PUT":
		data = json.loads(request.body)
		post_text = data.get("post_text")
		post.text = post_text
		post.save()
		return HttpResponse(status=204)	


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
