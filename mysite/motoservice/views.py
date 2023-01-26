from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Motociklas, Paslauga, MotocikloModelis, Uzsakymas
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import UzsakymoReviewForm
from django.views.generic.edit import FormMixin

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


class UzsakymasDetailView(FormMixin, generic.DetailView):
    model = Uzsakymas
    template_name = 'uzsakymai_detail.html'
    form_class = UzsakymoReviewForm

    # nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse('uzsakymas_detail', kwargs={'pk': self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.uzsakymas = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(UzsakymasDetailView, self).form_valid(form)


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

@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')

