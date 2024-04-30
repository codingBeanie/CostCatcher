from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Category
from ..serializer import CategorySerializer


class Categories(APIView):
    def get(self, request):
        try:
            queryID = request.query_params.get('id', None)
            queryName = request.query_params.get('name', None)
            categories = Category.objects.filter(user=request.user.id)

            # if a certain ID is queried
            if queryID and queryID != 'null':
                data = categories.get(id=queryID)
                serializer = CategorySerializer(data)

            # if a certain name is queried
            elif queryName:
                data = categories.get(name=queryName)
                serializer = CategorySerializer(data)

            # if no filter query is made, return all categories
            else:
                # sort Data by name
                queryList = []
                for category in categories:
                    queryList.append(category)
                queryList.sort(key=lambda x: x.name)

                serializer = CategorySerializer(queryList, many=True)
            return Response(status=200, data=serializer.data)
        except Exception as e:
            print("Error in Categories GET: ", e)
            return Response(status=500, data="Error in Categories GET")

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
