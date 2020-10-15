from django.db.models import Q
from django.shortcuts import render
import matplotlib.pyplot as plt, mpld3
import matplotlib.dates as mdates

from agencies.models import Agency
from politicians.models import Politician

# Create your views here.
def mentions(request, p_id):
    xdata = []
    ydata = []
    agencies = Agency.objects.filter(Q(politician=p_id) ).values_list('published', flat=True)
    for published in agencies:
        xdata.append(published)
        ydata.append(1)
    fig, ax = plt.subplots(figsize=(4, 4) )
    ax.plot(xdata, ydata, marker="o")

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d') )
    ax.set_xlabel('date', fontsize=20)
    ax.set_ylabel('counts', fontsize=20)

    html_fig = mpld3.fig_to_html(fig)
    plt.close(fig)
    return render(request, "visualizations/mentions.html", {"figure": html_fig} )
