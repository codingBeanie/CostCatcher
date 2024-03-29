from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Category
from ..serializer import CategorySerializer


class Categories(APIView):
    def get(self, request):
        queryID = request.query_params.get('id', None)
        if queryID:
            queryID = queryID.replace('/', '')
            data = Category.objects.get(id=queryID)
            serializer = CategorySerializer(data)
        else:
            data = Category.objects.all().order_by('name')
            serializer = CategorySerializer(data, many=True)
        return Response(status=200, data=serializer.data)

    def post(self, request):
        data = request.data
        if Category.objects.filter(name=data['name']).exists():
            return Response(status=400, data="Category already exists")

        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data="Category has been created")
        return Response(status=500, data="Category could not be created")

    def put(self, request):
        data = request.data
        category = Category.objects.get(id=data['id'])

        serializer = CategorySerializer(category, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data="Category has been updated")
        return Response(status=500, data="Category could not be updated")

    def delete(self, request):
        try:
            if request.data:
                category = Category.objects.get(id=request.data)
                category.delete()
                return Response(status=200, data="Category has been deleted")
            return Response(status=400, data="Invalid Category ID")
        except:
            return Response(status=500, data="Category could not be deleted")
