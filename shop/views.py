from django.shortcuts import render, HttpResponse, redirect
from .models import User, ItemUpdated, Bid, ItemUserConnect, Comment, FinishBids
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout as django_logout
def sign(request):
    #if user sends a form
    if request.method == 'POST':
        #get username and check it
        username = request.POST.get('username')
        if not username:
            return render(request, 'shop/sign.html', {'error': "please enter username"})
        if len(username) < 4:
           return render(request, 'shop/sign.html', {'error': "username not valid"})
        #get password and check it
        password = request.POST.get('password')
        if not password:
            return render(request, 'shop/sign.html', {'error': "please enter password"})
        if len(password) < 4:
           return render(request, 'shop/sign.html', {'error': "password not valid"})
        #check if username and password are in db
        userEntering = User.objects.filter(username=username).first()
        if not userEntering:
            return render(request, 'shop/sign.html', {'error': "wrong password/username"})
        if not check_password(password, userEntering.hashPassword):
            return render(request, 'shop/sign.html', {'error': "wrong password/username"})
        request.session['username'] = username
        return redirect("home")
    #if user access via get
    return render(request, 'shop/sign.html')



def register(request):
    if request.method == "POST":
       #get username and check it
        username = request.POST.get('username')
        if not username:
            return render(request, 'shop/register.html', {'error': "please enter username"})
        if len(username) < 4:
           return render(request, 'shop/register.html', {'error': "username not valid"})
        checker = User.objects.filter(username=username).first()
        if checker:
            return render(request, 'shop/register.html', {'error': "user already exists"})
        #get password and check it
        password = request.POST.get('password')
        passwordcon = request.POST.get('passwordCon')
        if not password:
            return render(request, 'shop/register.html', {'error': "please enter password"})
        if len(password) < 4:
           return render(request, 'shop/register.html', {'error': "password not valid"})
        if password != passwordcon:
            return render(request, 'shop/register.html', {'error': "passwords don't match"})
        #add user to db
        userEntering = User(username=username, hashPassword=make_password(password))
        userEntering.save()
        return redirect('sign')
    return render(request, 'shop/register.html')

def home(request):
    #check if user is logged in
    if 'username' in request.session:
        allItems = ItemUpdated.objects.all()
        return render(request, 'shop/home.html', {'username': request.session['username'], 'items': allItems, 'types': True})
    #if user isn't logged in
    else:
        return redirect('sign')
    
def logout(request):
    #clear user info from session
    django_logout(request)
    request.session.flush()
    return redirect('sign')

def addItems(request):
    #check if user is logged in 
    if 'username' in request.session:
        #if user sends the form
        if request.method == 'POST':
            #get user info 
            userInfo = User.objects.filter(username=request.session['username']).first()
            #get item info
            item_Title = request.POST.get('item_name')
            item_Price = request.POST.get('item_price')
            item_Image = request.POST.get('item_image')
            item_type  = request.POST.get('item_type')
            item_description = request.POST.get('item_description')
            #check info
            if not item_Image or not item_Price or not item_Title or not item_description or item_type == '':
                return render(request, 'shop/adder.html', {'username': request.session['username'], 'error': 'Invalid input'})
            #create a new item and saving it
            newItem = ItemUpdated(item_name=item_Title, item_price=item_Price, item_image=item_Image, item_description=item_description, item_type=item_type)
            newItem.save()
            newConnection = ItemUserConnect(userPlacedABid= userInfo, itemGotBid=newItem, bidAdmin=True)
            newConnection.save()
            #redirecting to home page
            return redirect('home')
        #if the user access the page with get
        return render(request, 'shop/adder.html', {'username': request.session['username']})
    #if the user is not logged in 
    return redirect('sign')

def itemPage(request, clickedItemTitle):
    if 'username' in request.session:
        #get the clicked item
        clickedItem = ItemUpdated.objects.filter(pk= clickedItemTitle).first()
        #get user info
        activeUser = User.objects.filter(username=request.session['username']).first()
        #get comments
        comments = Comment.objects.filter(item=clickedItem)
        if not clickedItem:
            return HttpResponse('404item not found')
        #check if the active user is the one who is accessing the page
        adminUser = False
        inWatchlist = True
        userItemChecker = ItemUserConnect.objects.filter(userPlacedABid=activeUser, itemGotBid=clickedItem).first()
        if userItemChecker:
            adminUser = userItemChecker.bidAdmin
        else:
            inWatchlist = False
        #if the user sends a form 
        checkIfTheBidIsEnded = FinishBids.objects.filter(item=clickedItem).first()
        if checkIfTheBidIsEnded:
            return render(request, 'shop/itemPage.html', {'item': clickedItem, 'username': activeUser.username, 'ended': True, 'userWinner': checkIfTheBidIsEnded.buyer.username})
        if request.method == 'POST':
            #get the new bid the user will enter
            newBid = request.POST.get('newBid')
            #check the new bid
            if not newBid:
                return render(request, 'shop/itemPage.html', {'item': clickedItem, 'username': activeUser.username, 'userAdmin': adminUser, 'inWatchlist': inWatchlist, 'error': 'bid not valid', 'comments': comments})
            newBid = float(newBid)
            if not newBid or newBid < clickedItem.item_price:
                return render(request, 'shop/itemPage.html', {'item': clickedItem, 'username': activeUser.username, 'userAdmin': adminUser, 'inWatchlist': inWatchlist, 'error': 'bid not valid', 'comments': comments})
            bidAdder = Bid(buyerId=activeUser, itemId=clickedItem, bidAmount=newBid)
            bidAdder.save()
            clickedItem.item_price = newBid
            clickedItem.save()
            return render(request, 'shop/itemPage.html', {'item': clickedItem, 'username': activeUser.username, 'userAdmin': adminUser, 'inWatchlist': inWatchlist, 'comments': comments})
        return render(request, 'shop/itemPage.html', {'item': clickedItem, 'username': activeUser.username, 'userAdmin': adminUser, 'inWatchlist': inWatchlist, 'comments': comments})
    return redirect('sign')

def bidEnder(request, itemToEndBid):
    #check if user is signed in
    if 'username' in request.session:
        #get user and item info
        userCreator = User.objects.get(username=request.session['username'])
        itemWannaEnd = ItemUpdated.objects.get(item_name=itemToEndBid)
        #get the winner
        winnerUser = Bid.objects.get(itemId=itemWannaEnd, bidAmount=itemWannaEnd.item_price).buyerId
        #check if the user is the admin
        checker = ItemUserConnect.objects.get(userPlacedABid=userCreator, itemGotBid=itemWannaEnd)
        if not checker:
            return HttpResponse('access denied')
        #add it to ended bids
        bidToEnd = FinishBids(buyer=winnerUser, seller=userCreator, item=itemWannaEnd, lastBid=itemWannaEnd.item_price)
        bidToEnd.save()
        return redirect('itemPage', clickedItemTitle=itemWannaEnd.pk)
    return redirect('sign')

    

def types(request, typeClicked):
    if 'username' in request.session:
        allItems = ItemUpdated.objects.filter(item_type=typeClicked)
        return render(request, 'shop/home.html', {'username': request.session['username'], 'items': allItems, 'types': True})
    #if user isn't logged in
    else:
        return redirect('sign')



def watchlist(request):
    if 'username' in request.session:
        #get user info
        user = User.objects.get(username=request.session['username'])

        #get items user put in watchlist
        allItems = ItemUserConnect.objects.filter(userPlacedABid=user, bidAdmin=False)
        
        #loop through the elements in all items
        all_item_objects = [item.itemGotBid for item in allItems]

        #render the template
        return render(request, 'shop/home.html', {'username': request.session['username'], 'items': all_item_objects, 'types': False})
    return redirect('sign')    
    
def watchlistAdder(request, itemToAdd):
    if 'username' in request.session:
        #get user and item info
        user = User.objects.get(username=request.session['username'])
        itemToBeAdded = ItemUpdated.objects.get(pk=itemToAdd)

        #check if item is already there
        checker = ItemUserConnect.objects.filter(userPlacedABid=user, itemGotBid=itemToBeAdded)
        if checker:
            return redirect(watchlist)
        #add them to the connection
        adder = ItemUserConnect(userPlacedABid=user, itemGotBid=itemToBeAdded)
        adder.save()

        #redirectiong to watchlist
        return redirect('watchlist')
    
    #if user isn't signed in 
    return redirect('sign')

def watchlistRemover(request, itemToRemove):
    #check if user is signed
    if 'username' in request.session:
        #get user and item
        user = User.objects.get(username=request.session['username'])
        item = ItemUpdated.objects.get(pk=itemToRemove)
        
        #remove from connectioon
        connection = ItemUserConnect.objects.filter(userPlacedABid=user, itemGotBid=item, bidAdmin=False).first()
        if not connection:
            return HttpResponse('error')
        connection.delete()

        #redirecting to watchlist
        return redirect('watchlist')
    
    #if user isn't signed in
    return redirect('sign')

def comments(request, itempk):
    #check if user is logged in
    if 'username' in request.session:
        #get user info 
        user = User.objects.get(username=request.session['username'])
        #get item info
        item = ItemUpdated.objects.get(pk=itempk)
        if request.method == 'POST':
            #get the comment
            comment = request.POST.get('comment')
            commentCreator = Comment(comment=comment, user=user, item=item)
            commentCreator.save()
            return redirect('itemPage', clickedItemTitle=itempk)
        return HttpResponse('error 1')
    return HttpResponse('error2')
