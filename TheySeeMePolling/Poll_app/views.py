from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
    HTTP_201_CREATED,
    HTTP_200_OK
)

from .models import Poll, Question, Choice, Answer
from .serializers import Poll_Serializer, Question_Serializer, Choice_Serializer, Answer_Serializer

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


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def create_poll(request):
    serializer = Poll_Serializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        poll = serializer.save()
        return Response(Poll_Serializer(poll).data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def update_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'PUT':
        serializer = Poll_Serializer(poll, data=request.data, partial=True)
        if serializer.is_valid():
            poll = serializer.save()
            return Response(Poll_Serializer(poll).data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        poll.delete()
        return Response("Poll deleted", status=HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def create_question(request):
    serializer = Question_Serializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save()
        return Response(Question_Serializer(question).data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def update_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'PUT':
        serializer = Question_Serializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(Question_Serializer(question).data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return Response("Question deleted", status=HTTP_200_OK)
    
    
@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def create_choice(request):
    serializer = Choice_Serializer(data=request.data)
    if serializer.is_valid():
        choice = serializer.save()
        return Response(Choice_Serializer(choice).data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def update_choice(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    if request.method == 'PUT':
        serializer = Choice_Serializer(choice, data=request.data, partial=True)
        if serializer.is_valid():
            choice = serializer.save()
            return Response(Choice_Serializer(choice).data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        choice.delete()
        return Response("Choice deleted", status=HTTP_200_OK)
    
        
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_answers(request, user_id):
    answers = Answer.objects.filter(user_id=user_id)
    serializer = Answer_Serializer(answers, many=True)
    return Response(serializer.data) 


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_answer(request):
    serializer = Answer_Serializer(data=request.data)
    if serializer.is_valid():
        answer = serializer.save()
        return Response(Answer_Serializer(answer).data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    