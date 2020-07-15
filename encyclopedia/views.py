import markdown2
import random
import re

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from random import randint

from . import util

from markdown2 import Markdown

class NewSearchForm(forms.Form):
	query = forms.CharField(label="Enter your query:")
class NewPageForm(forms.Form):
	entry_name = forms.CharField(label="Enter page name:") 
	entry_content = forms.CharField(widget=forms.Textarea(), label="Enter page content:") 
class EditPageForm(forms.Form):
	entry_content = forms.CharField(widget=forms.Textarea(), label="Edit page content:") 
	
	
def index(request):
	if request.method == "POST":
		page = "encyclopedia/index.html"
		url = search_form(request, page)
		return HttpResponseRedirect(url)
	else:
		return render(request, "encyclopedia/index.html", {
			"form": NewSearchForm(),
			"entries": util.list_entries()
		})

def entry(request, name):
	if request.method == "POST":
		page = "encyclopedia/entry.html"
		url = search_form(request, page)
		return HttpResponseRedirect(url)
	else:
		markdowner = Markdown()
		content_text = util.get_entry(name)
		if content_text:
			content = markdowner.convert(content_text)
			return render(request, "encyclopedia/entry.html", {
				"form": NewSearchForm(),
				"name": name,
				"content": content
			})
		else:
			return render(request, "encyclopedia/error.html", {
				"form": NewSearchForm(),
				"text": "Requested page is not found!"
			})
	
def search_results(request, query):
	if request.method == "POST":
		page = "encyclopedia/search_results.html"
		url = search_form(request, page)
		return HttpResponseRedirect(url)
	else:
		result_entries = []
		entries = util.list_entries()
		for i in range(0,len(entries)):
			entry = entries[i]
			entry_lower = entry.lower()
			if entry_lower.find(query.lower())>=0:
				result_entries.append(entry);
		return render(request, "encyclopedia/search_results.html", {
				"form": NewSearchForm(),
				"entries": result_entries
		})

def search_form(request, page):
	form = NewSearchForm(request.POST)
	if form.is_valid():
		query = form.cleaned_data["query"]
		entry_text = util.get_entry(query)
		if entry_text:
			url = reverse("encyclopedia:entry", kwargs={'name': query})
		else:
			url = reverse("encyclopedia:search_results", kwargs={'query': query})
		return url
	else:
		return render(request, page, {
			"form": form
        })	

def create(request):
	if request.method == "POST":
		form = NewPageForm(request.POST)
		if form.is_valid():
			entry_name = form.cleaned_data["entry_name"]
			entry_content = form.cleaned_data["entry_content"]
			existing_entry = util.get_entry(entry_name)
			if existing_entry:
				return render(request, "encyclopedia/error.html", {
					"form": NewSearchForm(),
					"text": "Such entry is already existing!"
				})
			else:
				util.save_entry(entry_name, entry_content)
				url = reverse("encyclopedia:entry", kwargs={'name': entry_name})
				return HttpResponseRedirect(url)	
		else:
			form = NewSearchForm(request.POST)
			page = "encyclopedia/create.html"
			url = search_form(request, page)
			return HttpResponseRedirect(url) 		
	else:
		return render(request, "encyclopedia/create.html", {
			"form": NewSearchForm(),
			"create_page_form": NewPageForm()
		})

def edit(request, name):
	if request.method == "POST":
		form = EditPageForm(request.POST)
		if form.is_valid():
			edited_entry_content = form.cleaned_data["entry_content"]
			util.save_entry(name, edited_entry_content)
			url = reverse("encyclopedia:entry", kwargs={'name': name})
			return HttpResponseRedirect(url)	
		else:
			form = NewSearchForm(request.POST)
			page = "encyclopedia/edit.html"
			url = search_form(request, page)
			return HttpResponseRedirect(url) 		
	else:		
		entry_content = '\r\n'.join(list(filter(None,util.get_entry(name).splitlines())))
		initial = {'entry_content': entry_content}
		return render(request, "encyclopedia/edit.html", {
			"form": NewSearchForm(),
			"entry_name": name,
			"edit_page_form": EditPageForm(initial=initial)
		})
	
		
def random_entry(request):
	all_entries = util.list_entries()
	len_entries = len(all_entries)-1
	random_number = randint(0, len_entries)
	random_entry = all_entries[random_number]
	entry_text = util.get_entry(random_entry)
	if entry_text:
		url = reverse("encyclopedia:entry", kwargs={'name': random_entry})
		return HttpResponseRedirect(url)	
	else:
		return render(request, "encyclopedia/error.html", {
			"form": NewSearchForm(),
			"text": "Something went wrong... Requested page is not found!"
		})

def error(request, text):		
	return render(request, "encyclopedia/error.html", {
		"form": NewSearchForm(),
		"text": text
	})
