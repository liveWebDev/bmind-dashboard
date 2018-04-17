"""
Definition of urls for DataViz.
"""

# urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

admin.autodiscover()

favicon_view = RedirectView.as_view(url='/static/app/favicon.png', permanent=True)

urlpatterns = [
    url(r'^', include('app.urls')),
    url(r'^admin/', admin.site.urls)
]

# Active DEBUG Toolbar
# if settings.DEBUG:
#    import debug_toolbar

#    urlpatterns = [
#                      url(r'^__debug__', include(debug_toolbar.urls))
#                  ] + urlpatterns

# This is only required to support extension-style formats (e.g. /data.csv)


static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
