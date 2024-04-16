from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Category
from ..serializer import CategorySerializer


class Categories(APIView):
    def get(self, request):
        queryID = request.query_params.get('id', None)
        queryName = request.query_params.get('name', None)
        categories = Category.objects.filter(user=request.user.id)
        if queryID:
            data = categories.get(id=queryID)
            serializer = CategorySerializer(data)
        elif queryName:
            data = categories.get(name=queryName)
            serializer = CategorySerializer(data)
        else:
            data = categories.order_by('name')
            serializer = CategorySerializer(data, many=True)
        return Response(status=200, data=serializer.data)

    def post(self, request):
        data = request.data
        user = request.user.id
        data['user'] = user

        categories = Category.objects.filter(user=user)
        if categories.filter(name=data['name']).exists():
            return Response(status=400, data="Category already exists")

        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data="Category has been created")
        return Response(status=500, data=serializer.errors)

    def put(self, request):
        data = request.data
        user = request.user.id
        data['user'] = user
        categories = Category.objects.filter(user=user)
        category = categories.get(id=data['id'])

        serializer = CategorySerializer(category, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data="Category has been updated")
        return Response(status=500, data=serializer.errors)

    def delete(self, request):
        if request.data:
            categories = Category.objects.filter(user=request.user.id)
            category = categories.get(id=request.data)
            category.delete()
            return Response(status=200, data="Category has been deleted")
        return Response(status=400, data="Invalid Category ID")
