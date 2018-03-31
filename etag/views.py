from django.shortcuts import render
from rest_framework.authtoken.models import Token
#from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets, filters, status
from rest_framework.renderers import BrowsableAPIRenderer, JSONPRenderer,JSONRenderer,XMLRenderer,YAMLRenderer #, filters
from .renderer import eventdropsJSONRenderer
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser,FileUploadParser
#from renderer import CustomBrowsableAPIRenderer
from filters import *
from etag.models import *
from serializer import ReaderSerializer, AnimalSerializer,ReaderLocationSerializer,TagsSerializer,TagReadsSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import os, requests,json
#import DjangoModelPermissionsOrAnonReadOnly


class ReadersViewSet(viewsets.ModelViewSet):
    """
    RFID Readers table view set.
    """
    model = Readers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ReaderSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ReadersFilter
    search_fields = ('user', 'description',)
    ordering_fields = '__all__'
    
    def get_queryset(self):
        user = self.request.user
	if self.request.user.is_authenticated():
        	if not user:
            		return []
		#private_tags = TagReads.objects.filter(public=False,user=user.id).values_list('tag_id')
		private_tag_readers = TagReads.objects.filter(public=False,user=user.id).values_list('reader_id')
        	return Readers.objects.filter(reader_id__in=private_tag_readers)
	#public_tags = Tags.objects.filter(public=True).values_list('tag_id')
        public_tag_readers = TagReads.objects.filter(public=True).values_list('reader_id')
	return Readers.objects.filter(reader_id__in=public_tag_readers)

    def create(self, request):
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            reader = Readers.objects.create(reader_id=serializer.data['reader_id'],name=serializer.data['name'],description=serializer.data['description'])
            reader.user_id = self.request.user.id
            reader.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReaderLocationViewSet(viewsets.ModelViewSet):
    """
    Reader Location table view set.
    """
    model = ReaderLocation
    queryset = ReaderLocation.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ReaderLocationSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ReaderLocationFilter
    search_fields = ('start_timestamp','end_timestamp')
    ordering_fields = '__all__'
	
    def get_queryset(self):
        user = self.request.user
	if self.request.user.is_authenticated():
        	if not user:
            		return []
		#private_tags = Tags.objects.filter(public=False,user_id=user.id).values_list('tag_id')
        	private_tag_readers = TagReads.objects.filter(public=False,user=user.id).values_list('reader_id')
		return ReaderLocation.objects.filter(reader_id__in=private_tag_readers)
	#public_tags = Tags.objects.filter(public=True).values_list('tag_id')
	public_tag_readers = TagReads.objects.filter(public=True).values_list('reader_id')
	return ReaderLocation.objects.filter(reader_id__in=public_tag_readers)

	
class AnimalViewSet(viewsets.ModelViewSet):
    """
    Animal table view set.
    """
    model = TaggedAnimal
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = AnimalSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = TaggedAnimalFilter
    ordering_fields = '__all__'
	
    def get_queryset(self):
        user = self.request.user
	if self.request.user.is_authenticated():
        	if not user:
            		return []
		user_tags = TagOwner.objects.filter(user=user.id).value_list('tag_id')
		#private_tags = TagReads.objects.filter(public=False,tag_id__in=user_tags).values_list('tag_id').distinct()
        	return TaggedAnimal.objects.filter(tag_id__in=user_tags,public=False)
	public_tags = TagReads.objects.filter(public=True).values_list('tag_id').distinct()
        return TaggedAnimal.objects.filter(tag_id__in=public_tags)

	
class TagsViewSet(viewsets.ModelViewSet):
    """
    Tags table view set.
    """
    model = TagOwner
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = TagsSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter ,filters.OrderingFilter)
    filter_class = TagOwnerFilter
    search_fields = ('tag_id',)
    ordering_fields = '__all__'
	
    def get_queryset(self):
        user = self.request.user
	if self.request.user.is_authenticated():
        	if not user:
            		return []
        	return TagOwner.objects.filter(user=user.id)
	public_tags = TagReads.objects.filter(public=True).values_list('tag_id').distinct()
	return TagOwner.objects.filter(tag_id__in=public_tags)
		
    def create(self, request):
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            reader = Tags.objects.create(tag_id=serializer.data['tag_id'],name=serializer.data['name'],description=serializer.data['description'])
            reader.user_id = self.request.user.id
            reader.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
class TagReadsViewSet(viewsets.ModelViewSet):
    """
    TagReads table view set.
    """
    model = TagReads
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = TagReadsSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer,eventdropsJSONRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = TagReadsFilter
    search_fields = ('tag_id',)
    ordering_fields =  '__all__' 
	
    def get_queryset(self):
	user = self.request.user
	if self.request.user.is_authenticated():
        	if not user:
            		return []
		else :             
        		return TagReads.objects.filter(user_id = user.id)
	public_tags = TagReads.objects.filter(public=True).values_list('tag_id').distinct()
	return TagReads.objects.filter(tag_id__in=public_tags)
	

class etagDataUploadView(APIView):
        permission_classes =(IsAuthenticated,)
        #parser_classes = (MultiPartParser, FormParser,FileUploadParser,)
        parser_classes = (FileUploadParser,)
        renderer_classes = (JSONRenderer,)

        def post(self, request, uploadDirectory="/data/file_upload",format=None):
                #Get Token for task submission
                tok = Token.objects.get_or_create(user=self.request.user)
                headers = {'Authorization':'Token {0}'.format(str(tok[0])),'Content-Type':'application/json'} 
                #check if uploadDirectory exists
                if not os.path.isdir(uploadDirectory):
                    os.makedirs(uploadDirectory)
                result={} #'var':dir(request),'fpath':request.build_absolute_uri().split('/')}
                local_file=""
                reader_id = request.DATA.get("reader_id")
                public_id=  request.DATA.get("myCheck")
                if public_id != '1':
					public_id=False
                if public_id == '1':
					public_id=True
                #result={"reader_id":reader_id,"public_id":public_id}
                #return Response(result)
                for key,value in request.FILES.iteritems():
                        filename= value.name
                        local_file = "%s/%s" % (uploadDirectory,filename)
                        self.handle_file_upload(request.FILES[key],local_file)
                        result[key]=local_file
                #Request task
                task_name = "etagq.tasks.tasks.etagDataUpload"
                payload={"function": task_name,"queue": "celery","args":[reader_id,local_file,str(tok[0]),public_id],"kwargs":{},"tags":[]}
                components = request.build_absolute_uri().split('/')
                hostname = os.environ.get("host_hostname", components[2])
                r=requests.post("{0}//{1}/api/queue/run/etagq.tasks.tasks.etagDataUpload/.json".format(components[0],hostname),data=json.dumps(payload),headers=headers)
                return Response(r.json())


        def handle_file_upload(self,f,filename):
                if f.multiple_chunks():
                        with open(filename, 'wb+') as temp_file:
                                for chunk in f.chunks():
                                        temp_file.write(chunk)
                else:
                        with open(filename, 'wb+') as temp_file:
                                temp_file.write(f.read())
