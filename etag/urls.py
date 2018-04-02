__author__ = 'mstacy'
from django.conf.urls import patterns, include, url
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from etag.views import ReadersViewSet,ReaderLocationViewSet,TagOwnerViewSet,TagReadsViewSet
from etag.views import AnimalViewSet,etagDataUploadView
from etag.views import LocationsViewSet


router = routers.SimpleRouter()
router.register('readers', ReadersViewSet)
router.register('reader_location', ReaderLocationViewSet)
router.register('locations', LocationsViewSet) 
router.register('tags', TagOwnerViewSet)
router.register('tag_reads', TagReadsViewSet)
router.register('tag_animal', AnimalViewSet)
#router.register('lusource', LuSourceViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^file-upload/',etagDataUploadView.as_view(), name='file-upload'),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['api', 'json', 'jsonp', 'xml', 'yaml'])
