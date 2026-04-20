from actions import option_1, option_2, option_3, option_4, option_5, option_6, option_7, option_8

MENU = {
    "1": ("See a chronological log of all automated trading actions generated for a stock.", option_1),
    "2": ("Group stocks by ticker and calculate their maximum and minimum RSI values over a specific year to find the most volatile assets.", option_2),
    "3": ("Find days where a BUY signal triggered, but only if the trading volume on that specific day was strictly greater than that exact stock's average daily volume for a specific year.", option_3),
    "4": ("See all price action and calculated indicators for a stock in a defined date range", option_4),
    "5": ("See the 10 highest volume trading days for a specific sector to examine possible macroeconomic events", option_5),
    "6": ("List the sectors that generated the most BUY signals after a specified date", option_6),
    "7": ("Find 'falling knives': stocks with an oversold RSI that did not generate a BUY signal in the subsequent 30 days", option_7),
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
