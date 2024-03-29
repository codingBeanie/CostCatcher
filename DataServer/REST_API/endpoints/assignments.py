from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Assignment, Category
from ..serializer import AssignmentSerializer
from ..bindings import createBinding, deleteBinding


class Assignments(APIView):
    def get(self, request):
        queryID = request.query_params.get('id', None)
        if queryID:
            queryID = queryID.replace('/', '')
            data = Assignment.objects.get(id=queryID)
            serializer = AssignmentSerializer(data)
        else:
            data = Assignment.objects.all()
            serializer = AssignmentSerializer(data, many=True)
        return Response(status=200, data=serializer.data)

    def post(self, request):
        try:
            data = request.data
            keyword = data['keyword']

            if Assignment.objects.filter(keyword=keyword).exists():
                return Response(status=400, data="Assignment already exists")

            serializer = AssignmentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                createBinding(serializer.instance)
                return Response(status=200, data="Assignment has been created")

        except:
            return Response(status=500, data="Assignment could not be created")

    def put(self, request):
        data = request.data
        print(data)
        assignment = Assignment.objects.get(id=data['id'])
        deleteBinding(assignment)

        assignment.keyword = data['keyword']
        assignment.checkMode = data['checkMode']
        assignment.category = Category.objects.get(id=data['category'])
        assignment.save()
        createBinding(assignment)

        return Response(status=200, data="Assignment has been updated")

    def delete(self, request):
        assignment = Assignment.objects.get(id=request.data)
        deleteBinding(assignment)
        assignment.delete()
        return Response(status=200, data="Assignment has been deleted")
