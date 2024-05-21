from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Assignment, Category
from ..serializer import AssignmentSerializer
from ..bindings import createBinding, deleteBinding
import time
import logging


class Assignments(APIView):
    log = logging.getLogger("api")
    ####################################################################################################
    # GET
    ####################################################################################################

    def get(self, request):
        user = request.user.id
        assignments = Assignment.objects.filter(user=user)
        queryID = request.query_params.get('id', None)
        if queryID:
            data = assignments.get(id=queryID)
            serializer = AssignmentSerializer(data)
        else:
            data = assignments.all()
            serializer = AssignmentSerializer(data, many=True)

        endTime = time.time()
        return Response(status=200, data=serializer.data)

    ####################################################################################################
    # POST
    ####################################################################################################
    def post(self, request):
        try:
            data = request.data
            user = request.user.id
            data['user'] = user

            # Check if assignment already exists
            if Assignment.objects.filter(user=user, keyword=data['keyword']).exists():
                return Response(status=400, data="Assignment already exists")

            # create assignment
            serializer = AssignmentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                createBinding(serializer.instance)
                return Response(status=200, data="Assignment has been created")
            else:
                self.log.error(
                    "API ERROR [assignments/POST]:", serializer.errors)
                return Response(status=400, data=serializer.errors)

        except Exception as e:
            self.log.error("API ERROR [assignments/POST]:", e)
            return Response(status=500, data="Assignment could not be created")

    ####################################################################################################
    # PUT
    ####################################################################################################
    def put(self, request):
        data = request.data
        assignment = Assignment.objects.get(id=data['id'])
        deleteBinding(assignment)

        assignment.keyword = data['keyword']
        assignment.checkMode = data['checkMode']
        assignment.category = Category.objects.get(id=data['category'])
        assignment.save()
        createBinding(assignment)

        return Response(status=200, data="Assignment has been updated")

    ####################################################################################################
    # DELETE
    ####################################################################################################
    def delete(self, request):
        assignment = Assignment.objects.get(id=request.data)
        deleteBinding(assignment)
        return Response(status=200, data="Assignment has been deleted")
