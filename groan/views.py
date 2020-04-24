from django.db.models import Avg
from django.shortcuts import render


# Create your views here.
from groan.models import Groan


def index(request):
    context = {
        'average': Groan.objects.all().aggregate(Avg('magnitude'))['magnitude__avg'],
    }
    return render(request, 'groan/index.html', context=context)
