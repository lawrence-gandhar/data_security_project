from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.


def index(request):
    return HttpResponse('hi')