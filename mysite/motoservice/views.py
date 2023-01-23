from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import Motociklas, Paslauga, MotocikloModelis, Uzsakymas

# Create your views here.
def index(request):
    num_motociklai = Motociklas.objects.all().count()
    num_paslaugos = Paslauga.objects.all().count()
    num_aptarnauta = Uzsakymas.objects.filter(status__exact='p').count()

    context = {
        'num_motociklai': num_motociklai,
        'num_paslaugos': num_paslaugos,
        'num_aptarnauta': num_aptarnauta,
    }

    return render(request, 'index.html', context=context)

def motociklai(request):
    motociklai = Motociklas.objects.all()
    context = {
        'motociklai': motociklai
    }
    print(motociklai)
    return render(request, 'motociklai.html', context=context)

def motociklas(request, motociklas_id):
    vienas_motociklas = get_object_or_404(Motociklas, pk=motociklas_id)
    return render(request, 'motociklas.html', {'motociklas': vienas_motociklas})

class PaslaugaListView(generic.ListView):
    model = Paslauga
    template_name = 'paslauga_list.html'

class UzsakymasListView(generic.ListView):
    model = Uzsakymas
    template_name = 'uzsakymai.html'


class UzsakymasDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = 'uzsakymai_detail.html'
