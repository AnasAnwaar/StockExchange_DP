using System;

namespace DP_PROJECT.Models
{
    public class Stock
    {
        public int StockId { get; set; }
        public string StockName { get; set; }
        public string StockSymbol { get; set; }
        public decimal CurrentPrice { get; set; }
        public DateTime LastUpdated { get; set; }
    }
}
