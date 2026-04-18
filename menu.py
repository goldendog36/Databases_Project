from actions import option_1, option_2, option_3, option_4, option_5, option_6, option_7, option_8

MENU = {
    "1": ("Option 1 description", option_1),
    "2": ("Option 2 description", option_2),
    "3": ("Option 3 description", option_3),
    "4": ("Option 4 description", option_4),
    "5": ("See the 10 highest volume trading days for a specific sector to examine possible macroeconomic events", option_5),
    "6": ("List the sectors that generated the most buy signals during a specific market period", option_6),
    "7": ("Find 'falling knives': stocks with an oversold RSI that did not generate a buy signal in the subsequent 30 days", option_7),
    "8": ("Check how often different indicators are firing", option_8),
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
