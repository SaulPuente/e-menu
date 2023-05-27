from wsgiref.simple_server import demo_app
from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse

import os

from backend.data_access.dao_tables.dao_t_test import DAO_T_Test
from backend.data_access.dao_tables.dao_t_user import DAO_T_Users
from backend.logics.mysql_conn.lib_db_connector import Threading_DB_Connection
from backend.logics.jwt.lib_jwt import JWT_Lib

import time


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
        
class register(APIView):
    permission_classes = (AllowAny,)

    def __init__(self):
        # self.json_builder     = Json_Builder()
        # self.jwt              = JWT_Lib()
        self.db_handler         = Threading_DB_Connection(dbconfig)
        self.dao_t_users        = DAO_T_Users(self.db_handler)
        self.jwt                = JWT_Lib()
    
    def post(self, request):
        try:
            data        = request.data

            response = dict()
            
            email = data.get("email", "").strip()
            fname = data.get("fname", "").strip()
            lname = data.get("lname", "").strip()
            password = data.get("password", "").strip()

            if not email or not fname or not lname or not password:
                response["status"] = "WRONG"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            now_time    = int(time.time())
            exp_time    = now_time + int(1000)
            jwt_json    = {}
            jwt_json['exp'] = exp_time
            session_jwt = self.jwt.m_encode(json=jwt_json,secret=email)

            user_id = self.dao_t_users.insert_new_user(email, fname, lname, password, "active", session_jwt)
            
            response['status'] = "OK"
            response["id"] = user_id
            response["token"]   = session_jwt

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class login(APIView):
    permission_classes = (AllowAny,)

    def __init__(self):
        # self.json_builder     = Json_Builder()
        # self.jwt              = JWT_Lib()
        self.db_handler         = Threading_DB_Connection(dbconfig)
        self.dao_t_users        = DAO_T_Users(self.db_handler)
        self.jwt                = JWT_Lib()
    
    def post(self, request):
        try:
            data        = request.data

            response = dict()
            
            email = data.get("email", "").strip()
            password = data.get("password", "").strip()

            if not email or not password:
                response["status"] = "WRONG"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            dto_user = self.dao_t_users.select_by_email(email)

            if password != dto_user.password:
                response["status"] = "WRONG"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            now_time    = int(time.time())
            exp_time    = now_time + int(1000)
            jwt_json    = {}
            jwt_json['exp'] = exp_time
            session_jwt = self.jwt.m_encode(json=jwt_json,secret=email)

            self.dao_t_users.update_token(dto_user.id, session_jwt)

            response['status'] = "OK"
            response["token"]   = session_jwt

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)