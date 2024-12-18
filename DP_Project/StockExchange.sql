create DATABASE DB_StockExchange
use DB_StockExchange
go

CREATE TABLE Users (
    UserId INT PRIMARY KEY IDENTITY(1,1),
    Username NVARCHAR(50) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(255) NOT NULL,
    Email NVARCHAR(100) NOT NULL UNIQUE,
    CreatedAt DATETIME DEFAULT GETDATE()
);


CREATE TABLE Stocks (
    StockId INT PRIMARY KEY IDENTITY(1,1),
    StockName NVARCHAR(100) NOT NULL,
    StockSymbol NVARCHAR(10) NOT NULL UNIQUE,
    CurrentPrice DECIMAL(10, 2) NOT NULL,
    LastUpdated DATETIME DEFAULT GETDATE()
);


CREATE TABLE Transactions (
    TransactionId INT PRIMARY KEY IDENTITY(1,1),
    UserId INT NOT NULL,
    StockId INT NOT NULL,
    TransactionType NVARCHAR(10) CHECK (TransactionType IN ('BUY', 'SELL')),
    Quantity INT NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    TransactionDate DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (UserId) REFERENCES Users(UserId),
    FOREIGN KEY (StockId) REFERENCES Stocks(StockId)
);


CREATE TABLE Portfolios (
    PortfolioId INT PRIMARY KEY IDENTITY(1,1),
    UserId INT NOT NULL,
    StockId INT NOT NULL,
    Quantity INT NOT NULL,
    FOREIGN KEY (UserId) REFERENCES Users(UserId),
    FOREIGN KEY (StockId) REFERENCES Stocks(StockId),
    CONSTRAINT UniqueUserStock UNIQUE (UserId, StockId) -- Ensures a user can't have duplicate stock entries
);


CREATE TABLE MarketNews (
    NewsId INT PRIMARY KEY IDENTITY(1,1),
    Title NVARCHAR(255) NOT NULL,
    Content NVARCHAR(MAX) NOT NULL,
    PublishedAt DATETIME DEFAULT GETDATE()
);


INSERT INTO Stocks (StockName, StockSymbol, CurrentPrice, LastUpdated)
VALUES 
('Apple', 'AAPL', 150.00, GETDATE()),
('Microsoft', 'MSFT', 250.00, GETDATE()),
('Google', 'GOOGL', 2800.00, GETDATE()),
('Amazon', 'AMZN', 3300.00, GETDATE());
 SELECT * from Stocks
 SELECT * from Users



INSERT INTO Users (Username, PasswordHash, Email, CreatedAt)
VALUES ('admin1', 'admin', 'admin1@example.com', GETDATE()); 

SELECT * from Users


INSERT INTO Stocks (StockName, StockSymbol, CurrentPrice, LastUpdated)
VALUES
('Tesla Inc.', 'TSLA', 850.10, GETDATE()),
('Alphabet Inc.', 'AINC', 2805.67, GETDATE()),
('Meta Platforms Inc.', 'META', 190.23, GETDATE()),
('NVIDIA Corp.', 'NVDA', 245.12, GETDATE()),
('Adobe Inc.', 'ADBE', 530.45, GETDATE()),
('Netflix Inc.', 'NFLX', 410.32, GETDATE()),
('Intel Corp.', 'INTC', 55.10, GETDATE()),
('Cisco Systems Inc.', 'CSCO', 56.78, GETDATE()),
('Oracle Corp.', 'ORCL', 85.45, GETDATE()),
('Salesforce Inc.', 'CRM', 192.10, GETDATE()),
('Qualcomm Inc.', 'QCOM', 120.35, GETDATE()),
('Zoom Video Comm.', 'ZM', 108.42, GETDATE()),
('Shopify Inc.', 'SHOP', 50.76, GETDATE()),
('Square Inc.', 'SQ', 82.94, GETDATE()),
('PayPal Holdings Inc.', 'PYPL', 95.67, GETDATE()),
('eBay Inc.', 'EBAY', 49.98, GETDATE()),
('Twitter Inc.', 'TWTR', 35.65, GETDATE()),
('Snap Inc.', 'SNAP', 10.45, GETDATE()),
('Uber Technologies Inc.', 'UBER', 31.85, GETDATE()),
('Lyft Inc.', 'LYFT', 14.23, GETDATE()),
('Airbnb Inc.', 'ABNB', 123.40, GETDATE()),
('DoorDash Inc.', 'DASH', 78.90, GETDATE());
SELECT * from Stocks

INSERT INTO Transactions (UserId, StockId, TransactionType, Quantity, Price, TransactionDate)
VALUES
(1, 1, 'BUY', 10, 175.35, GETDATE()),
(1, 2, 'BUY', 15, 310.50, GETDATE()),
(1, 3, 'BUY', 5, 135.25, GETDATE()),
(1, 4, 'SELL', 2, 850.10, GETDATE()),
(1, 5, 'BUY', 8, 2805.67, GETDATE()),
(1, 6, 'BUY', 20, 190.23, GETDATE()),
(1, 7, 'SELL', 5, 245.12, GETDATE()),
(1, 8, 'BUY', 22, 530.45, GETDATE()),
(1, 9, 'BUY', 7, 410.32, GETDATE()),
(1, 10, 'SELL', 3, 55.10, GETDATE()),
(1, 11, 'BUY', 9, 56.78, GETDATE()),
(1, 12, 'BUY', 14, 85.45, GETDATE()),
(1, 13, 'SELL', 2, 192.10, GETDATE()),
(1, 14, 'BUY', 4, 120.35, GETDATE()),
(1, 15, 'BUY', 11, 108.42, GETDATE()),
(1, 16, 'SELL', 2, 50.76, GETDATE()),
(1, 17, 'BUY', 25, 82.94, GETDATE()),
(1, 18, 'BUY', 3, 95.67, GETDATE()),
(1, 19, 'SELL', 5, 49.98, GETDATE()),
(1, 20, 'BUY', 2, 35.65, GETDATE()),
(1, 21, 'BUY', 5, 10.45, GETDATE()),
(1, 22, 'SELL', 2, 31.85, GETDATE()),
(1, 23, 'BUY', 19, 14.23, GETDATE()),
(1, 24, 'BUY', 10, 123.40, GETDATE()),
(1, 25, 'SELL', 2, 78.90, GETDATE());





INSERT INTO MarketNews (Title, Content, PublishedAt)
VALUES
('Tech Stocks Surge', 'Tech companies see a strong rally amid positive earnings reports.', GETDATE()),
('Market Opens Higher', 'Wall Street opens higher as inflation fears ease.', GETDATE()),
('Oil Prices Drop', 'Oil prices fall below $80 per barrel amid recession fears.', GETDATE()),
('Tesla Hits New High', 'Tesla stock reaches a new all-time high after strong sales data.', GETDATE()),
('Meta Unveils New VR', 'Meta Platforms unveils its latest VR headset.', GETDATE()),
('NVIDIA Reports Earnings', 'NVIDIA reports record-breaking revenue for Q4.', GETDATE()),
('Zoom Declines', 'Zoom stock falls as demand for virtual meetings slows.', GETDATE()),
('Amazon Expands', 'Amazon announces plans to expand its logistics network.', GETDATE()),
('Apple Launches iPhone', 'Apple launches the latest iPhone model to great acclaim.', GETDATE()),
('Netflix Subscription Growth', 'Netflix sees subscription growth after launching an ad-supported tier.', GETDATE()),
('Chip Shortage Eases', 'Global chip shortage shows signs of improvement.', GETDATE()),
('Airbnb Demand Rises', 'Airbnb reports strong demand for vacation rentals.', GETDATE()),
('Uber Q2 Results', 'Uber reports better-than-expected Q2 results.', GETDATE()),
('Lyft Faces Competition', 'Lyft faces increasing competition from new ride-sharing apps.', GETDATE()),
('PayPal Upgrades', 'PayPal introduces new payment features for businesses.', GETDATE()),
('eBay Expands Categories', 'eBay expands into new product categories.', GETDATE()),
('Twitter Updates', 'Twitter introduces new subscription features.', GETDATE()),
('Snap Sees Growth', 'Snapchat sees user growth in emerging markets.', GETDATE()),
('Shopify Partners', 'Shopify announces new partnerships with major retailers.', GETDATE()),
('Square Rebrands', 'Square Inc. rebrands as Block to focus on blockchain.', GETDATE()),
('Adobe Acquires Figma', 'Adobe completes acquisition of design platform Figma.', GETDATE()),
('Oracle Cloud Growth', 'Oracle sees strong growth in cloud services.', GETDATE()),
('Cisco Reports Demand', 'Cisco reports increased demand for networking hardware.', GETDATE()),
('Intel New Chips', 'Intel launches its next-generation processors.', GETDATE()),
('Tesla Production', 'Tesla increases production capacity in new gigafactories.', GETDATE());


SELECT * from MarketNews
INSERT INTO Stocks (StockName, StockSymbol, CurrentPrice, LastUpdated)
VALUES
('Apple Inc.', 'AAPL', 175.35, GETDATE()),
('Microsoft Corp.', 'MSFT', 310.50, GETDATE()),
('Amazon.com Inc.', 'AMZN', 135.25, GETDATE()),
('Tesla Inc.', 'TSLA', 850.10, GETDATE()),
('Alphabet Inc.', 'GOOGL', 2805.67, GETDATE()),
('Meta Platforms Inc.', 'META', 190.23, GETDATE()),
('NVIDIA Corp.', 'NVDA', 245.12, GETDATE()),
('Adobe Inc.', 'ADBE', 530.45, GETDATE()),
('Netflix Inc.', 'NFLX', 410.32, GETDATE()),
('Intel Corp.', 'INTC', 55.10, GETDATE()),
('Cisco Systems Inc.', 'CSCO', 56.78, GETDATE()),
('Oracle Corp.', 'ORCL', 85.45, GETDATE()),
('Salesforce Inc.', 'CRM', 192.10, GETDATE()),
('Qualcomm Inc.', 'QCOM', 120.35, GETDATE()),
('Zoom Video Comm.', 'ZM', 108.42, GETDATE()),
('Shopify Inc.', 'SHOP', 50.76, GETDATE()),
('Square Inc.', 'SQ', 82.94, GETDATE()),
('PayPal Holdings Inc.', 'PYPL', 95.67, GETDATE()),
('eBay Inc.', 'EBAY', 49.98, GETDATE()),
('Twitter Inc.', 'TWTR', 35.65, GETDATE()),
('Snap Inc.', 'SNAP', 10.45, GETDATE()),
('Uber Technologies Inc.', 'UBER', 31.85, GETDATE()),
('Lyft Inc.', 'LYFT', 14.23, GETDATE()),
('Airbnb Inc.', 'ABNB', 123.40, GETDATE()),
('DoorDash Inc.', 'DASH', 78.90, GETDATE());
SELECT * from Stocks



INSERT INTO Portfolios (UserId, StockId, Quantity)
VALUES
(1, 29, 50),
(1, 30, 30),
(1, 31, 25),
(1, 32, 40),
(1, 33, 15),
(1, 34, 35),
(1, 35, 20),
(1, 36, 60),
(1, 37, 18),
(1, 38, 22),
(1, 39, 10),
(1, 40, 14),
(1, 41, 5),
(1, 42, 8),
(1, 43, 12),
(1, 44, 9),
(1, 45, 28),
(1, 46, 3),
(1, 47, 32),
(1, 48, 7),
(1, 49, 18),
(1, 50, 12),
(1, 51, 14),
(1, 52, 27),
(1, 53, 11);
SELECT * from Portfolios


INSERT INTO Transactions (UserId, StockId, TransactionType, Quantity, Price, TransactionDate)
VALUES
(1, 29, 'BUY', 50, 175.35, GETDATE()),
(1, 30, 'BUY', 30, 310.50, GETDATE()),
(1, 31, 'SELL', 10, 135.25, GETDATE()),
(1, 32, 'BUY', 40, 850.10, GETDATE()),
(1, 33, 'SELL', 5, 2805.67, GETDATE()),
(1, 34, 'BUY', 35, 190.23, GETDATE()),
(1, 35, 'SELL', 20, 245.12, GETDATE()),
(1, 36, 'BUY', 60, 530.45, GETDATE()),
(1, 37, 'BUY', 18, 410.32, GETDATE()),
(1, 38, 'SELL', 8, 55.10, GETDATE()),
(1, 39, 'BUY', 10, 56.78, GETDATE()),
(1, 40, 'BUY', 14, 85.45, GETDATE()),
(1, 41, 'SELL', 5, 192.10, GETDATE()),
(1, 42, 'BUY', 8, 120.35, GETDATE()),
(1, 43, 'SELL', 12, 108.42, GETDATE()),
(1, 44, 'BUY', 9, 50.76, GETDATE()),
(1, 45, 'SELL', 28, 82.94, GETDATE()),
(1, 46, 'BUY', 3, 95.67, GETDATE()),
(1, 47, 'SELL', 32, 49.98, GETDATE()),
(1, 48, 'BUY', 7, 35.65, GETDATE()),
(1, 49, 'BUY', 18, 10.45, GETDATE()),
(1, 50, 'SELL', 12, 31.85, GETDATE()),
(1, 51, 'BUY', 14, 14.23, GETDATE()),
(1, 52, 'SELL', 27, 123.40, GETDATE()),
(1, 53, 'BUY', 11, 78.90, GETDATE());
SELECT * from Transactions