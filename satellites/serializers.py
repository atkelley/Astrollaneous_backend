from rest_framework import serializers 
from .models import Satellite


class SatelliteSerializer(serializers.ModelSerializer):
  class Meta:
    model = Satellite
    fields = ('id',
              'name',
              'acronym',
              'type',
              'title',
              'image_url',
              'text',
              'text_html',
              'created_date')
 