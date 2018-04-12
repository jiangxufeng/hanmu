# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http import HttpResponse


def main(request):
    return HttpResponse('<h1 align="center">My Website</h1>')

