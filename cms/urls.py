from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import DetailView

from models import Article, Navigation

nav_headers = Navigation.objects.filter(parent=None).order_by('order')


class CmsView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(CmsView, self).get_context_data(**kwargs)
        context['nav_headers'] = nav_headers
        return context

    def get_object(self):
        try:
            return super(CmsView, self).get_object()
        except AttributeError:
            return Navigation.objects.get_first().article


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'sitemap', 'cms.views.sitemap', name='sitemap'),
    url(r'^(?P<slug>[\w-]+)/$', CmsView.as_view()),
    url(r'', CmsView.as_view())
]
