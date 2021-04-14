from django.shortcuts import render
from apps.OD_data import models
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
# Create your views here.


class CategoryView(APIView):
    """标签类别"""

    def get(self, request):
        category = models.LabelCategory.objects.all()
        res = CategorySerializer(category, many=True) # Serializer 的主要工作是将 Python 数据结构序列化为其它格式（XML／JSON 等等）。
        return Response({
            'code': 200,
            'message': 'Are you OK?',
            'category_name': res.data,
        },
        status=status.HTTP_200_OK,)


