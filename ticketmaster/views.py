from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from .forms import CommentForm
from .models import Comment







def add_product(request,id):
   if request.method == "POST":
       form = CommentForm(request.POST)
       if form.is_valid():
           comment = form.save(commit=False)
           comment.event = id
           form.save()
           return redirect('comments', id)
   else:
       form = CommentForm()
       context = {'form': form, 'name': id}
       return render(request, 'ticketmaster/add-form.html', context)




def update_product(request, name, id):
   product = Comment.objects.get(id=id)
   form = CommentForm(request.POST or None, instance=product)
   if form.is_valid():
       form.save()
       return redirect('comments', name)
   context = {'form': form}
   return render(request, 'ticketmaster/add-form.html', context)




def delete_product(request, name, id):
   comment = Comment.objects.get(id=id)
   if request.method == "POST":
       comment.delete()
       return redirect('comments', name)
   context = {'comment': comment,  'name': name}
   return render(request, 'ticketmaster/delete-confirm.html', context)





def eventSearch(request):
   if request.method == 'POST':
       genre = request.POST['genre']
       location = request.POST['location']


       if not genre or not location:
           messages.info(request, 'Both fields must be filled')
           return redirect('ticketmaster-index')


       events = getEvents(genre, location)


       if events is None:
           messages.info(request, 'There was an error getting the data')
           return redirect('ticketmaster-index')


       else:
           users = events['_embedded']['events']
           user_list = []


           for user in users:
               name = user['name']
               image = user['images'][0]['url']
               venue = user["_embedded"]["venues"][0]["name"]
               address = user["_embedded"]["venues"][0]["address"]["line1"]
               city = user["_embedded"]["venues"][0]["city"]["name"]
               state = user["_embedded"]["venues"][0]["state"]["name"]
               date = user["dates"]["start"]["localDate"]
               time = user["dates"]["start"]["localDate"]
               link = user["url"]


               user_details = {
                   'name': name,
                   'image': image,
                   'venue': venue,
                   'address': address,
                   'city': city,
                   'state': state,
                   'date': date,
                   'time': time,
                   'link': link
               }


               user_list.append(user_details)


           context = {'users': user_list}
           return render(request, 'ticketmaster/ticketmaster.html', context)


   return render(request, 'ticketmaster/ticketmaster.html')




def getEvents(genre, location):
   try:
       url = "https://app.ticketmaster.com/discovery/v2/events.json"
       params = {
           "classificationName": genre,
           "city": location,
           "sort": "date,asc",
           "apikey": "kUzOZyipqqVNqBArNsEswxoXBNbZSQyG"
       }


       response = requests.get(url, params=params)
       response.raise_for_status()
       data = response.json()
       return data
   except requests.exceptions.RequestException as e:
       print(f"Request failed: {e}")
       return None




def comments(request, id):
   comments = Comment.objects.all()
   context = {'name': id, 'comments': comments}
   return render(request, 'ticketmaster/comments.html', context)
