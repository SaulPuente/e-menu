from wsgiref.simple_server import demo_app
from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse

import os

from backend.data_access.dao_tables.dao_t_test import DAO_T_Test
from backend.logics.mysql_conn.lib_db_connector import Threading_DB_Connection


dbconfig = {
        "database_username": "sypr",
        "database_name": "e_menu",
        "database_password": "&!SSw^t!66mw:PB",
        "host": "e-menu.mysql.database.azure.com",
        "port": 3306
}
print(dbconfig)
# Create your views here.
def default(request):
    context = {"data":"Home Page of Django App"}
    return render(request,'api/default.html', context)

class test(APIView):
    permission_classes = (AllowAny,)

    def __init__(self):
        # self.json_builder     = Json_Builder()
        # self.jwt              = JWT_Lib()
        self.db_handler       = Threading_DB_Connection(dbconfig)
        self.dao_t_test         = DAO_T_Test(self.db_handler)

    def post(self, request):
        try:
            data        = request.data
            
            dto_tests = self.dao_t_test.select_all()

            test_list = list()

            for dto_test in dto_tests:
                test_dict = dict()
                test_dict["id"] = dto_test.id
                test_dict["name"] = dto_test.name
                test_dict["description"] = dto_test.description
                test_list.append(test_dict)
            response = dict()
            response['list'] = test_list

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)