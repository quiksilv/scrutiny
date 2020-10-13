from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.db.models import Q
from politicians.models import Politician
from politicians.forms import PoliticianForm
from posts.models import Post
from posts.forms import PostForm
from agencies.models import Agency
from hansards.models import Hansard, Paragraph

def index(request):
    results = Politician.objects.all()
    return render(request, 'politicians/index.html', {'results': results} )
def search(request):
    term = request.GET.get('term')
    results = Politician.objects.filter(Q(name__contains=term) )
    return render(request, 'politicians/index.html', {'results': results} )
def view(request, name):
    form = PostForm()
    details = Politician.objects.filter(name=name).get()
    posts = Post.objects.filter(Q(politician__name__contains=name) ).order_by('-created')
    agencies = Agency.objects.filter(Q(politician__name=name) ).order_by('-created')
    hansards = []
    paragraphs = Paragraph.objects.filter(Q(politician__name=name) ).values('hansard').distinct()
    for paragraph in paragraphs:
        hansard_id = paragraph['hansard']
        hansard = Hansard.objects.get(id=hansard_id)
        hansards.append(hansard)
    return render(request, 'politicians/view.html', {'form': form, 'details': details, 'agencies': agencies, 'posts': posts, 'hansards': hansards})
