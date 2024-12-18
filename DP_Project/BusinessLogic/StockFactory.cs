using DP_PROJECT.Models;

namespace DP_PROJECT.BusinessLogic
{
    public static class StockFactory
    {
        public static Stock CreateStock(string type, string name, string symbol, decimal price)
        {
            switch (type.ToLower())
            {
                case "equity":
                    return new Stock
                    {
                        StockName = name,
                        StockSymbol = symbol,
                        CurrentPrice = price
                    };
                case "bond":
                    return new Stock
                    {
                        StockName = $"{name} Bond",
                        StockSymbol = symbol,
                        CurrentPrice = price
                    };
                case "etf":
                    return new Stock
                    {
                        StockName = $"{name} ETF",
                        StockSymbol = symbol,
                        CurrentPrice = price
                    };
                default:
                    throw new ArgumentException("Invalid stock type");
            }
        }
    }
}
