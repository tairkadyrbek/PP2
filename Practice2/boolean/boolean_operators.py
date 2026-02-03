#1 Logical Operators
battery = 10
charger_connected = False
print(battery > 20 and charger_connected)    # False

#2
is_admin = False
is_owner = False
print(is_admin or is_owner)   # True

#3
game_over = False
print(not game_over)    # True

#4
age = 19
has_id = True
print(age >= 18 and (has_id or age >= 21))    # True

#5
username_correct = True
password_correct = True
print(username_correct and password_correct)  # True