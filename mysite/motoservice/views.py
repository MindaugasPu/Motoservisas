from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Motociklas, Paslauga, MotocikloModelis, Uzsakymas
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def index(request):
    num_motociklai = Motociklas.objects.all().count()
    num_paslaugos = Paslauga.objects.all().count()
    num_aptarnauta = Uzsakymas.objects.filter(status__exact='p').count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_motociklai': num_motociklai,
        'num_paslaugos': num_paslaugos,
        'num_aptarnauta': num_aptarnauta,
        'num_visits': num_visits
    }

    return render(request, 'index.html', context=context)

def motociklai(request):
    paginator = Paginator(Motociklas.objects.all(), 4)
    page_number = request.GET.get('page')
    paged_motociklai = paginator.get_page(page_number)
    context = {
        'motociklai': paged_motociklai
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
    paginate_by = 8
    template_name = 'uzsakymai.html'


class UzsakymasDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = 'uzsakymai_detail.html'


def search(request):
    query = request.GET.get('query')
    search_results = Motociklas.objects.filter(Q(klientas__icontains=query) | Q(valstybinis_NR__icontains=query) | Q(vin_kodas__icontains=query) | Q(motociklo_modelis_id__marke__icontains=query) | Q(motociklo_modelis_id__modelis__icontains=query))
    return render(request, 'search.html', {'motociklai': search_results, 'query': query})


class VartotojasListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    template_name = 'manouzsakymai.html'
    paginate_by = 10

    def get_queryset(self):
        return Uzsakymas.objects.filter(vartotojas=self.request.user)
