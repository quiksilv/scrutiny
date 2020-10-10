from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound

from django.db.models import Q
from .models import Post
from .forms import PostForm

# Create your views here.
def index(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})
def add(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save() 
            # redirect to a new URL:
            return HttpResponseRedirect('/politicians/')
        else:
            print(form.errors)
