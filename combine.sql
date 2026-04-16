CREATE DATABASE IF NOT EXISTS SP500_Analysis;
USE SP500_Analysis;

DROP TABLE IF EXISTS SP500_Master;

CREATE TABLE IF NOT EXISTS SP500_Master (
    -- Company info
    ticker VARCHAR(10) NOT NULL,
    company_name VARCHAR(255),
    sector VARCHAR(100),
    sub_industry VARCHAR(100),

    -- Price data
    price_id INT PRIMARY KEY AUTO_INCREMENT,
    trade_date DATE NOT NULL,
    open_price DECIMAL(10,2),
    high_price DECIMAL(10,2),
    low_price DECIMAL(10,2),
    close_price DECIMAL(10,2),
    adjusted_close_price DECIMAL(10,2),
    volume BIGINT,

    -- Moving averages
    ma_50_day DECIMAL(10,2),
    ma_200_day DECIMAL(10,2),

    -- Oscillators
    rsi_14_day DECIMAL(5,2),

    -- Trading signals
    signal_id INT,
    signal_type VARCHAR(50),
    indicator_used VARCHAR(50)
);

LOAD DATA INFILE '/var/lib/mysql-files/sp500-companies.csv'
INTO TABLE SP500_Master
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
IGNORE 1 ROWS
(ticker, company_name, sector, sub_industry, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy);

LOAD DATA INFILE '/var/lib/mysql-files/SP500_Historical_Data.csv'
INTO TABLE SP500_Master
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
IGNORE 1 ROWS
(ticker, trade_date, open_price, high_price, low_price, close_price, adjusted_close_price, volume);

-- Calculate 50-day moving average
UPDATE SP500_Master t
JOIN (
    SELECT 
        price_id,
        AVG(close_price) OVER (
            PARTITION BY ticker
            ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
        ) AS ma_50_day
    FROM SP500_Master
) x ON t.price_id = x.price_id
SET t.ma_50_day = x.ma_50_day;

-- Calculate 200-day moving average
UPDATE SP500_Master t
JOIN (
    SELECT 
        price_id,
        AVG(close_price) OVER (
            PARTITION BY ticker
            ROWS BETWEEN 199 PRECEDING AND CURRENT ROW
        ) AS ma_200_day
    FROM SP500_Master
) x ON t.price_id = x.price_id
SET t.ma_200_day = x.ma_200_day;

-- Calculate 14-day RSI
UPDATE SP500_Master t
SET rsi_14_day = (
    SELECT 100 - (100 / (1 + (SUM(CASE WHEN close_price > LAG(close_price) OVER (PARTITION BY ticker ORDER BY trade_date) THEN close_price - LAG(close_price) OVER (PARTITION BY ticker ORDER BY trade_date) ELSE 0 END) / NULLIF(SUM(CASE WHEN close_price < LAG(close_price) OVER (PARTITION BY ticker ORDER BY trade_date) THEN LAG(close_price) OVER (PARTITION BY ticker ORDER BY trade_date) - close_price ELSE 0 END), 0))))
    FROM SP500_Master t2
    WHERE t2.ticker = t.ticker
      AND t2.trade_date BETWEEN DATE_SUB(t.trade_date, INTERVAL 13 DAY) AND t.trade_date
);

-- Generate trading signals based on moving average crossover
UPDATE SP500_Master
SET signal_type = 'BUY',
    indicator_used = 'MA_50'
WHERE ma_50_day > ma_200_day;

-- Export the combined data to a CSV file
SELECT * FROM SP500_Master
INTO OUTFILE '/var/lib/mysql-files/output.csv'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

