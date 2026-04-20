from db import execute_query
from datetime import datetime

# GUIDELINES:
# params = prompt user if needed for SQL parameters
# rows = execute_query(cursor, SQL goes here, params go here)
# for r in rows:
#     print(r)

def option_1(cursor):
    stock = input("\nWhat stock would you like to see a log of? ").strip().upper()

    query = """
            SELECT dp.trade_date, ts.signal_type, ts.indicator_used, dp.close_price
            FROM Trading_Signals ts
            JOIN Daily_Prices dp ON ts.price_id = dp.price_id
            WHERE dp.ticker = %s
            ORDER BY dp.trade_date DESC
            LIMIT 50;
            """
    results = execute_query(cursor, query, (stock,))
    if results:
        print(f"{stock} has a log of: ")
        header = f"{'DATE':<25} | {'SIGNAL TYPE':<10} | {'INDICATOR':>10} | {'CLOSE':>10}"
        print(header)
        print("-" * len(header))
        for row in results:
            date = str(row[0])
            signal_type = row[1]
            indicator = row[2]
            close_price = row[3]

            print(f"{date:<25} | {signal_type:<10} | {indicator:>10} | {close_price:>10.2f}")
    else:
        print(f"No log of {stock}")

def option_2(cursor):
    year = input("\nWhat year would you like to look at? ").strip()

    # depends on date format
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    query = """
            SELECT e.ticker, e.company_name, MAX(o.rsi_14_day) as peak_rsi, MIN(o.rsi_14_day) as lowest_rsi
            FROM Equities e
            JOIN Daily_Prices dp ON e.ticker = dp.ticker
            JOIN Oscillators o ON dp.price_id = o.price_id
            WHERE dp.trade_date BETWEEN %s AND %s
            GROUP BY e.ticker, e.company_name
            ORDER BY lowest_rsi ASC
            LIMIT 20;
    """

    results = execute_query(cursor, query, (start_date, end_date,))
    if results:
        print(f"{start_date} to {end_date} has a log of: ")
        header = f"{'TICKER':<8} | {'COMPANY NAME':<25} | {'PEAK RSI':>10} | {'LOWEST RSI':>10}"
        print(header)
        print("-" * len(header))
        for row in results:
            ticker = row[0]
            name = row[1]
            peak_rsi = row[2]
            lowest_rsi = row[3]

            print(f"{ticker:<8} | {name:<25} | {peak_rsi:>10.2f} | {lowest_rsi:>10.2f}")
    else:
        print(f"No log for {year}")


def option_3(cursor):
    stock = input("\nWhat stock would you like to check out? ").strip().upper()
    year = input("What year would you like to look at? ").strip()

    start = f"{year}-01-01"
    end = f"{year}-12-31"

    # Step 1: Calculate the average volume once
    avg_volume_query = """
        SELECT AVG(volume) 
        FROM Daily_Prices 
        WHERE ticker = %s AND trade_date BETWEEN %s AND %s
    """
    avg_result = execute_query(cursor, avg_volume_query, (stock, start, end))

    if not avg_result or avg_result[0][0] is None:
        print(f"No volume data found for {stock} in {year}.")
        return

    avg_vol = avg_result[0][0]

    # Step 2: Run the main query using that average
    # Note: Using 'BUY' in all caps to match your SQL setup
    query = """
            SELECT dp.ticker, dp.trade_date, ts.indicator_used, dp.volume, dp.close_price
            FROM Daily_Prices dp
            JOIN Trading_Signals ts ON dp.price_id = ts.price_id
            WHERE ts.signal_type = 'BUY'
            AND dp.ticker = %s
            AND dp.trade_date BETWEEN %s AND %s
            AND dp.volume > %s
            ORDER BY dp.trade_date DESC;
    """

    results = execute_query(cursor, query, (stock, start, end, avg_vol))

    if results:
        print(f"\n{stock} high-volume buy signals in {year} (Avg Vol: {avg_vol:,.0f}):")
        header = f"{'TICKER':<8} | {'DATE':<25} | {'INDICATOR':>10} | {'VOLUME':>12} | {'CLOSE':>10}"
        print(header)
        print("-" * len(header))
        for row in results:
            ticker, date, indicator, volume, price = row
            print(f"{ticker:<8} | {str(date):<25} | {indicator:>10} | {volume:>12,} | {price:>10.2f}")
    else:
        print(f"No high volume buy signals found for {stock} in {year}.")

def option_4(cursor):
    ticker = input("\nWhat stock would you like to see? ").strip().upper()
    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter end date (YYYY-MM-DD): ").strip()

    query = """
                SELECT dp.trade_date, dp.close_price, dp.volume, ma.ma_50_day, ma.ma_200_day, o.rsi_14_day
                FROM Daily_Prices dp
                JOIN Moving_Averages ma ON dp.price_id = ma.price_id
                JOIN Oscillators o ON dp.price_id = o.price_id
                WHERE dp.ticker = %s
                AND dp.trade_date BETWEEN %s AND %s
                ORDER BY dp.trade_date ASC;
                """

    results = execute_query(cursor, query, (ticker, start_date, end_date))

    if results:
        print(f"\nPrice Action and Indicators for {ticker} from {start_date} to {end_date}:")
        header = f"{'DATE':<12} | {'CLOSE':>10} | {'VOLUME':>12} | {'MA 50':>10} | {'MA 200':>10} | {'RSI':>8}"
        print(header)
        print("-" * len(header))

        for row in results:
            date, close, vol, ma50, ma200, rsi = row
            print(f"{str(date):<12} | {close:>10.2f} | {vol:>12,} | {ma50:>10.2f} | {ma200:>10.2f} | {rsi:>8.2f}")
    else:
        print(f"No data found for {ticker} in that date range.")

def option_5(cursor):
    sectors = get_sectors(cursor)
    
    print("------ Sectors ------")
    for index, sector in enumerate(sectors, start=1):
        print(f"({index}) : {sector}")
    print("\n")

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
    SELECT e.company_name, dp.ticker, dp.trade_date, dp.volume, dp.close_price
    FROM Daily_Prices dp
    JOIN Equities e ON dp.ticker = e.ticker
    WHERE e.sector = %s
    ORDER BY dp.volume DESC
    LIMIT 10
    """
    
    results = execute_query(cursor, sql, (sector_choice,))

    print(f"\n10 Highest Trading Volume Days in {sector_choice}")
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
    WHERE ts.signal_type = 'BUY'
    AND dp.trade_date >= %s
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
        SELECT dp.ticker, dp.trade_date as oversold_date, o.rsi_14_day, dp.close_price
        FROM Daily_Prices dp
        JOIN Oscillators o ON dp.price_id = o.price_id
        WHERE o.rsi_14_day < 25
        AND NOT EXISTS (
            SELECT 1
            FROM Daily_Prices dp_future
            JOIN Trading_Signals ts ON dp_future.price_id = ts.price_id
            WHERE dp_future.ticker = dp.ticker
            AND ts.signal_type = 'BUY'
            AND dp_future.trade_date > dp.trade_date
            AND dp_future.trade_date <= DATE_ADD(dp.trade_date, INTERVAL 30 DAY)
        )
        ORDER BY dp.trade_date DESC
        LIMIT 100;
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
