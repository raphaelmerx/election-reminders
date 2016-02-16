from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Voter
from .forms import UnsubscribeForm


def unsubscribe(request):
    try:
        voter = get_object_or_404(Voter, message__uuid=request.GET.get('uuid'))
    except ValueError:
        return HttpResponse('Invalid UUID', status=400)
    if request.method == 'GET':
        form = UnsubscribeForm(instance=voter)
    else:
        form = UnsubscribeForm(request.POST, instance=voter)
        if form.is_valid():
            form.save()
    return render(request, 'unsubscribe.html', {'form': form})
