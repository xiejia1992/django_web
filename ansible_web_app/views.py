# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render_to_response
from rest_framework.decorators import api_view
from models import Group, IP
from libs.serializers import GroupSerializer, IPSerializer
from libs.api_method_utils import get_model_list, add_model, get_model_id, put_model_id, delete_model_id


# Create your views here.
def ansible_index(request):
    all_ip_address = IP.objects.all()
    all_group = Group.objects.all()
    return render_to_response('ansible_index.html', {"all_ip_address":all_ip_address, "all_group":all_group})


@api_view(['GET', 'POST'])
def group_list(request):
    if request.method == 'GET':
        return get_model_list(request=request,
                              Model=Group,
                              Serializer=GroupSerializer)
    elif request.method == 'POST':
        return add_model(request=request,
                         Model=Group,
                         Serializer=GroupSerializer)

@api_view(['GET', 'PUT', 'DELETE'])
def group_detail(request, id):
    if request.method == 'GET':
        return get_model_id(request=request,
                            id=id,
                            Model=Group,
                            Serializer=GroupSerializer)
    elif request.method == 'PUT':
        return put_model_id(request=request,
                            id=id, 
                            Model=Group,
                            Serializer=GroupSerializer)
    elif request.method == 'DELETE':
        return delete_model_id(request=request,
                               id=id,
                               Model=Group)

@api_view(['GET', 'POST'])
def ip_list(request):
    if request.method == 'GET':
        return get_model_list(request=request,
                              Model=IP,
                              Serializer=IPSerializer)
    elif request.method == 'POST':
        return add_model(request=request,
                         Model=IP,
                         Serializer=IPSerializer)

@api_view(['GET', 'PUT', 'DELETE'])
def ip_detail(request, id):
    if request.method == 'GET':
        return get_model_id(request=request,
                            id=id,
                            Model=IP,
                            Serializer=IPSerializer)
    elif request.method == 'PUT':
        return put_model_id(request=request,
                            id=id, 
                            Model=IP,
                            Serializer=IPSerializer)
    elif request.method == 'DELETE':
        return delete_model_id(request=request,
                               id=id,
                               Model=IP)

