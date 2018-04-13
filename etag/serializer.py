from rest_framework import serializers
import json
from models import *
import os, requests

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
        fields = ('url','reader_id', 'description')#'user_id')

    def make_url(self, obj):
        """
        Build URL for Order instance
        """
        # Prepare the IDs you need for the URL reverse
        kwargs = {
            'reader_id': obj.reader_id,
        }
        url = reverse('readers-list', kwargs=kwargs)
        return self.context['request'].build_absolute_uri(url)
    #def create(self, validated_data):
     #   return Roosts.objects.using('purple').create(**validated_data)

class ReaderLocationSerializer(serializers.HyperlinkedModelSerializer):
    #source = LuSourceSerializer()
    reader_id = serializers.SlugRelatedField(slug_field='reader_id')
    #location_id = serializers.RelatedField(source='location_id.location_id', read_only=True)
    location_id = serializers.SlugRelatedField(slug_field='location_id')
    class Meta:
        model = ReaderLocation
        fields = ('url','reader_id','location_id','start_timestamp','end_timestamp',)
    #def create(self, validated_data):
     #   return Roosts.objects.using('purple').create(**validated_data)

class TaggedAnimalSerializer(serializers.HyperlinkedModelSerializer):
    tag_id = serializers.SlugRelatedField(slug_field='tag_id')
    field_data=WritableJSONField() #serializers.DictField()
    #animal_id = serializers.RelatedField(source='animal_id.animal_id', read_only=True)
    animal_id = serializers.SlugRelatedField(slug_field='animal_id')
    class Meta:
        model = TaggedAnimal
        fields = ('url','tag_id','animal_id','start_time','end_time','field_data',)
    #def create(self, validated_data):
     #   return Roosts.objects.using('purple').create(**validated_data)
	 
class TagOwnerSerializer(serializers.HyperlinkedModelSerializer):
    tag_id = serializers.SlugRelatedField(slug_field='tag_id')
    #user_id = serializers.SerializerMethodField('_user')
    #user_id = serializers.PrimaryKeyRelatedField(read_only=True,default=serializers.CurrentUserDefault())
    class Meta:
        model = TagOwner
        fields = ('url','tag_id','start_time','end_time',)#'user_id')
    #def create(self, validated_data):
     #   return Roosts.objects.using('purple').create(**validated_data)

class TagReadsSerializer(serializers.HyperlinkedModelSerializer):
    reader_id = serializers.SlugRelatedField(slug_field='reader_id')
    reader_url = serializers.HyperlinkedIdentityField(view_name='readers-detail')
    tag_id = serializers.SlugRelatedField(slug_field='tag_id')
    tag_url = serializers.HyperlinkedIdentityField(view_name='tags-detail')
    field_data = WritableJSONField()
    #user_id = serializers.PrimaryKeyRelatedField(read_only=True,default=serializers.CurrentUserDefault())
    #user_id = serializers.SerializerMethodField('_user')

    class Meta:
        model = TagReads
        fields = ('url','reader_id','tag_id','field_data','tag_read_time','public',)
    #def create(self, validated_data):
     #   return Roosts.objects.using('purple').create(**validated_data)
