from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Motociklas, Paslauga, UzsakymoEilute, Uzsakymas
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import UzsakymoReviewForm, UserUpdateForm,  ProfilisUpdateForm, VartotojoUzsakymasCreateForm, UzsakymasPagalVartotojasUpdateForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin


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

    # nurodome, kur atsidursime komentaro s??km??s atveju.
    def get_success_url(self):
        return reverse('uzsakymas_detail', kwargs={'pk': self.object.id})

    # standartinis post metodo perra??ymas, naudojant FormMixin, galite kopijuoti tiesiai ?? savo projekt??.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # ??tai ??ia nurodome, kad knyga bus b??tent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijung??s.
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

class UzsakymasPagalVartotojasCreateView(LoginRequiredMixin, generic.CreateView):
    model = Uzsakymas
    # fields = ['motociklas', 'grazinimas']
    success_url = '/motoservice/manouzsakymai/'
    template_name = 'vartotojo_uzsakymai_form.html'
    form_class = VartotojoUzsakymasCreateForm

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        return super().form_valid(form)

class UzsakymasPagalVartotojasUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Uzsakymas
    # fields = ['motociklas', 'grazinimas', 'status']
    # success_url = '/motoservice/manouzsakymai/'
    template_name = 'vartotojo_uzsakymai_form.html'
    form_class = UzsakymasPagalVartotojasUpdateForm

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        return super().form_valid(form)

    def test_func(self):
        uzsakymas = self.get_object()
        return self.request.user == uzsakymas.vartotojas

    def get_success_url(self):
        return reverse('uzsakymas_detail', kwargs={'pk': self.object.id})

class UzsakymasPagalVartotojasDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Uzsakymas
    success_url = '/motoservice/manouzsakymai/'
    template_name = 'vartotojo_uzsakymai_delete.html'

    def test_func(self):
        uzsakymas = self.get_object()
        return self.request.user == uzsakymas.vartotojas


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reik??mes i?? registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slapta??od??iai
        if password == password2:
            # tikriname, ar neu??imtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} u??imtas!')
                return redirect('register')
            else:
                # tikriname, ar n??ra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. pa??tu {email} jau u??registruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame nauj?? vartotoj??
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} u??registruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slapta??od??iai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')


@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context)

class PaslaugosRedagavimasUpdateView(generic.UpdateView):
    model = UzsakymoEilute
    fields = ['paslauga', 'kiekis']
    template_name = 'paslaugosredagavimas_form.html'

    def get_success_url(self):
        return reverse('uzsakymas_detail', kwargs={'pk': self.kwargs['pk2']})

class PaslaugosTrinimoView(generic.DeleteView):
    model = UzsakymoEilute
    template_name = 'paslaugostrinimas_form.html'
    context_object_name = 'eilute'

    def get_success_url(self):
        return reverse('uzsakymas_detail', kwargs={'pk': self.kwargs['pk2']})


class PaslaugaPridetiCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = UzsakymoEilute
    fields = ['paslauga', 'kiekis']
    template_name = 'paslaugospridejimas_form.html'

    def get_success_url(self):
        return reverse('uzsakymas_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)



    def test_func(self):
        uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['pk'])
        return self.request.user == uzsakymas.vartotojas

