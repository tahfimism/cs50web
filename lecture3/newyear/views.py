from django.shortcuts import render
import datetime as dt
from django.http import HttpResponse

# Create your views here.
def index(request):
    now = dt.datetime.now()

    return render(request, "index.html", {
        "newyear": now.month == 1 and now.day == 1,
    })

