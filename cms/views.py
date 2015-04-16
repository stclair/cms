from django.shortcuts import render_to_response

from cms.models import Navigation

nav_headers = Navigation.objects.filter(parent=None).order_by('order')


def sitemap(request):
    sitemap = []
    for navigation in nav_headers:
        sitemap += navigation.flatten()
    return render_to_response('cms/sitemap.html', {'sitemap': sitemap, 'nav_headers': nav_headers})
