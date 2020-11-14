from django.shortcuts import render, HttpResponse
import json

from .models import Doc
from .forms import UploadForm
from .processing_file import Sheet


def home(request):
    if request.method == 'POST':
        form = UploadForm(request.POST or None, request.FILES or None)
        if request.is_ajax():
            if form.is_valid():
                form.save()
                unique_value = Sheet.proc(request.FILES['upload'])
                form = UploadForm()
                context = {
                    # 'form': form,
                    'result': unique_value
                }
                return HttpResponse(
                    json.dumps(context),
                    content_type="application/json"
                )
    form = UploadForm()
    unique_value = None
    context = {
        'form': form,
        'result': unique_value
    }
    return render(request, 'docs/main.html', context)
