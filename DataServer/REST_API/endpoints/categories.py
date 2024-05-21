from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Category
from ..serializer import CategorySerializer
import logging


class Categories(APIView):
    log = logging.getLogger("api")
    ####################################################################################################
    # GET
    ####################################################################################################

    def get(self, request):
        try:
            queryID = request.query_params.get('id', None)
            queryName = request.query_params.get('name', None)

            queryID = None if queryID == 'null' else queryID
            queryName = None if queryName == 'null' else queryName

            filters = {}
            filters['user'] = request.user.id

            # if a certain ID is queried
            if queryID:
                filters['id'] = queryID

            # if a certain name is queried
            if queryName:
                filters['name'] = queryName

            # if no filter query is made, return all categories
            categories = Category.objects.filter(**filters).order_by('name')
            serializer = CategorySerializer(categories, many=True)
            return Response(status=200, data=serializer.data)

        except Exception as e:
            self.log.error("API ERROR [categories/GET]:", e)
            return Response(status=500, data="Error in Categories GET")

    ####################################################################################################
    # POST
    ####################################################################################################
    def post(self, request):
        try:
            data = request.data
            user = request.user.id
            data['user'] = user

            if Category.objects.filter(user=user, name=data['name']).exists():
                return Response(status=400, data="Category already exists")

            serializer = CategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200, data="Category has been created")
            else:
                self.log.error(
                    "API ERROR [categories/POST]:", serializer.errors)
                return Response(status=400, data=serializer.errors)

        except Exception as e:
            self.log.error("API ERROR [categories/POST]:", e)
            return Response(status=500, data="Error in Categories POST")

    ####################################################################################################
    # PUT
    ####################################################################################################
    def put(self, request):
        try:
            data = request.data
            user = request.user.id
            data['user'] = user
            category = Category.objects.get(id=data['id'])

            serializer = CategorySerializer(category, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200, data="Category has been updated")
            else:
                self.log.error(
                    "API ERROR [categories/PUT]:", serializer.errors)
                return Response(status=400, data=serializer.errors)

        except Exception as e:
            self.log.error("API ERROR [categories/PUT]:", e)
            return Response(status=500, data="Error in Categories PUT")

    ####################################################################################################
    # DELETE
    ####################################################################################################
    def delete(self, request):
        try:
            category = Category.objects.filter(
                user=request.user.id, id=request.data)
            category.delete()
            return Response(status=200, data="Category has been deleted")

        except Exception as e:
            self.log.error("API ERROR [categories/DELETE]:", e)
            return Response(status=500, data="Error in Categories DELETE")
