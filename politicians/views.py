from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.db.models import Q
from politicians.models import Politician
from politicians.forms import PoliticianForm
from posts.models import Post
from posts.forms import PostForm

def index(request):
    results = Politician.objects.all()
    return render(request, 'politicians/index.html', {'results': results} )
def search(request):
    term = request.GET.get('term')
    results = Politician.objects.filter(Q(name__contains=term) )
    return render(request, 'politicians/index.html', {'results': results} )
def view(request, name):
    details = Politician.objects.filter(name=name).get()
    posts = Post.objects.filter(Q(politician__name__contains=name) ).order_by('-created')
    form = PostForm()
    return render(request, 'politicians/view.html', {'details': details, 'posts': posts, 'form': form})
