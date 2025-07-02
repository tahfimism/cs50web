from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Item, Comment, Category, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "items": Item.objects.filter(isopen=True).all(),
        "closed_items":Item.objects.filter(isopen=False).all(),

    })


def item(request, item_id):
    item = Item.objects.get(pk=item_id)
    bids = item.bids.all().order_by('-amount')
    price = bids.order_by('-amount').first().amount if bids.exists() else item.starting_bid
    message = request.session.pop('message', None)
    winning_bidder = None

    if request.method == "POST":
        # Watchlist actions
        if "watchlist_action" in request.POST:
            if request.POST["watchlist_action"] == "add":
                request.user.watchlist.add(item)
                request.session['message'] = "Added to watchlist"
            else:
                request.user.watchlist.remove(item)
                request.session['message'] = "Removed from watchlist"
            return HttpResponseRedirect(reverse("item", args=(item_id,)))

        # Bidding actions
        elif "bid_place" in request.POST:
            bid_input = request.POST.get("bid_place")
            try:
                bid_placed = float(bid_input)
                if (bids.exists() and bid_placed > bids.first().amount) or ((not bids.exists()) and bid_placed > item.starting_bid):
                    Bid.objects.create(amount=bid_placed, item=item, bidder=request.user)
                    request.session['message'] = "Bid successful"
                else:
                    request.session['message'] = "Bid too low"
            except (TypeError, ValueError):
                request.session['message'] = "Invalid bid amount."
            return HttpResponseRedirect(reverse("item", args=(item_id,)))

        # Comment actions
        elif "comment_text" in request.POST:
            comment_text = request.POST.get("comment_text")
            if comment_text and request.user.is_authenticated:
                Comment.objects.create(text=comment_text, item=item, by=request.user)
                request.session['message'] = "Comment added."
            return HttpResponseRedirect(reverse("item", args=(item_id,)))

        # Close auction
        elif "close_auction" in request.POST and request.user == item.owner:
            item.isopen = False
            item.owner = item.bids.order_by('-amount').first().bidder
            item.save()
            request.session['message'] = f"Auction closed. Item is now owned by {item.owner}"
            return HttpResponseRedirect(reverse("item", args=(item_id,)))

    return render(request, "auctions/item.html", {
        "item": item,
        "price": price,
        "bids": bids,
        "message": message,
        "comments": item.comments.all(),
        "winning_bidder": winning_bidder,
    })


def watchlist(request):
    items = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "items": items,
    })



def categories(request):
    return render(request, "auctions/categories.html", {
        "categories":Category.objects.all()
    })




def category(request, category_name):
    category = Category.objects.get(name=category_name)
    return render(request, "auctions/category.html", {
        "category":category,
    })




def create(request):
    if request.method == "POST":
        form = request.POST
        category_id = form["category"]
        if not category_id:
            request.session['message'] = "Please select a category."
            return HttpResponseRedirect(reverse("create"))

        Item.objects.create(
            title=form["title"],
            starting_bid=form["starting_bid"],
            category=Category.objects.get(pk=category_id),
            image=form["image_url"],
            description=form["description"],
            isopen=True,
            owner=request.user
        )
        return HttpResponseRedirect(reverse("index"))
    message = request.session.pop('message', None)
    return render(request, "auctions/create.html", {
        "categories": Category.objects.all(),
        "message": message
    })




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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")




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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def comment(request, item_id):
    if request.method == "POST":
        item = Item.objects.get(pk=item_id)
        text = request.POST.get("text")
        Comment.objects.create(text=text, item=item, by=request.user)
        return HttpResponseRedirect(reverse("item", args=(item_id,)))
    return HttpResponseRedirect(reverse("index"))