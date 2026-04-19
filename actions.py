from db import execute_query

# GUIDELINES:
# params = prompt user if needed for SQL parameters
# rows = execute_query(cursor, SQL goes here, params go here)
# for r in rows:
#     print(r)

def option_1(cursor):
    stock = input("What stock would you like to see a log of?").strip()

    query = """
            SELECT dp.date, ts.signal_type, ts.indicator_used, dp.close_price
            FROM Trading_Signals ts
            JOIN Daily_Prices dp ON ts.price_id = dp.price_id
            WHERE dp.ticker = %s
            ORDER BY dp.date DESC
            LIMIT 50;
            """
    results = execute_query(cursor, query, (stock,))
    if results:
        print(f"{stock} has a log of: ")
        print(f"{'DATE':<25} | {'SIGNAL TYPE':<10} | {'INDICATOR':>10} | {'CLOSE':>10}")
        print("-"*62)
        for row in results:
            date = row[0]
            signal_type = row[1]
            indicator = row[2]
            close_price = row[3]

            print(f"{date:<25} | {signal_type:<10} | {indicator:>10} | {close_price:>10.2f}")
    else:
        print(f"No log of {stock}")

def option_2(cursor):
    year = input("What year would you like to look at?").strip()

    # depends on date format
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    query = """
            SELECT e.ticker, e.company_name, MAX(o.rsi_14_day) as peak_rsi, MIN(o.rsi_14_day) as lowest_rsi
            FROM Equities e
            JOIN Daily_Prices dp ON e.ticker = dp.ticker
            JOIN Oscillators o ON dp.price_id = o.price_id
            WHERE dp.date BETWEEN %s AND %s
            GROUP BY e.ticker, e.company_name
            ORDER BY lowest_rsi ASC
            LIMIT 20;
    """

    results = execute_query(cursor, query, (start_date, end_date,))
    if results:
        print(f"{start_date} to {end_date} has a log of: \n")
        print(f"{'TICKER':<8} | {'COMPANY NAME':<25} | {'PEAK RSI':>10} | {'LOWEST RSI':>10}")
        print("-" * 62)
        for row in results:
            ticker = row[0]
            name = row[1]
            peak_rsi = row[2]
            lowest_rsi = row[3]

            print(f"{ticker:<8} | {name:<25} | {peak_rsi:>10.2f} | {lowest_rsi:>10.2f}")
    else:
        print(f"No log for {year}")


def option_3(cursor):
    print("Yay!")

def option_4(cursor):
    print("Yay!")

def option_5(cursor):
    print("Yay!")

def option_6(cursor):
    print("Yay!")

def option_7(cursor):
    print("Yay!")

def option_8(cursor):
    print("Yay!")