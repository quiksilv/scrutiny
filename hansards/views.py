from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import Hansard, Paragraph

def view(request, name):
    hansard = Hansard.objects.get(name=name)
    paragraphs = Paragraph.objects.filter(hansard=hansard)
    return render(request, 'hansards/view.html', {"hansard": hansard, "paragraphs": paragraphs} )
