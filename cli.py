from db import connect
import sys

def main():
    conn = connect()
    cursor = conn.cursor()

    print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$ Welcome to ALGOTRADE $$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")

    print("AlgoTrade is your favorite price-based-indicator platform that tells you when to BUY or SELL")

    name = input("Please enter your name: ")

    print(f"\nHello {name}!")

    print("What would you like to do today?\n"
    "(1) See the closing price of a stock\n"
    "(2) MEDIUM BLAH\n"
    "(3) HARD BLAH\n")
    
    option = int(input("Please enter the number of your desired option: "))

    if option == 1:
        print("Yay!")
        # cursor.execute(SQL)
        # for row in cursor.fetchall():
        #   print(row)
    elif option == 2:
        print("Yippee!")
    elif option == 3:
        print("Hoorah!")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main();