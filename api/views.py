import os
import requests
from django.http import HttpResponse, JsonResponse


def index(request):
  return HttpResponse("Hello, world. You're at the backend root index. This exists because nature abhors a vacuum and dogs hate vacuum cleaners. Read into that what you will...")


def nasa(request, id=None):
    api_url = "https://techport.nasa.gov/api/projects"
    params = {
      "api_key": os.environ.get("NASA_API_KEY")
    }

    if id:
      api_url = f"https://techport.nasa.gov/api/projects/{id}"
    response = requests.get(api_url, params=params)
    return JsonResponse(response.json())