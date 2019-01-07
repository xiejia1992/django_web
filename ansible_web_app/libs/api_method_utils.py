from rest_framework import status
from rest_framework.response import Response


def get_model_list(request=None, Model=None, Serializer=None):
    model = Model.objects.all()
    serializer = Serializer(model, many=True)
    return Response(serializer.data)


def add_model(request=None, Model=None, Serializer=None):
    serializer = Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_model_id(request=None, id=None, Model=None, Serializer=None):
    try:
        model = Model.objects.get(id=id)
    except Model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = Serializer(model)
    return Response(serializer.data)


def put_model_id(request=None, id=None, Model=None, Serializer=None):
    try:
        model = Model.objects.get(id=id)
    except Model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = Serializer(model, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_model_id(request=None, id=None, Model=None,):
    try:
        model = Model.objects.get(id=id)
    except Model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    model.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
