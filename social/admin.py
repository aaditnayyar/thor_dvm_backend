from django.contrib import admin
from .models import Post,Comment,UserProfile
from import_export.admin import ImportExportMixin
from .actions import export_as_xls

admin.site.register(Post)
admin.site.register(Comment)
#admin.site.register(Version)

class UserProfileAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['user','name', 'bio','dp']
    actions = [export_as_xls]
    
admin.site.register(UserProfile, UserProfileAdmin)

#from django.contrib import admin

#from reversion.admin import VersionAdmin
# @admin.register(Post)
# class ClientModelAdmin(VersionAdmin):
#       pass