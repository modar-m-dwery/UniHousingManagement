from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('institute.urls')),
    path('official/', include('officials.urls')),
    path('student/', include('students.urls')),
    path('', include('complaints.urls')),
    path('staff/', include('workers.urls')),
    
    path('auth/', include('django_auth.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)