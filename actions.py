from db import execute_query
from datetime import datetime

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
    for index, row in enumerate(results, start=1):
        company, ticker, date, volume, price = row
        print(f"{index}. {company} ({ticker}) | {date} | Vol: {volume} | Close: {price}")

def get_sectors(cursor):
    sql = """
    SELECT DISTINCT e.sector
    FROM Equities e
    """
    rows = execute_query(cursor, sql)
    return [r[0] for r in rows]

def option_6(cursor):
    while True:
        date_input = input("Please enter the start date of your market period "
        "in YYYY-MM-DD format: ").strip()
        try:
            valid_date = datetime.strptime(date_input, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date.")
       
    sql = """
    SELECT e.sector, COUNT(ts.signal_id) as total_buy_signals
    FROM Equities e
    JOIN Daily_Prices dp ON e.ticker = dp.ticker
    JOIN Trading_Signals ts ON dp.price_id = ts.price_id
    WHERE ts.signal_type = 'Buy'
    AND dp.date >= %s
    GROUP BY e.sector
    ORDER BY total_buy_signals DESC
    LIMIT 10;
    """
    # HAVING COUNT(ts.signal_id) > 50 --> now query returns top 10, not all over 50

    results = execute_query(cursor, sql, (valid_date,))

    print(f"Sectors with the highest number of generated buy signals since {valid_date}")
    if not results:
        print ("No results found for that date.")
    else:
        for index, row in enumerate(results, start=1):
            sector, buy_signal_count = row
            print(f"{index}. {sector} : {buy_signal_count}")


def option_7(cursor):
    sql = """
    SELECT dp.ticker, dp.date as oversold_date, o.rsi_14_day, dp.close_price
    FROM Daily_Prices dp
    JOIN Oscillators o ON dp.price_id = o.price_id
    WHERE o.rsi_14_day < 25
    AND NOT EXISTS (
        SELECT 1
        FROM Daily_Prices dp_future
        JOIN Trading_Signals ts ON dp_future.price_id = ts.price_id
        WHERE dp_future.ticker = dp.ticker
        AND ts.signal_type = 'Buy'
        AND dp_future.date > dp.date
        AND dp_future.date <= DATE_ADD(dp.date, INTERVAL 30 DAY)
    )
    ORDER BY dp.date DESC;
    """

    results = execute_query(cursor, sql)

    print("--- Falling Knives ---")
    if not results:
        print("No results found.")
    else:
        for index, row in enumerate(results, start=1):
            ticker, oversold_date, rsi, price = row
            print(f"{index}. {ticker} | {oversold_date} | RSI: {rsi} | Price: {price}")

def option_8(cursor):
    sql = """
    SELECT indicator_used, signal_type, COUNT(signal_id) as total_occurrences
    FROM Trading_Signals
    GROUP BY indicator_used, signal_type
    ORDER BY total_occurrences DESC;
    """

    results = execute_query(cursor, sql)

    print("--- Cumulative Indicator Totals ---")
    for index, row in enumerate(results, start=1):
        indicator, signal, total_occurrences = row
        print(f"{index}. Indicator: {indicator} | Signal: {signal} | Count: {total_occurrences}")
