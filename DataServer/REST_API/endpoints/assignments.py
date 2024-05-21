from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Assignment, Category
from ..serializer import AssignmentSerializer
from ..bindings import createBinding, deleteBinding
import logging


class Assignments(APIView):
    log = logging.getLogger("api")
    ####################################################################################################
    # GET
    ####################################################################################################

    def get(self, request):
        try:
            user = request.user.id
            queryID = request.query_params.get('id', None)
            queryID = None if queryID == 'null' else queryID

            filters = {}
            filters['user'] = user

            if queryID:
                filters['id'] = queryID

            assignments = Assignment.objects.filter(
                **filters).order_by('keyword')
            serializer = AssignmentSerializer(assignments, many=True)
            return Response(status=200, data=serializer.data)

        except Exception as e:
            self.log.error("API ERROR [assignments/GET]:", e)
            return Response(status=500, data="Error in Assignments GET")

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
        try:
            data = request.data
            assignment = Assignment.objects.get(
                id=data['id'], user=request.user.id)
            deleteBinding(assignment)

            data['user'] = request.user.id
            data['category'] = Category.objects.get(
                id=data['category'], user=request.user.id).id
            serializer = AssignmentSerializer(assignment, data=data)
            if serializer.is_valid():
                serializer.save()
                createBinding(serializer.instance)
                return Response(status=200, data="Assignment has been updated")
            else:
                self.log.error(
                    "API ERROR [assignments/PUT]:", serializer.errors)
                return Response(status=400, data=serializer.errors)

        except Exception as e:
            self.log.error("API ERROR [assignments/PUT]:", e)
            return Response(status=500, data="Assignment could not be updated")

    ####################################################################################################
    # DELETE
    ####################################################################################################
    def delete(self, request):
        try:
            assignment = Assignment.objects.get(
                id=request.data, user=request.user.id)
            deleteBinding(assignment)
            return Response(status=200, data="Assignment has been deleted")
        except Exception as e:
            self.log.error("API ERROR [assignments/DELETE]:", e)
            return Response(status=500, data="Assignment could not be deleted")
