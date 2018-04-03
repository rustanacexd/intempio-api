from django.conf import settings
# from django.urls import path, re_path, include, reverse_lazy
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
# from django.views.generic.base import RedirectView
# from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken import views
# from .users.views import UserViewSet, UserCreateViewSet
from .sunovion_events.views import SunovionCreateEvent

# router = DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'users', UserCreateViewSet)
admin.site.site_header = 'Intempio'
admin.site.site_title = 'Admin'
admin.site.index_title = 'Events Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/sunovion-events', SunovionCreateEvent.as_view(), name='sunovion-event-create'),
    # path('api/v1/', include(router.urls)),
    # path('api-token-auth/', views.obtain_auth_token),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    # re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
