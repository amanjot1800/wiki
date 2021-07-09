from django.shortcuts import render, redirect
from django.http import HttpResponse
import markdown2
import random as rand

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def fetch(request, title):
    entry = util.get_entry(title)

    if entry is None:
        return render(request, "encyclopedia/error.html"), {
            "error": "404: The page requested was not found."
        }

    content = markdown2.markdown(entry)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })


def q(request):
    if request.method == 'POST':
        query = request.POST.get('q')

        if util.get_entry(query) is not None:
            return redirect(f"/{query}")

        else:
            entries = util.suggest_entries(query)
            return render(request, "encyclopedia/search.html", {
                "entries": entries,
                "query": query
            })

    return redirect("/")


def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if util.create_or_edit_entry(title, content):
            return redirect(f'/{title}')
        else:
            return render(request, "encyclopedia/error.html", {
                "error": "An entry with same name already exists. Try another name."
            })
    else:
        return render(request, "encyclopedia/create.html")


def edit(request, title2):
    if request.method == "POST":
        title = request.POST.get("new_title")
        content = request.POST.get("new_content")

        if util.create_or_edit_entry(title, content, "w"):
            return redirect(f'/{title}')
        else:
            return render(request, "encyclopedia/error.html", {
                "error": "An entry with same name already exists. Try another name."
            })
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": title2,
            "content": util.get_entry(title2)
        })


def random(request):

    return redirect(f"/{rand.choice(util.list_entries())}")

