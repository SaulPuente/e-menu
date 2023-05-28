#-------------------------------------------------------------------------------
dictionary_t_recipes = {}
#-------------------------------------------------------------------------------
dictionary_t_recipes['select_all']      = "SELECT recipe_id, recipe_name, recipe_description, recipe_image, recipe_info, recipe_price, recipe_location, recipe_place_name FROM recipes;"
dictionary_t_recipes['select_by_id']    = "SELECT recipe_id, recipe_name, recipe_description, recipe_image, recipe_info, recipe_price, recipe_location, recipe_place_name FROM recipes WHERE recipe_id=%d limit 1;"
dictionary_t_recipes['insert_new']      = "INSERT INTO recipes (recipe_name, recipe_description, recipe_image, recipe_info, recipe_price, recipe_location, recipe_place_name) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');"
dictionary_t_recipes['update_by_id']    = "UPDATE recipes SET recipe_name = '%s', recipe_description = '%s', recipe_image = '%s', recipe_info = '%s', recipe_price = '%s', recipe_location = '%s', recipe_place_name = '%s' WHERE recipe_id = %d;"
dictionary_t_recipes['delete_by_id']    = "DELETE FROM recipes WHERE recipe_id = %d;"