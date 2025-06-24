from django.shortcuts import render, redirect
import markdown2
from . import util
import random

entries = util.list_entries()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, title):
    content = markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content,
    })
    
def search(request):
    if request.method == "POST":
        query = request.POST.get("q", "").strip()
        entries = util.list_entries()

        # Check for exact match
        if query in entries:
            return redirect("entry", title=query)
        else:
            # Find entries that contain the query as a substring
            matching_entries = [entry for entry in entries if query.lower() in entry.lower()]
            return render(request, "encyclopedia/search.html", {
                "entries": matching_entries,
                "query": query
            })
    else:
        # Handle GET request (though search is typically a POST request)
        return render(request, "encyclopedia/search.html")


def new(request):

    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()

        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/new.html", {
                "message": "ERROR: a page with this title already exist. Try again for a different entry"
            })

        else:
            util.save_entry(title, content)
            return redirect("entry", title=title)

    return render(request, "encyclopedia/new.html")


def randomentry(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect("entry", title=title)
