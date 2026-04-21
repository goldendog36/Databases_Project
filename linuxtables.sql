CREATE DATABASE IF NOT EXISTS SP500_Analysis;
USE SP500_Analysis;

DROP TABLE IF EXISTS Equities;
DROP TABLE IF EXISTS Trading_Signals;
DROP TABLE IF EXISTS Moving_Averages;
DROP TABLE IF EXISTS Oscillators;
DROP TABLE IF EXISTS Daily_Prices;

\! echo "Creating tables...";

CREATE TABLE IF NOT EXISTS Equities (
    ticker VARCHAR(10) NOT NULL PRIMARY KEY,
    company_name VARCHAR(255),
    sector VARCHAR(100),
    sub_industry VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Daily_Prices (
    ticker VARCHAR(10) NOT NULL,
    price_id INT PRIMARY KEY AUTO_INCREMENT,
    trade_date DATE NOT NULL,
    open_price DECIMAL(10,2),
    high_price DECIMAL(10,2),
    low_price DECIMAL(10,2),
    close_price DECIMAL(10,2),
    adjusted_close_price DECIMAL(10,2),
    volume BIGINT
);

\! echo "Tables created successfully. Loading company data...";

LOAD DATA INFILE '/var/lib/mysql-files/sp500-companies.csv'
INTO TABLE Equities
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
IGNORE 1 ROWS
(ticker, company_name, sector, sub_industry, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy);

\! echo "Loading stock data...";

LOAD DATA INFILE '/var/lib/mysql-files/SP500_Historical_Data.csv'
INTO TABLE Daily_Prices
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
IGNORE 1 ROWS
(ticker, trade_date, open_price, high_price, low_price, close_price, adjusted_close_price, volume);

CREATE TABLE IF NOT EXISTS Oscillators (
    price_id INT PRIMARY KEY AUTO_INCREMENT,
    ticker VARCHAR(10) NOT NULL,
    trade_date DATE NOT NULL,
    rsi_14_day DECIMAL(5,2),
    FOREIGN KEY (price_id) REFERENCES Daily_Prices(price_id)
);

LOAD DATA INFILE '/var/lib/mysql-files/SP500_Historical_Data.csv'
INTO TABLE Oscillators
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
IGNORE 1 ROWS
(ticker, trade_date, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy);

\! echo "Data loaded successfully. Calculating moving averages...";

CREATE TABLE Moving_Averages (
    price_id INT PRIMARY KEY AUTO_INCREMENT,
    ma_50_day DECIMAL(10,2),
    ma_200_day DECIMAL(10,2),
    FOREIGN KEY (price_id) REFERENCES Daily_Prices(price_id)
);

-- Calculate Moving Averages
UPDATE Moving_Averages t
JOIN (
    SELECT
        price_id,
        AVG(close_price) OVER (
            PARTITION BY ticker
            ORDER BY trade_date
            ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
        ) AS ma_50_day,
        AVG(close_price) OVER (
            PARTITION BY ticker
            ORDER BY trade_date
            ROWS BETWEEN 199 PRECEDING AND CURRENT ROW
        ) AS ma_200_day
    FROM Daily_Prices
) x ON t.price_id = x.price_id
SET t.ma_50_day = x.ma_50_day,
    t.ma_200_day = x.ma_200_day;

\! echo "Moving averages calculated. Calculating RSI...";

-- Calculate 14-day RSI
WITH price_changes AS (
    SELECT
        ticker,
        trade_date,
        close_price,
        close_price - LAG(close_price) OVER (PARTITION BY ticker ORDER BY trade_date) AS change_val
    FROM Daily_Prices
),
gains_losses AS (
    SELECT
        ticker,
        trade_date,
        CASE WHEN change_val > 0 THEN change_val ELSE 0 END AS gain,
        CASE WHEN change_val < 0 THEN -change_val ELSE 0 END AS loss
    FROM price_changes
),
rsi_calc AS (
    SELECT
        ticker,
        trade_date,
        SUM(gain) OVER (
            PARTITION BY ticker
            ORDER BY trade_date
            ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
        ) AS avg_gain,
        SUM(loss) OVER (
            PARTITION BY ticker
            ORDER BY trade_date
            ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
        ) AS avg_loss
    FROM gains_losses
)
UPDATE Oscillators t
JOIN rsi_calc r
  ON t.ticker = r.ticker
 AND t.trade_date = r.trade_date
SET t.rsi_14_day = 100 - (100 / (1 + (r.avg_gain / NULLIF(r.avg_loss, 0))));

\! echo "RSI calculated. Generating trading signals...";

CREATE TABLE IF NOT EXISTS Trading_Signals (
    signal_id INT PRIMARY KEY AUTO_INCREMENT,
    price_id INT,
    signal_type VARCHAR(50),
    indicator_used VARCHAR(50),
    FOREIGN KEY (price_id) REFERENCES Daily_Prices(price_id)
);

-- Generate trading signals based on moving average crossover
INSERT INTO Trading_Signals (price_id, signal_type, indicator_used)
SELECT 
    m.price_id,
    CASE
        WHEN m.ma_50_day > m.ma_200_day * 1.01 THEN 'BUY'
        WHEN m.ma_50_day < m.ma_200_day * 0.99 THEN 'SELL'
        ELSE 'HOLD'
    END AS signal_type,
    'MA_50'
FROM Moving_Averages m;

CREATE INDEX idx_signals_lookup ON Trading_Signals (price_id, signal_type);
CREATE INDEX idx_rsi_lookup ON Oscillators (rsi_14_day);
CREATE INDEX idx_ticker_date ON Daily_Prices (ticker, trade_date);
CREATE INDEX idx_equities_sector ON Equities (sector);

\! echo "Done.";
