from django.shortcuts import render

from .models import Doc
from .forms import UploadForm


def home(request):
    form = UploadForm(request.POST or None, request.FILES or None)
    if request.is_ajax():
        if form.is_valid():
            form.save()
            form = UploadForm()
    context = {
        'form': form
    }
    return render(request, 'docs/main.html', context)
