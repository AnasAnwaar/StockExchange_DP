using System;
using DP_PROJECT.BusinessLogic;
using DP_PROJECT.DataAccess;
using DP_PROJECT.Models;
using System.Collections.Generic;

namespace DP_PROJECT.Controllers
{
    public class StockController
    {
        private readonly StockDAO _stockDAO;
        private readonly StockFacade _stockFacade;

        public StockController(string connectionString)
        {
            _stockDAO = new StockDAO(connectionString);
            _stockFacade = new StockFacade(connectionString);
        }

        public List<Stock> GetAllStocks()
        {
            try
            {
                return _stockDAO.GetAllStocks();
            }
            catch (Exception ex)
            {
                throw new Exception("Error fetching stocks: " + ex.Message, ex);
            }
        }

        public void BuyStock(int userId, int stockId, int quantity)
        {
            try
            {
                _stockFacade.BuyStock(userId, stockId, quantity);
            }
            catch (Exception ex)
            {
                throw new Exception("Error buying stock: " + ex.Message, ex);
            }
        }

        public void SellStock(int userId, int stockId, int quantity)
        {
            try
            {
                _stockFacade.SellStock(userId, stockId, quantity);
            }
            catch (Exception ex)
            {
                throw new Exception("Error selling stock: " + ex.Message, ex);
            }
        }
    }
}
