using System;

namespace DP_PROJECT.Models
{
    public class Stock
    {
        public int Id { get; set; }
        public string Symbol { get; set; }
        public string Name { get; set; }
        public decimal CurrentPrice { get; set; }
        public StockType Type { get; set; }
    }

    public enum StockType
    {
        Equity,
        Bond,
        ETF
    }
}
