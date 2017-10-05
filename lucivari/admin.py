from django.contrib import admin
from lucivari.models import Experiment, Conditions, Snv, Genes, Document, TemplateFile, UserProfile
#from lucivari.models import UserProfile

# Add in this class to customise the Admin Interface
class ExperimentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class ConditionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

#admin.site.register(Category, CategoryAdmin)
#admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
admin.site.register(Genes)
admin.site.register(Snv)
admin.site.register(Experiment)
admin.site.register(Conditions)
