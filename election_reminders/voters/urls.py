from django.conf.urls import url

from .views import unsubscribe


urlpatterns = [
    url(r'unsubscribe', unsubscribe, name='unsubscribe'),
]
