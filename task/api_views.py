from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from task.serializers import TaskSerializer
from task.models import Task


class TasksPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class TaskList(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('title', 'description')
    pagination_class = TasksPagination

    def get_queryset(self):
        queryset = Task.objects.all()
        return queryset


class TaskCreate(CreateAPIView):
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class TaskRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    lookup_field = 'id'
    serializer_class = TaskSerializer

    def delete(self, request, *args, **kwargs):
        task_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('task_data_{}'.format(task_id))
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            task = response.data
            cache.set('task_data_{}'.format(task['id']), {
                'title': task['title'],
                'description': task['description'],
            })
        return response
