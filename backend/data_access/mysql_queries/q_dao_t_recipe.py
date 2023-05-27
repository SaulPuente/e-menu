#-------------------------------------------------------------------------------
dictionary_t_recipes = {}
#-------------------------------------------------------------------------------
dictionary_t_recipes['select_all']      = "SELECT recipe_id, recipe_name, recipe_description, recipe_image, recipe_info FROM recipes;"
dictionary_t_recipes['select_by_id']    = "SELECT recipe_id, recipe_name, recipe_description, recipe_image, recipe_info FROM recipes WHERE recipe_id=%d limit 1;"
dictionary_t_recipes['insert_new']      = "INSERT INTO recipes (recipe_name, recipe_description, recipe_image, recipe_info) VALUES ('%s', '%s', '%s', '%s');"
dictionary_t_recipes['update_by_id']    = "UPDATE recipes SET recipe_name = '%s', recipe_description = '%s', recipe_image = '%s', recipe_info = '%s' WHERE recipe_id = %d;"
dictionary_t_recipes['delete_by_id']    = "DELETE FROM recipes WHERE recipe_id = %d;"