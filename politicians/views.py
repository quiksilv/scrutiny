from django.shortcuts import render

from django.db.models import Q
from politicians.models import Politician, Constituency, Portfolio
from politicians.forms import PoliticianForm
from posts.models import Post
from posts.forms import PostForm
from agencies.models import Agency
from hansards.models import Hansard, Paragraph

from visualizations.views import Visualization

def index(request):
    results = Constituency.objects.select_related().all()
    return render(request, 'politicians/index.html', {'results': results} )
def search(request):
    term = request.GET.get('term')
    #search by name
    politicians = Politician.objects.filter(Q(name__contains=term) ).values_list('id', flat=True)
    results = Constituency.objects.select_related().filter(politician__in=politicians )
    return render(request, 'politicians/index.html', {'results': results} )
def view(request, name):
    details = {}
    form = PostForm()
    objs = Politician.objects.filter(name=name).values('id', 'name', 'image_url', 'highest_education', 'twitter', 'facebook', 'wikipedia')
    details['id'] = objs[0]['id']
    details['name'] = objs[0]['name']
    details['image_url'] = objs[0]['image_url']
    details['highest_education'] = objs[0]['highest_education']
    details['twitter'] = objs[0]['twitter']
    details['facebook'] = objs[0]['facebook']
    details['wikipedia'] = objs[0]['wikipedia']
    details['figure'] = Visualization.mentions(objs[0]['id'])
    details['performance_plot'] = Visualization.barchart(objs[0]['id'])
    
    posts = Post.objects.filter(Q(politician__name__contains=name) ).order_by('-created')
    agencies = Agency.objects.filter(Q(politician__name=name) ).order_by('-created')
    hansards = []
    paragraphs = Paragraph.objects.filter(Q(politician__name=name) ).values('hansard').distinct()
    for paragraph in paragraphs:
        hansard_id = paragraph['hansard']
        hansard = Hansard.objects.get(id=hansard_id)
        hansards.append(hansard)

    return render(request, 'politicians/view.html', {'form': form, 'details': details, 'agencies': agencies, 'posts': posts, 'hansards': hansards})
