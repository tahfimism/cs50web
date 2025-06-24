from django.shortcuts import render
import datetime as dt
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse


class newtaskform(forms.Form):
    task = forms.CharField(label="new task")

    


# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = ["make coffee", "tea", "spill", "hello"]
    return render(request, "indextodo.html", {
        "tasks" : request.session["tasks"]
    })


def add(request):
    if request.method == "POST":
        form = newtaskform(request.POST)
        if form.is_valid():  # <-- Add parentheses here
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("todo:index"))
        else:
            return render(request, "add.html", {
                "form": form
            })

    return render(request, "add.html", {
        "form": newtaskform()
    })


