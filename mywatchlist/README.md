# Data Delivery using Django
HEROKU APP: [LINK](https://pbp-asg2.herokuapp.com/mywatchlist/html)
## Difference Between JSON, XML, and HTML
XML is a markup language mostly used to store data, whereas HTML is a markup language that helps us develop a design and web content. JSON and XML are both largely used for data storage; the difference between them is in how they are written.

## Why We Need Data Delivery in Implementing a Platform
In general, data delivery is necessary for all applications. Data delivery is used to retrieve data, and it goes without saying that data are crucial for applications.

## Implementation
### Creating a new app `mywatchlist`
```cmd
python manage.py startapp mywatchlist
```
### Add URL for `mywatchlist`
Add to `urlpatterns` in `urls.py` that is on `project_django` directroy
```py
path('mywatchlist/', include('mywatchlist.urls'))
```
### Create a model for `mywatchlist`
```py
# models.py
from django.db import models


class WatchList(models.Model):
    watched = models.BooleanField()
    title = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    release_date = models.CharField(max_length=55)
    review = models.TextField()
```
### Add data for the `WatchList` 
Create a folder `fixtures` and create a new file named `initial_watchlist_data.json`
```json
[
    {
        "model": "mywatchlist.watchlist",
        "pk":1,
        "fields": {
            "watched": true,
            "title": "Fullmetal Alchemist: Brotherhood",
            "rating": 5,
            "release_date": "Apr 5, 2009",
            "review": "A good solid anime!"
        }
    },
    {
        "model": "mywatchlist.watchlist",
        "pk":2,
        "fields": {
            "watched": false,
            "title": "Kaguya-sama wa Kokurasetai: Ultra Romantic",
            "rating": 0,
            "release_date": "Apr 9, 2022",
            "review": "-"
        }
    },
    {
        "model": "mywatchlist.watchlist",
        "pk":3,
        "fields": {
            "watched": true,
            "title": "Gintama??",
            "rating": 4.5,
            "release_date": "Apr 8, 2015",
            "review": "Nice comedy and action!"
        }
    },
    {
        "model": "mywatchlist.watchlist",
        "pk":4,
        "fields": {
            "watched": true,
            "title": "Steins;Gate",
            "rating": 4,
            "release_date": "Apr 6, 2011",
            "review": "I watch anime to relieve stress.. But this sh*t made me rack my brain."
        }
    },
    
    {
        "model": "mywatchlist.watchlist",
        "pk":5,
        "fields": {
            "watched": true,
            "title": "Shingeki no Kyojin Season 3 Part 2",
            "rating": 4,
            "release_date": "Apr 29, 2019",
            "review": "rumbleee.."
        }
    },
    
    {
        "model": "mywatchlist.watchlist",
        "pk":6,
        "fields": {
            "watched": true,
            "title": "Gintama'",
            "rating": 4.5,
            "release_date": " Apr 4, 2011",
            "review": "Hillarious yet cool anime!"
        }
    },
    
    {
        "model": "mywatchlist.watchlist",
        "pk":7,
        "fields": {
            "watched": true,
            "title": "Gintama: The Final",
            "rating": 4.7,
            "release_date": "Jan 8, 2021",
            "review": "Very cool action, yet the comedy is spot on nonetheless"
        }
    },
    
    {
        "model": "mywatchlist.watchlist",
        "pk":8,
        "fields": {
            "watched": true,
            "title": "Gintama': Enchousen",
            "rating": 4.4,
            "release_date": "Oct 4, 2012",
            "review": "Enough Gintama"
        }
    },
    {
        "model": "mywatchlist.watchlist",
        "pk":9,
        "fields": {
            "watched": false,
            "title": "Hunter x Hunter (2011)",
            "rating": 0,
            "release_date": "Oct 2, 2011",
            "review": "-"
        }
    },
    {
        "model": "mywatchlist.watchlist",
        "pk":10,
        "fields": {
            "watched": false,
            "title": "Ginga Eiyuu Densetsu",
            "rating": 0,
            "release_date": "Apr 8, 2015",
            "review": "-"
        }
    }
]
```
### Implement three feature: HTML, XML, and JSON
```py
# views.py
from django.shortcuts import render
from mywatchlist.models import WatchList
from django.http import HttpResponse
from django.core import serializers


def show_mywatchlist(request):
    data_mywatchlist_item = WatchList.objects.all()
    amount_watched = sum(movies.watched for movies in data_mywatchlist_item)
    amount_not_watched = len(data_mywatchlist_item) - amount_watched
    display_message = "Congratulations, you have watched movies a lot!" if \
        amount_watched > amount_not_watched else \
        "Woah, you have not much watched movies!"

    context = {
        'watch_list': data_mywatchlist_item,
        'name': 'Jovian',
        'npm': '2106720891',
        'display_message': display_message
    }

    return render(request, "mywatchlist.html", context)


def show_xml(request):
    data = WatchList.objects.all()
    return HttpResponse(serializers.serialize("xml", data), 
                        content_type="application/xml")


def show_xml_by_id(request, id):
    data = WatchList.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), 
                        content_type="application/xml")


def show_json(request):
    data = WatchList.objects.all()
    return HttpResponse(serializers.serialize("json", data), 
                        content_type="application/json")


def show_json_by_id(request, id):
    data = WatchList.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), 
                        content_type="application/json")
```

### Create a routing to the three features above
Add the codes to `urls.py` inside `codepatterns`
```py
path('html/', show_mywatchlist, name='show_mywatchlist'),
path('xml/', show_xml, name='show_xml'),
path('xml/<int:id>', show_xml_by_id, name='show_xml_by_id'),
path('json/', show_json, name='show_json'),
path('json/<int:id>', show_json_by_id, name='show_json_by_id'),
```

### Deploy to heroku
Add `python manage.py loaddata initial_watchlist_data.json` into `Procfile` so that heroku can load `initial_watchlist_data.json`.
git add, commit, and push, and tada!