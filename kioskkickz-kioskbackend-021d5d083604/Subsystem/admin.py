from django.contrib import admin
from .models import BiometricSystemModel, RecordModel

# Register your models here.
class BiometricSystemModelAdmin(admin.ModelAdmin):
    exclude = ('isStarted',)

admin.site.register(BiometricSystemModel, BiometricSystemModelAdmin)
admin.site.register(RecordModel)

admin.site.site_header = 'Biometric System Manager'

admin.site.site_title = 'Biometric System Manager'