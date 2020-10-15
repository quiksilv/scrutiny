from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from .models import Hansard, Paragraph
from politicians.models import Politician

import os
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def preprocessing(text):
    page_number = 0
    results = {}
    lines = text.split('\n')
    lines = list(filter(None, lines) )
    #remove header
    if "BELUM DISUNTING" in lines[0]:
        del lines[0] #BELUM DISUNTING
        del lines[0] #DATE
    return lines
def getparagraphs(lines):
    paragraphs = []
    counter = 0
    paragraph = ""
    for line in lines:
        if line.isspace():
            paragraphs.append(paragraph)
            paragraph = ""
            counter = counter + 1
            continue
        paragraph += ' ' + line
    paragraphs = list(filter(None, paragraphs) )
    return paragraphs
def getactors(paragraphs, actor):
    politicians = Politician.objects.filter().values('name')
    titles = ['YB', 'Amar', 'Patinggi', 'Dato', 'Datuk', 'Amar', 'Tan', 'Sri', 'Dr', 'Tuan', 'Puan', 'Anak', 'Haji', 'Hj', 'Haji', 'Hajah', 'Bin', 'Binti', 'Encik', 'Cik', 'Ir', 'Prof.', 'Dr']
    others = ['Timbalan Speaker', 'Speaker', 'Tuan Pengerusi']
    results = {}
    for i, paragraph in enumerate(paragraphs):
        if ":" in paragraph:
            actor = paragraph.split(":")[0].replace('  ', ' ')
            for title in titles:
                actor = actor.replace(title, '').replace('  ', ' ').strip()
            have_actor = False
            for politician in politicians:
                if politician['name'].replace('_', ' ') in actor:
                    actor = politician['name'].replace('_', ' ')
                    have_actor = True
                    break
            if not have_actor:
                actor = "unknown"
            results[i] = actor
        else:
            if actor != None:
                results[i] = actor
    return actor, results
    
@user_passes_test(lambda u: u.is_superuser)
def process(request):
    output_string = StringIO()
    elements = []
    results = {}
    actors = {}
    #TODO:Process on upload
    with open(os.path.join(settings.MEDIA_ROOT, 'hansards/sample3.pdf'), 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            read_position = output_string.tell()
            interpreter.process_page(page)
            output_string.seek(read_position, 0)
            page_text = output_string.read()
            elements.append(page_text)
    
    hansard = Hansard.objects.get(id=1)
    #keep track of actor from the beginning
    actor = ""
    for page, element in enumerate(elements):
        lines = preprocessing(element)
        paras = getparagraphs(lines)
        actor, actors = getactors(paras, actor)
        results[page] = paras
        for line, para in enumerate(paras):
            politician = None
            if line in actors.keys():
                name = actors[line].replace(' ', '_')
                if Politician.objects.filter(name=name).count() == 1:
                    politician = Politician.objects.get(name=name)
            Paragraph.objects.get_or_create(page=page, line=line, content=para, politician=politician, hansard=hansard)
    return render(request, 'hansards/process.html', {'results': results}, {'actors': actors} )
def view(request, name):
    hansard = Hansard.objects.get(name=name)
    paragraphs = Paragraph.objects.filter(hansard=hansard)
    return render(request, 'hansards/view.html', {"hansard": hansard, "paragraphs": paragraphs} )
