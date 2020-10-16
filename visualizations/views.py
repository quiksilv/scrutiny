from django.db.models import Q
from django.shortcuts import render
import matplotlib.pyplot as plt, mpld3
import matplotlib.dates as mdates

from agencies.models import Agency
from politicians.models import Politician

# Create your views here.
#def mentions(request, p_id):
class Visualization:
    def barchart(p_id):
        data = [60, 30, 80]
        labels = ['Exp', 'Pop', 'Act']
        ind = range(1, len(labels) + 1)
        fig, ax = plt.subplots(figsize=(2, 2) )
        ax.bar(ind, data, label='Attributes')
        ax.set_ylabel('%')
        ax.set_xticks(ind)
        ax.set_xticklabels(labels)

        html_fig = mpld3.fig_to_html(fig)
        plt.close(fig)
        return html_fig
    def mentions(p_id):
        xdata = []
        ydata = []
        agencies = Agency.objects.filter(Q(politician=p_id) ).values_list('published', flat=True)
        for agency in agencies:
            xdata.append(agency)
            ydata.append(1)
        fig, ax = plt.subplots(figsize=(6, 3) )
        mformat = mdates.DateFormatter('%d')
        ax.xaxis.set_major_formatter(mformat)
        ax.plot_date(xdata, ydata, marker="o")
    
        ax.set_xlabel('Date', fontsize=20)
        ax.set_ylabel('Count', fontsize=20)

        ax.yaxis.set_ticks([])
    
        html_fig = mpld3.fig_to_html(fig)
        plt.close(fig)
        #return render(request, "visualizations/mentions.html", {"figure": html_fig} )
        return html_fig
