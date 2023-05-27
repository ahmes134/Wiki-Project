from django.shortcuts import render
from . import util
from markdown2 import Markdown
import random

#might need this
from django.shortcuts import redirect

def old_url_redirect(request, old_url):
    new_url = "wiki/" + old_url
    return redirect(new_url, permanent=True)
####

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request, title):
    markdowner = Markdown()
    if util.get_entry(title) == None:
        return render (request, "encyclopedia/error.html", {"message":"Page Not Found"})
    else:
        page_content = markdowner.convert(util.get_entry(title))
        return render (request, "encyclopedia/content.html", {
            "content": page_content, "page_title": title
    })

def search(request):
    if request.method == "POST":
        search_entry = request.POST['q']
        markdowner = Markdown()
        entry_retrieved = util.get_entry(search_entry)

    if entry_retrieved == None:
        entries = util.list_entries()
        search_results = []
        #need a list of the entries that include the query as a substring
        for entry in entries:
            if search_entry.lower() in entry.lower(): 
                search_results.append(entry)
     
        return render (request, "encyclopedia/search.html", {
                "search_results": search_results
        })

    else: 
        content = markdowner.convert(entry_retrieved) 
        return render (request, "encyclopedia/content.html", {
            "content": content, "page_title": search_entry
        })

def new_page(request):
    if request.method == "GET":
        return render (request, "encyclopedia/new_page.html")

    else:
        title = request.POST['usr_title']
        entry = request.POST['usr_entry']
        entry = entry.strip()
        validTitle = util.get_entry(title)
        if validTitle is not None:  #if the title provided by the user already exists
            return render(request, "encyclopedia/error.html", {
                "message": "This page already exists"
            })
        else: #if the title does not already exist -> create the new page 
            markdowner = Markdown()
            page_content = markdowner.convert(entry)
            util.save_entry(title, entry)
            return render (request, "encyclopedia/content.html", {
            "content": page_content, "page_title": title
    })

def edit_page(request): #this title parameter comes from the path in urls.py
    if request.method == "POST":
        title = request.POST["entry_title"]
        entry = util.get_entry(title)
        entry = entry.strip()
        #need to enter the title and content into the template for edit page
        return render (request, "encyclopedia/edit_page.html", {"title": title, "content": entry})
            
def save_page(request):
        if request.method == "POST":
            title = request.POST["usr_title"]
            entry = request.POST['usr_entry'].strip() #in markdown format 
            util.save_entry(title, entry) #saves the markdown
            #convert and render the page
            markdowner = Markdown()
            page_content = markdowner.convert(util.get_entry(title))
            #send the content in html format
            return render (request, "encyclopedia/content.html", {
            "content": page_content, "page_title": title
    })

def random_page(request):
    entries_list = util.list_entries()
    chosen_title = random.choice(entries_list)
    chosen_entry= util.get_entry(chosen_title)
    markdowner = Markdown()
    page_content = markdowner.convert(chosen_entry)
    return render (request, "encyclopedia/content.html", {
        "content": page_content, "page_title": chosen_title
    })


    
