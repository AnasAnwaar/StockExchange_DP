using System.Collections.Generic;
using System.Data.SqlClient;
using DP_PROJECT.Models;

namespace DP_PROJECT.DataAccess
{
    public class StockDAO
    {
        private readonly SqlConnection _connection;

        public StockDAO(string connectionString)
        {
            _connection = DatabaseConnection.GetInstance(connectionString).GetConnection();
        }

        public List<Stock> GetAllStocks()
        {
            var stocks = new List<Stock>();
            var query = "SELECT * FROM Stocks";

            using (var command = new SqlCommand(query, _connection))
            using (var reader = command.ExecuteReader())
            {
                while (reader.Read())
                {
                    stocks.Add(new Stock
                    {
                        StockId = (int)reader["StockId"],
                        StockName = reader["StockName"].ToString(),
                        StockSymbol = reader["StockSymbol"].ToString(),
                        CurrentPrice = (decimal)reader["CurrentPrice"],
                        LastUpdated = (DateTime)reader["LastUpdated"]
                    });
                }
            }

            return stocks;
        }

        public Stock GetStockById(int stockId)
        {
            var query = "SELECT * FROM Stocks WHERE StockId = @StockId";

            using (var command = new SqlCommand(query, _connection))
            {
                command.Parameters.AddWithValue("@StockId", stockId);
                using (var reader = command.ExecuteReader())
                {
                    if (reader.Read())
                    {
                        return new Stock
                        {
                            StockId = (int)reader["StockId"],
                            StockName = reader["StockName"].ToString(),
                            StockSymbol = reader["StockSymbol"].ToString(),
                            CurrentPrice = (decimal)reader["CurrentPrice"],
                            LastUpdated = (DateTime)reader["LastUpdated"]
                        };
                    }
                }
            }

            return null;
        }
    }
}
