from django.shortcuts import render
from mywatchlist.models import WatchList
from django.http import HttpResponse
from django.core import serializers


# Create your views here.
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