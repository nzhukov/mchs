from django.contrib import admin
from .models import CustomUser, Approvals, PassedApprovals, Rank, Rtp, Post, NoAttestation, InitialTrainingPeriod, GDZS

class UserAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email', 'rank')
    list_display_links = ('fullname',)
    search_fields = ('fullname','email', 'gdzs')
 
class ValueAdmin(admin.ModelAdmin):
    list_display = ('value',)
    list_display_links = ('value',)
    search_fields = ('value',)

class PassedApprovalsAdmin(admin.ModelAdmin):
    list_display = ('approvalsname', 'fullname')
    list_display_links = ('approvalsname',)
    search_fields = ('approvalsname', 'fullname')

class GDZSAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'value')
    list_display_links = ('fullname',)
    search_fields = ('value', 'fullname')
    
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Post, ValueAdmin)
admin.site.register(Rank, ValueAdmin)
admin.site.register(PassedApprovals, PassedApprovalsAdmin)
admin.site.register(Approvals)
admin.site.register(NoAttestation, ValueAdmin)
admin.site.register(InitialTrainingPeriod)
admin.site.register(GDZS, GDZSAdmin)