from django.http import HttpResponse


def index(request):
  return HttpResponse("Hello, world. You're at the backend root index. This exists because nature abhors a vacuum and dogs hate vacuum cleaners. Read into that what you will.")