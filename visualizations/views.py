from django.db.models import Q
from django.shortcuts import render
import matplotlib.pyplot as plt, mpld3
import matplotlib.dates as mdates

from agencies.models import Agency
from politicians.models import Politician

from datetime import datetime, timezone

import io
import urllib, base64
import numpy as np

# Create your views here.
#def mentions(request, p_id):
class Visualization:
    def barchart(p_id):
        data = [60, 30, 80]
        labels = ['Exp', 'Pop', 'Act']
        ind = range(1, len(labels) + 1)
        fig, ax = plt.subplots(figsize=(3, 3) )
        ax.bar(ind, data, label='Attributes')
        ax.set_ylabel('%')
        ax.set_xticks(ind)
        ax.set_xticklabels(labels)

        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        string = base64.b64encode(buf.read() )
        uri = urllib.parse.quote(string)
        return uri
    def mentions(p_id):
        xdata = []
        ydata = []
        agencies = Agency.objects.filter(Q(politician=p_id) ).values_list('published', flat=True)
        for agency in agencies:
            xdata.append(agency.replace(tzinfo=timezone.utc).astimezone(tz=None) )
        fig, ax = plt.subplots(figsize=(10, 4) )
        mformat = mdates.DateFormatter('%d/%m')
        ax.xaxis.set_major_formatter(mformat)
        y, x, _ = ax.hist(xdata)
    
        ax.set_xlabel('2020', fontsize=10)
        ax.set_ylabel('Count', fontsize=10)

        ax.yaxis.set_ticks(np.arange(0, y.max() + 1, 1) )

        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        string = base64.b64encode(buf.read() )
        uri = urllib.parse.quote(string)
        return uri
