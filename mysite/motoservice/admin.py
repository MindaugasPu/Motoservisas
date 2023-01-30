from django.contrib import admin
from .models import Motociklas, MotocikloModelis, Uzsakymas, UzsakymoEilute, Paslauga, UzsakymoReview, Profilis

class MotociklasAdmin(admin.ModelAdmin):
    list_display = ('motociklo_modelis', 'metai', 'valstybinis_NR', 'vin_kodas', 'klientas')
    list_filter = ('klientas', 'motociklo_modelis')
    search_fields = ('valstybinis_NR', 'vin_kodas')

class UzsakymoEiltueInLine(admin.TabularInline):
    model = UzsakymoEilute
    extra = 0

class UzsakymasAdmin(admin.ModelAdmin):
    list_display = ('motociklas', 'data', 'suma', 'vartotojas', 'grazinimas')
    list_editable = ('vartotojas', 'grazinimas')
    list_filter = ('status', 'vartotojas')
    inlines = [UzsakymoEiltueInLine]

class UzsakymoEiltueAdmin(admin.ModelAdmin):
    list_display = ('uzsakymas', 'paslauga', 'kiekis', 'kaina')
    list_filter = ('paslauga',)
    search_fields = ('uzsakymas',)

class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'kaina')

class UzsakymoReviewAdmin(admin.ModelAdmin):
    list_display = ('uzsakymas', 'date_created', 'reviewer', 'content')


# Register your models here.
admin.site.register(Motociklas, MotociklasAdmin)
admin.site.register(MotocikloModelis)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(UzsakymoEilute, UzsakymoEiltueAdmin)
admin.site.register(Paslauga, PaslaugaAdmin)
admin.site.register(UzsakymoReview, UzsakymoReviewAdmin)
admin.site.register(Profilis)
