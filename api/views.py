from wsgiref.simple_server import demo_app
from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse

import os

from backend.data_access.dao_tables.dao_t_test import DAO_T_Test
from backend.data_access.dao_tables.dao_t_user import DAO_T_Users
from backend.data_access.dao_tables.dao_t_recipe import DAO_T_Recipes
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
        self.dao_t_recipes      = DAO_T_Recipes(self.db_handler)
    
    def post(self, request):
        try:
            data        = request.data
            
            self.dao_t_recipes.alter_column()

            response = dict()

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
            fname = data.get("fname", "Nombre").strip()
            lname = data.get("lname", "Apellido").strip()
            password = data.get("password", "").strip()

            if not email or not password:
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
        
class newRecipe(APIView):
    permission_classes = (AllowAny,)

    def __init__(self):
        # self.json_builder     = Json_Builder()
        # self.jwt              = JWT_Lib()
        self.db_handler         = Threading_DB_Connection(dbconfig)
        self.dao_t_users        = DAO_T_Users(self.db_handler)
        self.dao_t_recipes      = DAO_T_Recipes(self.db_handler)
        self.jwt                = JWT_Lib()
    
    def post(self, request):
        try:
            data        = request.data

            response = dict()
            
            email = data.get("email", "").strip()
            token = data.get("token", "").strip()

            name = data.get("name", "").strip()
            description = data.get("description", "").strip()
            image = data.get("image", "").strip()
            ingredients = data.get("ingredients", "")
            steps = data.get("steps", "")
            price = data.get("price", "")
            location = data.get("location", "")
            place_name = data.get("place_name", "")

            if not name or not description or not image or not price or not location or not place_name:
                response["status"] = "MISSING DATA"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # dto_user = self.dao_t_users.select_by_email(email)

            # if not dto_user:
            #     response["status"] = "USER NOT FOUND"
            #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # if token != dto_user.token:
            #     response["status"] = "WRONG TOKEN"
            #     return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            info = {
                "ingredients": ingredients,
                "steps": steps
            }

            recipe_id = self.dao_t_recipes.insert_new(name, description, image, info, price, location, place_name)

            response['status'] = "OK"
            response["id"]   = recipe_id

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class recipes(APIView):
    permission_classes = (AllowAny,)

    def __init__(self):
        # self.json_builder     = Json_Builder()
        # self.jwt              = JWT_Lib()
        self.db_handler         = Threading_DB_Connection(dbconfig)
        self.dao_t_users        = DAO_T_Users(self.db_handler)
        self.dao_t_recipes      = DAO_T_Recipes(self.db_handler)
        self.jwt                = JWT_Lib()
    
    def post(self, request):
        try:
            data        = request.data

            response = dict()
            
            email = data.get("email", "").strip()
            token = data.get("token", "").strip()

            # if not email or not recipe or not token:
            #     response["status"] = "MISSING DATA"
            #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # dto_user = self.dao_t_users.select_by_email(email)
            
            # if not dto_user:
            #     response["status"] = "USER NOT FOUND"
            #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # if token != dto_user.token:
            #     response["status"] = "WRONG DATA"
            #     return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            dto_recipes = self.dao_t_recipes.select_all()

            recipes_list = list()

            for dto_recipe in dto_recipes:
                recipe_dict = dict()

                recipe_dict["id"] = dto_recipe.id
                recipe_dict["name"] = dto_recipe.name
                recipe_dict["description"] = dto_recipe.description
                recipe_dict["image"] = dto_recipe.image
                recipe_dict["ingredients"] = dto_recipe.ingredients
                recipe_dict["steps"] = dto_recipe.steps
                recipe_dict["price"] = dto_recipe.price
                recipe_dict["location"] = dto_recipe.location
                recipe_dict["place_name"] = dto_recipe.place_name

                recipes_list.append(recipe_dict)

            response['status'] = "OK"
            response["recipes"]   = recipes_list

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class recipe(APIView):
    permission_classes = (AllowAny,)

    def __init__(self):
        # self.json_builder     = Json_Builder()
        # self.jwt              = JWT_Lib()
        self.db_handler         = Threading_DB_Connection(dbconfig)
        self.dao_t_users        = DAO_T_Users(self.db_handler)
        self.dao_t_recipes      = DAO_T_Recipes(self.db_handler)
        self.jwt                = JWT_Lib()
    
    def post(self, request):
        try:
            data        = request.data

            response = dict()
            
            email = data.get("email", "").strip()
            token = data.get("token", "").strip()
            recipe = data.get("recipe", 0)

            if not recipe:# or not token:
                response["status"] = "MISSING DATA"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # dto_user = self.dao_t_users.select_by_email(email)
            
            # if not dto_user:
            #     response["status"] = "USER NOT FOUND"
            #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # if token != dto_user.token:
            #     response["status"] = "WRONG TOKEN"
            #     return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            dto_recipe = self.dao_t_recipes.select_by_id(recipe)

            if not dto_recipe:
                response["status"] = "RECIPE NOT FOUND"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            recipe_dict = dict()

            recipe_dict["id"] = dto_recipe.id
            recipe_dict["name"] = dto_recipe.name
            recipe_dict["description"] = dto_recipe.description
            recipe_dict["image"] = dto_recipe.image
            recipe_dict["ingredients"] = dto_recipe.ingredients
            recipe_dict["steps"] = dto_recipe.steps
            recipe_dict["price"] = dto_recipe.price
            recipe_dict["location"] = dto_recipe.location
            recipe_dict["place_name"] = dto_recipe.place_name

            response['status'] = "OK"
            response["recipe"]  = recipe_dict

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class updateRecipe(APIView):
    permission_classes = (AllowAny,)

    def __init__(self):
        # self.json_builder     = Json_Builder()
        # self.jwt              = JWT_Lib()
        self.db_handler         = Threading_DB_Connection(dbconfig)
        self.dao_t_users        = DAO_T_Users(self.db_handler)
        self.dao_t_recipes      = DAO_T_Recipes(self.db_handler)
        self.jwt                = JWT_Lib()
    
    def post(self, request):
        try:
            data        = request.data

            response = dict()
            
            email = data.get("email", "").strip()
            token = data.get("token", "").strip()

            recipe = data.get("recipe", 0)

            if not recipe:# or not token:
                response["status"] = "MISSING DATA"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # dto_user = self.dao_t_users.select_by_email(email)
            
            # if not dto_user:
            #     response["status"] = "USER NOT FOUND"
            #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # if token != dto_user.token:
            #     response["status"] = "WRONG TOKEN"
            #     return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            dto_recipe = self.dao_t_recipes.select_by_id(recipe)

            if not dto_recipe:
                response["status"] = "RECIPE NOT FOUND"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            
            name = data.get("name", dto_recipe.name).strip()
            description = data.get("description", dto_recipe.description).strip()
            image = data.get("image", dto_recipe.image).strip()
            ingredients = data.get("ingredients", dto_recipe.ingredients)
            steps = data.get("steps", dto_recipe.steps)
            price = data.get("price", dto_recipe.price)
            location = data.get("location", dto_recipe.location)
            place_name = data.get("place_name", dto_recipe.place_name)

            info = {
                "ingredients": ingredients,
                "steps": steps
            }

            self.dao_t_recipes.update_by_id(dto_recipe.id, name, description, image, info, price, location, place_name)            

            response['status'] = "OK"

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class deleteRecipe(APIView):
    permission_classes = (AllowAny,)

    def __init__(self):
        # self.json_builder     = Json_Builder()
        # self.jwt              = JWT_Lib()
        self.db_handler         = Threading_DB_Connection(dbconfig)
        self.dao_t_users        = DAO_T_Users(self.db_handler)
        self.dao_t_recipes      = DAO_T_Recipes(self.db_handler)
        self.jwt                = JWT_Lib()
    
    def post(self, request):
        try:
            data        = request.data

            response = dict()
            
            email = data.get("email", "").strip()
            token = data.get("token", "").strip()

            recipe = data.get("recipe", 0)

            if not recipe:# or not token:
                response["status"] = "MISSING DATA"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # dto_user = self.dao_t_users.select_by_email(email)

            # if not dto_user:
            #     response["status"] = "USER NOT FOUND"
            #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # if token != dto_user.token:
            #     response["status"] = "WRONG TOKEN"
            #     return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            dto_recipe = self.dao_t_recipes.select_by_id(recipe)

            if not dto_recipe:
                response["status"] = "RECIPE NOT FOUND"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            self.dao_t_recipes.delete_by_id(dto_recipe.id)            

            response['status'] = "OK"

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

db_handler         = Threading_DB_Connection(dbconfig)
dao_t_users        = DAO_T_Users(db_handler)
dao_t_recipes      = DAO_T_Recipes(db_handler)

def home(request):
    # retrieving all the books from the database
    dto_recipes = dao_t_recipes.select_all()#[{"id": 1,"title":"idjodd", "image": {"url": "ijdojodoi"}}]#Book.objects.all()

    recipes_list = list()

    for dto_recipe in dto_recipes:
        recipe_dict = dict()

        recipe_dict["id"] = dto_recipe.id
        recipe_dict["name"] = dto_recipe.name
        recipe_dict["description"] = dto_recipe.description
        recipe_dict["image"] = dto_recipe.image
        recipe_dict["ingredients"] = dto_recipe.ingredients
        recipe_dict["steps"] = dto_recipe.steps
        recipe_dict["price"] = dto_recipe.price
        recipe_dict["location"] = dto_recipe.location
        recipe_dict["place_name"] = dto_recipe.place_name

        recipes_list.append(recipe_dict)

    context = {'recipes': recipes_list}
    return render(request, 'api/home.html', context)


# this is a view for listing a single book
def recipe_detail(request, id):
    # querying a particular book by its id
    dto_recipe = dao_t_recipes.select_by_id(int(id))

    recipe_dict = dict()

    recipe_dict["id"] = dto_recipe.id
    recipe_dict["name"] = dto_recipe.name
    recipe_dict["description"] = dto_recipe.description
    recipe_dict["image"] = dto_recipe.image
    recipe_dict["ingredients"] = dto_recipe.ingredients
    recipe_dict["steps"] = dto_recipe.steps
    recipe_dict["price"] = dto_recipe.price
    recipe_dict["location"] = dto_recipe.location
    recipe_dict["place_name"] = dto_recipe.place_name

    context = {'recipe': recipe_dict}

    return render(request, 'api/recipe-detail.html', context)

# this is a view for adding a book
def add_recipe(request):
    # checking if the method is POST
    if request.method == 'POST':
        # getting all the data from the POST request
        data = request.POST
        # getting the image
        name = data.get("name", "").strip()
        description = data.get("description", "").strip()
        image = data.get("image", "").strip()
        ingredients = data.get("ingredients", "")
        steps = data.get("steps", "")
        price = data.get("price", "")
        location = data.get("location", "")
        place_name = data.get("place_name", "")

        # dto_user = self.dao_t_users.select_by_email(email)

        # if not dto_user:
        #     response["status"] = "USER NOT FOUND"
        #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # if token != dto_user.token:
        #     response["status"] = "WRONG TOKEN"
        #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

        info = {
            "ingredients": ingredients,
            "steps": steps
        }
        # creating and saving the book
        dao_t_recipes.insert_new(
           name = name,
           description = description,
           image = image,
           info = info,
           price = price,
           location = location,
           place_name = place_name
        )
        # going to the home page
        return redirect('home')
    return render(request, 'api/add-recipe.html')


# this is a view for editing the book's info
def edit_recipe(request, id):
    # getting the book to be updated
    dto_recipe = dao_t_recipes.select_by_id(int(id))
    # populating the form with the book's information
    # form = EditBookForm(instance=book)
    # checking if the request is POST
    if request.method == 'POST':
        # filling the form with all the request data
        # form = EditBookForm(request.POST, request.FILES, instance=book)
        data = request.POST

        name = data.get("name", dto_recipe.name).strip()
        description = data.get("description", dto_recipe.description).strip()
        image = data.get("image", dto_recipe.image).strip()
        ingredients = data.get("ingredients", dto_recipe.ingredients)
        steps = data.get("steps", dto_recipe.steps)
        price = data.get("price", dto_recipe.price)
        location = data.get("location", dto_recipe.location)
        place_name = data.get("place_name", dto_recipe.place_name)

        if name == "":
            name = dto_recipe.name
        if description == "":
            description = dto_recipe.description
        if image == "":
            image = dto_recipe.image
        if len(ingredients) == 0:
            ingredients = dto_recipe.ingredients
        if len(steps) == 0:
            steps = dto_recipe.steps
        if price == "":
            price = dto_recipe.price
        if location == "":
            location = dto_recipe.location
        if place_name == "":
            place_name = dto_recipe.place_name

        info = {
            "ingredients": ingredients,
            "steps": steps
        }

        dao_t_recipes.update_by_id(dto_recipe.id, name, description, image, info, price, location, place_name)

        return redirect('home')
    return render(request, 'api/update-recipe.html')



# this is a view for deleting a book
def delete_recipe(request, id):
    # getting the book to be deleted
    dto_recipe = dao_t_recipes.select_by_id(int(id))

    recipe_dict = dict()

    recipe_dict["id"] = dto_recipe.id
    recipe_dict["name"] = dto_recipe.name
    recipe_dict["description"] = dto_recipe.description
    recipe_dict["image"] = dto_recipe.image
    recipe_dict["ingredients"] = dto_recipe.ingredients
    recipe_dict["steps"] = dto_recipe.steps
    recipe_dict["price"] = dto_recipe.price
    recipe_dict["location"] = dto_recipe.location
    recipe_dict["place_name"] = dto_recipe.place_name
    # checking if the method is POST
    if request.method == 'POST':
        # delete the book
        # recipe.delete()
        dao_t_recipes.delete_by_id(int(id))
        # return to home after a success delete
        return redirect('home')
    context = {'recipe': recipe_dict}
    return render(request, 'api/delete-recipe.html', context)