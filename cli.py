from db import connect
from menu import print_menu, handle_choice
import sys

def main():
    conn = connect()
    cursor = conn.cursor()

    print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$ Welcome to ALGOTRADE $$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n")
    print("AlgoTrade is your favorite price-based-indicator platform that tells you when to BUY, SELL, or HOLD")

    try:
        running = True
        while running:
            print_menu()
            choice = input("Please enter the number of your desired option: ").strip()
            running = handle_choice(choice, cursor)
    finally:
        cursor.close()
        conn.close()
        print("\nThank you for using AlgoTrade!")
        sys.exit(0)

if __name__ == "__main__":
    main();