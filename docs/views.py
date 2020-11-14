from django.shortcuts import render

from .models import Doc
from .forms import UploadForm
from .processing_file import Sheet


def home(request):
    form = UploadForm(request.POST or None, request.FILES or None)
    unique_value = None
    if request.is_ajax():
        if form.is_valid():
            form.save()
            unique_value = Sheet.proc(request.FILES['upload'])
            form = UploadForm()
    context = {
        'form': form,
        'result': unique_value
    }
    return render(request, 'docs/main.html', context)
