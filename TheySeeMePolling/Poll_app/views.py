from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from .models import Poll
from .serializers import Poll_Serializer

import datetime

@csrf_exempt
@api_view(["GET"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please send username and password'},
                        status=HTTP_401_UNAUTHORIZED)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid username or password'},
                        status=HTTP_401_UNAUTHORIZED)
    token, _ = Token.objects.get_or_create(user=user)
    print(token.key)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_polls(request):
    now = datetime.datetime.now().date()

    polls = Poll.objects.filter(end_date__gte=now).filter(start_date__lte=now)
    #polls = Poll.objects.all().filter(end_date__lte>now).filter(start_date__gte<now)
    
    serializer = Poll_Serializer(polls, many=True)
    return Response(serializer.data)