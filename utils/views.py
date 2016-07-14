from rest_framework.response import Response
from rest_framework import status

def r_success(result):
    return Response(
        {"success":True, "result":result},
        status=status.HTTP_200_OK
    )

def r_failure(error):
    return Response(
        {"success":False, "error":str(error)},
        status=status.HTTP_400_BAD_REQUEST
    )