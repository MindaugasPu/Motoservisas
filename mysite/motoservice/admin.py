from django.contrib import admin
from .models import Motociklas, MotocikloModelis, Uzsakymas, UzsakymoEilute, Paslauga

# Register your models here.
admin.site.register(Motociklas)
admin.site.register(MotocikloModelis)
admin.site.register(Uzsakymas)
admin.site.register(UzsakymoEilute)
admin.site.register(Paslauga)