from django.shortcuts import render
from .models import Parties  

def parties_list(request):
    parties = Parties.objects.all()  
    return render(request, 'parties_list.html', {'parties': parties})
