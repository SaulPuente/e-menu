#-------------------------------------------------------------------------------
dictionary_t_user = {}
#-------------------------------------------------------------------------------
dictionary_t_user['select_all']         = "SELECT user_id, user_email, user_fname, user_lname, user_password, user_status, user_token FROM users;"
dictionary_t_user['select_by_id']       = "SELECT user_id, user_email, user_fname, user_lname, user_password, user_status, user_token FROM users WHERE user_id = %d;"
dictionary_t_user['select_by_email']    = "SELECT user_id, user_email, user_fname, user_lname, user_password, user_status, user_token FROM users WHERE user_email = '%s';"
dictionary_t_user['select_by_name']     = "SELECT user_id, user_email, user_fname, user_lname, user_password, user_status, user_token FROM users WHERE user_email like '%%%s%%' OR user_fname like '%%%s%%' OR user_lname like '%%%s%%';"

dictionary_t_user['update_user_status'] = "UPDATE users SET user_status ='%s' WHERE user_id = %d;"

dictionary_t_user['insert_new_user']    = "INSERT INTO users (user_email, user_fname, user_lname, user_password, user_status, user_token) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');"

dictionary_t_user['select_pass']        = "SELECT user_password FROM users WHERE user_id = %d;"
dictionary_t_user['update_pass']        = "UPDATE users SET user_password = '%s' WHERE user_id = %d ;"

dictionary_t_user['select_token']       = "SELECT user_token FROM users WHERE user_id = %d;"
dictionary_t_user['update_token']       = "UPDATE users SET user_token = '%s' WHERE user_id = %d ;"