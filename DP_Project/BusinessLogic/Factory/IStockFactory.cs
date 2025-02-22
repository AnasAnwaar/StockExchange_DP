public interface IStockFactory
{
    Stock CreateStock(string symbol, string name, decimal price, StockType type);
} 