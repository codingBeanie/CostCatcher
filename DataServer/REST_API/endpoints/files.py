from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Transaction


class Files(APIView):
    def get(self, request):
        try:
            data = Transaction.objects.values(
                'fileName', 'fileDate').distinct()
            return Response(status=200, data=data)
        except Exception as e:
            print("Error in Files API:", e)
            return Response(status=500, data="Files could not be queried")

    def delete(self, request):
        print("DELETE", request.data)
        try:
            data = request.data
            fileName = data['fileName']
            fileDate = data['fileDate']
            Transaction.objects.filter(
                fileName=fileName, fileDate=fileDate).delete()
            return Response(status=200, data="File has been deleted")
        except:
            return Response(status=500, data="File could not be deleted")
