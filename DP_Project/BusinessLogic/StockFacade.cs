using System;
using DP_PROJECT.DataAccess;
using DP_PROJECT.Models;

namespace DP_PROJECT.BusinessLogic
{
    public class StockFacade
    {
        private readonly StockDAO _stockDAO;
        private readonly PortfolioDAO _portfolioDAO;
        private readonly TransactionDAO _transactionDAO;

        public StockFacade(string connectionString)
        {
            _stockDAO = new StockDAO(connectionString);
            _portfolioDAO = new PortfolioDAO(connectionString);
            _transactionDAO = new TransactionDAO(connectionString);
        }

        
        public void BuyStock(int userId, int stockId, int quantity)
        {
            var stock = _stockDAO.GetStockById(stockId);
            if (stock == null)
                throw new Exception("Stock not found!");

            
            var transaction = new Transaction
            {
                UserId = userId,
                StockId = stockId,
                TransactionType = "BUY",
                Quantity = quantity,
                Price = stock.CurrentPrice,
                TransactionDate = DateTime.Now
            };
            _transactionDAO.AddTransaction(transaction);

           
            _portfolioDAO.AddOrUpdatePortfolio(userId, stockId, quantity);
        }

      
        public void SellStock(int userId, int stockId, int quantity)
        {
            var stock = _stockDAO.GetStockById(stockId);
            if (stock == null)
                throw new Exception("Stock not found!");

            var portfolio = _portfolioDAO.GetPortfolioByUserAndStock(userId, stockId);
            if (portfolio == null || portfolio.Quantity < quantity)
                throw new Exception("Insufficient stock to sell!");

           
            var transaction = new Transaction
            {
                UserId = userId,
                StockId = stockId,
                TransactionType = "SELL",
                Quantity = quantity,
                Price = stock.CurrentPrice,
                TransactionDate = DateTime.Now
            };
            _transactionDAO.AddTransaction(transaction);

           
            _portfolioDAO.AddOrUpdatePortfolio(userId, stockId, -quantity);
        }

       
        public Stock GetStockDetails(int stockId)
        {
            return _stockDAO.GetStockById(stockId);
        }
    }
}
