from actions import option_1, option_2, option_3, option_4, option_5, option_6, option_7, option_8

MENU = {
    "1": ("Option 1 description", option_1),
    "2": ("Option 2 description", option_2),
    "3": ("Option 3 description", option_3),
    "4": ("Option 4 description", option_4),
    "5": ("Option 5 description", option_5),
    "6": ("Option 6 description", option_6),
    "7": ("Option 7 description", option_7),
    "8": ("Option 8 description", option_8),
    "9": ("Exit", None)
}

def print_menu():
    print("What would you like to do today?")
    for key, (label, _) in MENU.items():
        print(f"({key}) : {label}")

def handle_choice(choice, cursor):
    action = MENU.get(choice)

    if not action:
        print("Invalid choice.")
        return True
    
    label, func = action
    
    if label == "Exit":
        return False
    
    func(cursor)
    return True
