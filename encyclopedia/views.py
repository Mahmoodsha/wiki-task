from django.shortcuts import render
from . import util
from markdown2 import Markdown
import random

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdown = Markdown()
    if content == None:
        return None
    else:
        return markdown.convert(content)
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def error(request, title):
    content = convert_md_to_html(title)
    if content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "no page found"
        })
    else:
        return render(request, "encyclopedia/entery.html", {
            "title":title,
            "content":content,
        })
        
def search(request):
    if request.method == "POST":
        search_name = request.POST ['q']
        data = convert_md_to_html(search_name)
        if data == None:
            search_suggestion = util.list_entries()
            suggestions = []
            for entry in search_suggestion:
                if search_name.lower() in entry.lower():
                    suggestions.append(entry)
            return render(request, "encyclopedia/search.html", {
                "suggestions":suggestions
                })
        else:
            return render(request, "encyclopedia/entery.html", {
            "title":search_name,
            "content":data,
        })
        
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        # html = convert_md_to_html(title)
        title = request.POST ["title"]
        content = request.POST ["content"]
        title_page = util.get_entry(title)
        if title_page is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "the page is already exist"
            })
        else:
            util.save_entry(title, content)
            content_page = convert_md_to_html(title)
        
            return render(request, "encyclopedia/entery.html", {
                "title":title,
                "content":content_page
            })
            
def edit(request):
    if request.method == "POST":
        title = request.POST ["title"]
        content =util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title":title,
            "content":content,
        })
        
def save(request):
    if request.method == "POST":
        title = request.POST ["title"]
        content = request.POST ["content"]
        util.save_entry(title, content)
        content_page = convert_md_to_html(title)
        return render(request, "encyclopedia/entery.html", {
            "title":title,
            "content":content_page,
        })
        
def random_page(request):
    entries = util.list_entries()
    random_entries = random.choice(entries)
    content = convert_md_to_html(random_entries)
    return render(request, "encyclopedia/entery.html", {
        "title":random_entries,
        "content":content
    })
    