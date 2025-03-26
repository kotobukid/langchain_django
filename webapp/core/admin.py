from django.contrib import admin

from .models import DesignedPrompt, GenerationHistory

admin.site.register(DesignedPrompt)
admin.site.register(GenerationHistory)
