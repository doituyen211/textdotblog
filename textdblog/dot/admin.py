from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Dots)
admin.site.register(Users)
admin.site.register(DotUseHistory)
admin.site.register(Payments)
admin.site.register(PricePlan)
admin.site.register(UserPlanSubscriptions)
