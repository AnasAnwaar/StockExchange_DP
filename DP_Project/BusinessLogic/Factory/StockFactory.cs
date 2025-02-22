using System;

public class StockFactory : IStockFactory
{
    public Stock CreateStock(string symbol, string name, decimal price, StockType type)
    {
        return type switch
        {
            StockType.Equity => new EquityStock(symbol, name, price),
            StockType.Bond => new BondStock(symbol, name, price),
            StockType.ETF => new ETFStock(symbol, name, price),
            _ => throw new ArgumentException("Invalid stock type")
        };
    }
} 