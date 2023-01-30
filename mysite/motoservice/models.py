from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from PIL import Image


# Create your models here.
class MotocikloModelis(models.Model):
    marke = models.CharField('Markė', max_length=200)
    modelis = models.CharField('Modelis', max_length=200)
    gamybos_metai = models.TextField('Gamybos metai', max_length=2000, default='')
    cover = models.ImageField('Viršelis', upload_to='covers', null=True)

    def __str__(self):
        return f"{self.marke} {self.modelis}"

    class Meta:
        verbose_name = 'Motociklo modelis'
        verbose_name_plural = 'Motociklų modeliai'


class Motociklas(models.Model):
    valstybinis_NR = models.CharField('Valstybiniai numeriai', max_length=7)
    motociklo_modelis = models.ForeignKey(to="MotocikloModelis", on_delete=models.SET_NULL, null=True)
    vin_kodas = models.CharField("VIN kodas", max_length=17, help_text="17 simbolių")
    klientas = models.CharField("Klientas", max_length=100)
    metai = models.IntegerField("Metai")
    aprasymas = HTMLField("Aprašymas", null=True, blank=True)


    def __str__(self):
        return f"{self.metai} {self.motociklo_modelis} [{self.valstybinis_NR}]"

    class Meta:
        verbose_name = 'Motociklas'
        verbose_name_plural = 'Motociklai'

class Uzsakymas(models.Model):
    data = models.DateTimeField("Data", auto_now_add=True)
    motociklas = models.ForeignKey(to="Motociklas", on_delete=models.CASCADE)
    grazinimas = models.DateField("Grąžinimas", null=True, blank=True)
    vartotojas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"[{self.motociklas.valstybinis_NR}] {self.motociklas.motociklo_modelis}"

    def is_overdue(self):
        return self.grazinimas and date.today() > self.grazinimas

    LOAN_STATUS = (
        ('u', 'Užregistruota'),
        ('v', 'Vykdoma'),
        ('g', 'Galima paimti'),
        ('p', 'Paimta'),
        ('a', 'Atšaukta'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='u',
        help_text='Statusas',
    )

    def suma(self):
        suma = 0
        eilutes = self.eilutes.all()
        for eilute in eilutes:
            suma += eilute.kaina()
        return suma


    class Meta:
        verbose_name = 'Užsakymas'
        verbose_name_plural = 'Užsakymai'
        ordering = ['id']


class UzsakymoReview(models.Model):
    uzsakymas = models.ForeignKey(to='Uzsakymas', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Atsiliepimas', max_length=2000)

    class Meta:
        verbose_name = "Atsiliepimas"
        verbose_name_plural = 'Atsiliepimai'
        ordering = ['-date_created']

class UzsakymoEilute(models.Model):
    uzsakymas = models.ForeignKey(to="Uzsakymas", on_delete=models.CASCADE, related_name="eilutes")
    paslauga = models.ForeignKey(to="Paslauga", on_delete=models.SET_NULL, null=True)
    kiekis = models.IntegerField("Kiekis")

    def __str__(self):
        return f"{self.uzsakymas.motociklas.motociklo_modelis} {self.paslauga.pavadinimas}"

    def kaina(self):
        return self.paslauga.kaina * self.kiekis
    class Meta:
        verbose_name = 'Užsakymo eilutė'
        verbose_name_plural = 'Užsakymų eilutės'

class Paslauga(models.Model):
    pavadinimas = models.CharField('Pavadinimas', max_length=200)
    kaina = models.IntegerField('Kaina')

    def __str__(self):
        return f"{self.pavadinimas}"

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'


class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)

