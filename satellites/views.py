from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import SatelliteSerializer
from .models import Satellite
# import requests, tle2czml, os


@api_view(['GET'])
def satellites(request):
  if request.method == 'GET':
    try:
      value_list = Satellite.objects.values_list('type', flat=True)
   
      group_by_value = {}
      for value in value_list:
        group_by_value[value] = Satellite.objects.values().filter(type=value)
      
      return Response(group_by_value)
    except Satellite.DoesNotExist: 
      return JsonResponse({'error': 'Satellites not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def satellite(request, name):
  if request.method == "GET":
    satellites = list(Satellite.objects.values())
    satellites_list = [entry for entry in satellites]

    result = None
    for satellite in satellites_list:
      for key, value in satellite.items():
        if key == 'acronym' and value == name:
          result = satellite
          break

    # base_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP={}&FORMAT=tle".format(name)
    # r = requests.get(base_url)

    # input_file = "static/mySpaceStuff/tle2czml/tle_{}.txt".format(name)
    
    # with open(input_file, 'wb') as f:
    #   f.write(r.content)
    # f.close()

    # output_file = "static/mySpaceStuff/tle2czml/tle_{}.czml".format(name)
    # tle2czml.create_czml(input_file, outputfile_path=output_file)
    return JsonResponse(result, safe=False)