from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from cert.models import Assignment
from cert.models import Certificate
from cert.models import AssignedQuestion
from cert.models import QuizStructure
from cert.models import Question
from cert.models import Person
from os.path import join
from certify import settings
import random

import pdfrw
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4, landscape

def create_overlay(ass, certificate):
    c = canvas.Canvas('temp_overlay.pdf', pagesize=landscape(A4))

    c.setFillColorRGB(0.1, 0.8, 0.6)  # choose your font colour
    c.setFont("Helvetica", 30)  # choose your font type and font size

    c.drawCentredString(11*cm, 14*cm, f'{ass.person.first_name} {ass.person.last_name}')
    c.drawCentredString(11*cm, 9*cm, f'{ass.quiz_structure.name}')

    qrw = QrCodeWidget(f'https://cert.dsacademy.kz/media/{certificate.permanent_link}')
    b = qrw.getBounds()

    w = b[2] - b[0]
    h = b[3] - b[1]

    size = 200

    d = Drawing(1,1, transform=[size / w, 0, 0, size / h, 0, 0])
    d.add(qrw)

    renderPDF.draw(d, c, 29*cm - size, 20*cm - size)

    c.save()


def merge_pdfs(form_pdf, overlay_pdf, output):
    """
    Merge the specified fillable form PDF with the
    overlay PDF and save the output
    """
    form = pdfrw.PdfReader(form_pdf)
    olay = pdfrw.PdfReader(overlay_pdf)

    for form_page, overlay_page in zip(form.pages, olay.pages):
        merge_obj = pdfrw.PageMerge()
        overlay = merge_obj.add(overlay_page)[0]
        pdfrw.PageMerge(form_page).add(overlay).render()

    writer = pdfrw.PdfWriter()
    writer.write(output, form)


def index(request):
    user = request.user
    person = Person.objects.get(user=user)
    assignments = Assignment.objects.filter(hidden=False).filter(person=person).filter(complete=True)

    return render(request,"certificates.html",{"assignments":assignments})


def generate(request, id):
    ass = Assignment.objects.get(pk=id)
    if ass.certificate is None:
        certificate = Certificate()
        certificate.save()
    else:
        certificate = ass.certificate

    certificate.permanent_link = f'cert{certificate.id}_{random.randint(11111,99999)}.pdf'
    certificate.save()
    ass.certificate = certificate
    ass.save()

    create_overlay(ass, certificate)
    merge_pdfs(join(settings.BASE_DIR,'certificate_blank.pdf'),
               'temp_overlay.pdf',
               join(settings.MEDIA_ROOT, certificate.permanent_link))

    if "dsacademy" in request.build_absolute_uri():
        return HttpResponse(f"https://cert.dsacademy.kz/media/{certificate.permanent_link}")
    else:
        return HttpResponse(f"http://localhost:8000/media/{certificate.permanent_link}")