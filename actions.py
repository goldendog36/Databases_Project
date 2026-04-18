from db import execute_query

def option_1(cursor):
    print("Yay!")
    # params = prompt user if needed for SQL parameters
    # rows = execute_query(cursor, SQL goes here, params go here)
    # for r in rows:
    #     print(r)

def option_2(cursor):
    print("Yay!")

def option_3(cursor):
    print("Yay!")

def option_4(cursor):
    print("Yay!")

def option_5(cursor):
    sectors = get_sectors(cursor)
    
    print("------ Sectors ------")
    for index, sector in enumerate(sectors, start=1):
        print(f"({index}) : {sector}")

    while True:
        try:
            choice = int(input("Please enter the number of the desired sector: ").strip())
            if 1 <= choice <= len(sectors):
                break
            else:
                print("Invalid sector.")
        except ValueError:
            print("Invalid number input.")

    sector_choice = sectors[choice-1]

    sql = """
    SELECT e.company_name, dp.ticker, dp.date, dp.volume, dp.close_price
    FROM Daily_Prices dp
    JOIN Equities e ON dp.ticker = e.ticker
    WHERE e.sector = %s
    ORDER BY dp.volume DESC
    LIMIT 10
    """
    
    results = execute_query(cursor, sql, (sector_choice,))

    print(f"10 Highest Trading Volume Days in {sector_choice}")
    for index, day in enumerate(results, start=1):
        company, ticker, date, volume, price = day
        print(f"{index}. {company} ({ticker}) | {date} | Vol: {volume} | Close: {price}")

def get_sectors(cursor):
    sql = """
    SELECT DISTINCT e.sector
    FROM Equities e
    """
    rows = execute_query(cursor, sql)
    return [r[0] for r in rows]

def option_6(cursor):
    print("Yay!")

def option_7(cursor):
    print("Yay!")

def option_8(cursor):
    print("Yay!")