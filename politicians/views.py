from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from politicians.models import Politician, Constituency, Portfolio
from politicians.forms import PoliticianForm
from posts.models import Post
from posts.forms import PostForm
from agencies.models import Agency
from hansards.models import Hansard, Paragraph
from visualizations.models import Statistics
from visualizations.views import Visualization

import datetime

def get_wikipedia_statistics(wikipedia, politician):
    stats = Statistics.objects.filter(category='wikipedia', politician=politician).order_by('-created').values('name', 'value')[:4]
    if stats:
        for stat in stats:
            wikipedia[stat['name'] ] = stat['value']
        timestamp = wikipedia['timestamp']
        wikipedia['timestamp'] = datetime.datetime.fromtimestamp(timestamp)

def get_twitter_statistics(twitter, politician):
    stats = Statistics.objects.filter(category='tweets', politician=politician).order_by('-created').values('name', 'value')[:9]
    if stats:
        for stat in stats:
            twitter[stat['name'] ] = stat['value']
        #normalised to total tweets
        total_tweets = int(twitter['total_tweets'])
        total_like_count = int(twitter['total_like_count'])
        total_retweet_count = int(twitter['total_retweet_count'])
        twitter['like_ratio'] = "{:.2f}".format(total_like_count/total_tweets)
        twitter['retweet_ratio'] = "{:.2f}".format(total_retweet_count/total_tweets)

def index(request):
    results = Constituency.objects.select_related().exclude(politician__isnull=True)
    stats = {}
    for result in results:
        agencies_count = Agency.objects.select_related().filter(politician=result.politician_id).count()
        stats[result.politician_id] = agencies_count
    return render(request, 'politicians/index.html', {'results': results, 'stats': stats} )
def search(request):
    term = request.GET.get('term')
    #search by name
    politicians = Politician.objects.filter(Q(name__contains=term) ).values_list('id', flat=True)
    results = Constituency.objects.select_related().filter(politician__in=politicians )
    stats = {}
    for result in results:
        agencies_count = Agency.objects.select_related().filter(politician=result.politician_id).count()
        stats[result.politician_id] = agencies_count
    return render(request, 'politicians/index.html', {'results': results, 'stats': stats} )
def view(request, name):
    details = {}
    form = PostForm()
    objs = Politician.objects.filter(name=name).values('id', 'name', 'image_url', 'highest_education', 'twitter', 'facebook', 'wikipedia')
    details['id'] = objs[0]['id']
    details['name'] = objs[0]['name']
    details['image_url'] = objs[0]['image_url']
    details['highest_education'] = objs[0]['highest_education']
    details['twitter'] = {}
    details['twitter']['link'] = objs[0]['twitter']
    get_twitter_statistics(details['twitter'], Politician.objects.get(id=objs[0]['id']) )

    details['facebook'] = objs[0]['facebook']
    details['wikipedia'] = {}
    details['wikipedia']['link'] = objs[0]['wikipedia']
    get_wikipedia_statistics(details['wikipedia'], Politician.objects.get(id=objs[0]['id']) )

    details['figure'] = Visualization.mentions(objs[0]['id'])
    details['performance_plot'] = Visualization.barchart(objs[0]['id'])
    
    posts = Post.objects.filter(Q(politician__name__contains=name) ).order_by('-created')
    agencies = Agency.objects.filter(Q(politician__name=name) ).order_by('-published')
    agencies_paginator = Paginator(agencies, 5)
    agencies_page_number = request.GET.get('agencies_page')

    try:
        agencies_page_obj = agencies_paginator.page(agencies_page_number)
    except PageNotAnInteger:
        agencies_page_obj = agencies_paginator.page(1)
    except EmptyPage:
        agencies_page_obj = agencies_paginator.page(agencies_paginator.num_pages)

    hansards = []
    paragraphs = Paragraph.objects.filter(Q(politician__name=name) ).values('hansard').distinct()
    for paragraph in paragraphs:
        hansard_id = paragraph['hansard']
        hansard = Hansard.objects.get(id=hansard_id)
        hansards.append(hansard)

    return render(request, 'politicians/view.html', {'form': form, 'details': details, 'agencies': agencies, 'posts': posts, 'hansards': hansards, 'agencies_page_obj': agencies_page_obj})
