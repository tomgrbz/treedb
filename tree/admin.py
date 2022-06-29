from django.contrib import admin

# Register your models here.
#allows admin page to show these models to Developer/SuperUser
from .models import Calculation, Neighborhood, RadiusData, Tree, Street, Result, TreeType
admin.site.register(Tree)
admin.site.register(Neighborhood)
admin.site.register(Street)
admin.site.register(RadiusData)
admin.site.register(Result)
admin.site.register(Calculation)
admin.site.register(TreeType)