from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('accounts.urls')),

    path('captcha/', include('captcha.urls')),
]

# Custom error handlers — shows friendly error pages instead of Django debug
handler404 = 'accounts.views.custom_404_view'
handler500 = 'accounts.views.custom_500_view'