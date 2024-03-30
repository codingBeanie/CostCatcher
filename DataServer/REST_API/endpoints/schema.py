from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import ImportSchema
from ..serializer import ImportSchemaSerializer


class Schema(APIView):
    def get(self, request):
        try:
            data = ImportSchema.objects.first()
            serializer = ImportSchemaSerializer(data)
            return Response(status=200, data=serializer.data)
        except:
            return Response(status=500, data="Schema could not be queried")

    def put(self, request):
        data = request.data
        schema = ImportSchema.objects.first()
        serializer = ImportSchemaSerializer(schema, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data="Schema has been updated")
        return Response(status=500, data="Schema could not be updated")
