from django.shortcuts import render
from .models import User, Profile
from .serializer import UserSerializer, MyTokenObtainPairSerializer, RegisterSerializer, PlaceSearchSerializer, AIRequestSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from .forms import SurveyForm, ProfileSurveyForm
import requests
from django.http import JsonResponse

import pathlib
import textwrap

import google.generativeai as genai
from IPython.display import display, Markdown

api_key = "AIzaSyD-823w2uUvdfj9X6AEGun6UOfh_geoO5Y"  # this is a fake key

genaiapi_key = "AIzaSyDe6ObFjVUpik-ISzUl4q5b-yWNxZy-REs"
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = ([AllowAny])
    serializer_class = RegisterSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.method == 'GET':
        context = f"Hey, {request.user.username}! You are logged in."
        return Response({'response': context}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        context = f"Hey, {request.user.username}! You have posted: {text}"
        return Response({'response': context}, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_places(request):
    serializer = PlaceSearchSerializer(data=request.query_params)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    print('get request received')

    queries = serializer.validated_data['queries']
    location = serializer.validated_data['location']
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': " ".join(queries),  # Join multiple queries into a single string
        'location': location,
        'wheelchair_accessible_entrance': 'true',
        'key': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    response = Response(data, status=status.HTTP_200_OK)

    response['Access-Control-Allow-Origin'] = '*'

    return response

@api_view(['GET'])
def ai_request_view(request):
    if request.method == 'GET':
        # Deserialize request data
        serializer = AIRequestSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            context = data.get('context', "")
            task = data.get('task', "")
            input_data_context = data.get('input_data_context', "")
            input_data = data.get('input_data', "")
            
            # Configure and use Generative AI model
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"You are a {context}. {task}. Below is {input_data_context}: {input_data}"
            response = model.generate_content(prompt)
            
            # Return response
            return Response({'response': response.text}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def survey(request):
    if request.method == 'POST':
        user_form = SurveyForm(request.POST)
        profile_form = ProfileSurveyForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return JsonResponse({'response': "Survey submitted successfully!"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    # If the request method is not POST or if the forms are not valid, return an error response
    return JsonResponse({'error': "Invalid data or request method"}, status=status.HTTP_400_BAD_REQUEST)



