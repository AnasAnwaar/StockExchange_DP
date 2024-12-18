using System;

namespace DP_PROJECT.Models
{
    public class Transaction
    {
        public int TransactionId { get; set; }
        public int UserId { get; set; }
        public int StockId { get; set; }
        public string TransactionType { get; set; }
        public int Quantity { get; set; }
        public decimal Price { get; set; }
        public DateTime TransactionDate { get; set; }
    }
}
