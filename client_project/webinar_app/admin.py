# webinar_app/admin.py
from django.contrib import admin
from .models import Webinar, WebinarBooking, Payment

admin.site.register(Webinar)
admin.site.register(WebinarBooking)
admin.site.register(Payment)

