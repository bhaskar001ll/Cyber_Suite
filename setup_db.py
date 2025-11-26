from login import create_user_table, register_user

create_user_table()
register_user("admin", "admin123")
print("Default user created: admin / admin123")