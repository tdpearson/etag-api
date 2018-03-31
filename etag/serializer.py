from rest_framework import serializers
import json
from models import *

class WritableJSONField(serializers.WritableField):
    def to_native(self, obj):
        return obj #json.dumps(obj)
    def from_native(self,value):
	return value #json.loads(value)

class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""
    def to_internal_value(self, data):
        return data
    def to_representation(self, value):
        return value

class ReaderSerializer(serializers.HyperlinkedModelSerializer):
    #source = LuSourceSerializer()
    reader_location = serializers.SerializerMethodField('make_url')
    class Meta:
        model = Readers
        fields = ('url','reader_id','name', 'description')#'user_id')

    def make_url(self, obj):
        """
        Build URL for Order instance
        """
        # Prepare the IDs you need for the URL reverse
        kwargs = {
            'reader_id': obj.reader_id,
        }
        url = reverse('readerlocation-list', kwargs=kwargs)
        return self.context['request'].build_absolute_uri(url)
    #def create(self, validated_data):
     #   return Roosts.objects.using('purple').create(**validated_data)

class ReaderLocationSerializer(serializers.HyperlinkedModelSerializer):
    #source = LuSourceSerializer()
    reader = serializers.SlugRelatedField(slug_field='reader_id')
    class Meta:
        model = ReaderLocation
        fields = ('url','reader_id','latitude','longitude', 'start_timestamp','end_timestamp','active')
    #def create(self, validated_data):
     #   return Roosts.objects.using('purple').create(**validated_data)

class AnimalSerializer(serializers.HyperlinkedModelSerializer):
    tag = serializers.SlugRelatedField(slug_field='tag_id')
    field_data=WritableJSONField() #serializers.DictField()
    class Meta:
        model = TaggedAnimal
        fields = ('url','tag_id','animal_id','start_time','end_time','field_data',)
    #def create(self, validated_data):
     #   return Roosts.objects.using('purple').create(**validated_data)
	 
class TagsSerializer(serializers.HyperlinkedModelSerializer):
    #tag_animals = AnimalSerializer() 
    class Meta:
        model = TagOwner
        fields = ('url','tag_id','start_time','end_time')#'user_id')
    #def create(self, validated_data):
     #   return Roosts.objects.using('purple').create(**validated_data)

class TagReadsSerializer(serializers.HyperlinkedModelSerializer):
    #source = LuSourceSerializer()
    reader = serializers.SlugRelatedField(slug_field='reader_id')
    reader_url = serializers.HyperlinkedIdentityField(view_name='readers-detail')
    tag = serializers.SlugRelatedField(slug_field='tag_id')
    tag_url = serializers.HyperlinkedIdentityField(view_name='tags-detail')
    class Meta:
        model = TagReads
        fields = ('url','reader_id','tag_id', 'tag_read_time',)
    #def create(self, validated_data):
     #   return Roosts.objects.using('purple').create(**validated_data)
