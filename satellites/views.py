from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import SatelliteSerializer
from .models import Satellite
import requests, tle2czml, os
from pathlib import Path

@api_view(['GET'])
def satellites(request):
  if request.method == 'GET':
    try:
      value_list = Satellite.objects.values_list('type', flat=True)
   
      group_by_value = {}
      for value in value_list:
        group_by_value[value] = Satellite.objects.values().filter(type=value)
      
      reversed = dict(sorted(group_by_value.items(), reverse=True))
      return Response(reversed)
    except Satellite.DoesNotExist: 
      return JsonResponse({'error': 'Satellites not found.'}, status=404)


@api_view(['GET'])
def satellite(request, name):
  if request.method == "GET":
    tle_filename = "{}.txt".format(name)
    czml_filename = "{}.czml".format(name)

    BASE_DIR = Path(__file__).resolve().parent.parent
    tle2czml_path = os.path.join(BASE_DIR, 'staticfiles', 'tle2czml')

    if not os.path.exists(tle2czml_path):
      os.makedirs(tle2czml_path)

    for folder in ['tle', 'czml']:
      if not os.path.exists(os.path.join(tle2czml_path, folder)):
        os.makedirs(os.path.join(tle2czml_path, folder))

    tle_file_path = os.path.join(tle2czml_path, "tle", tle_filename)
    czml_file_path = os.path.join(tle2czml_path, "czml", czml_filename)

    if not os.path.exists(czml_file_path):
      if not os.path.exists(tle_file_path):
        response = requests.get("https://celestrak.org/NORAD/elements/gp.php?GROUP={}&FORMAT=tle".format(name))
      
        try:
          with open(tle_file_path, 'wb') as file:
            file.write(response.content)
          file.close()
        except Exception as e:
          print(f"Error occurred: {e}")
          return HttpResponse("An error occurred writing the TLE file", status=400)

      tle2czml.create_czml(tle_file_path, outputfile_path=czml_file_path)

    try:
      file = open(czml_file_path, 'rb')
      return FileResponse(file, as_attachment=True, filename=czml_filename)

    except FileNotFoundError:
      return Response({"error": ".czml file not found"}, status=404)
