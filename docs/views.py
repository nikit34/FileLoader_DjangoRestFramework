from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Doc
from .forms import UploadForm


def home(request):
    form = UploadForm(request.POST or None, request.FILES or None)
    if request.is_ajax():
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'up'})
    context = {
        'form': form,
    }
    return render(request, 'docs/main.html', context)

def file_upload_view(request):
    print(request.FILES)
    if request.method == 'POST':
        my_file = request.FILES.get('file')
        Doc.objects.create(upload=my_file)
        return HttpResponse('')
    return JsonResponse({'post': 'false'})