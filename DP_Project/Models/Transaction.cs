using System;

namespace DP_PROJECT.Models
{
    public class Transaction
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public int StockId { get; set; }
        public int Quantity { get; set; }
        public decimal Price { get; set; }
        public TransactionType Type { get; set; }
        public DateTime Date { get; set; }
    }

    public enum TransactionType
    {
        Buy,
        Sell
    }
}
