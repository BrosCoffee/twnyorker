from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TopicSerializer
from .models import Topic

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'View List': '/topic_list',
        'View Detail': '/topic_detail/<str:pk>',
        'Create': '/topic_create',
        'Update': '/topic_update/<str:pk>',
        'Delete': '/topic_delete/<str:pk>',
    }

    return Response(api_urls)

@api_view(['GET'])
def topic_list(request):
    topics = Topic.objects.all().order_by('complete','-votes','-id')
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def topic_detail(request, pk):
    topic = Topic.objects.get(pk=pk)
    serializer = TopicSerializer(task, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def topic_create(request):
    serializer = TopicSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def topic_update(request, pk):
    topic = Topic.objects.get(pk=pk)
    serializer = TopicSerializer(instance=topic, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def topic_delete(request, pk):
    topic = Topic.objects.get(pk=pk)
    topic.delete()

    return Response('Successfully deleted topic!')
