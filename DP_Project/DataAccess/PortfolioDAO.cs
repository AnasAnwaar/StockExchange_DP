using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using DP_PROJECT.Models;

namespace DP_PROJECT.DataAccess
{
    public class PortfolioDAO
    {
        private readonly SqlConnection _connection;

        public PortfolioDAO(string connectionString)
        {
            _connection = DatabaseConnection.GetInstance(connectionString).GetConnection();
        }

        public List<Portfolio> GetPortfoliosByUserId(int userId)
        {
            try
            {
                var portfolios = new List<Portfolio>();
                var query = "SELECT * FROM Portfolios WHERE UserId = @UserId";

                using (var command = new SqlCommand(query, _connection))
                {
                    command.Parameters.AddWithValue("@UserId", userId);
                    using (var reader = command.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            portfolios.Add(new Portfolio
                            {
                                PortfolioId = (int)reader["PortfolioId"],
                                UserId = (int)reader["UserId"],
                                StockId = (int)reader["StockId"],
                                Quantity = (int)reader["Quantity"]
                            });
                        }
                    }
                }

                return portfolios;
            }
            catch (Exception ex)
            {
                throw new Exception("Error retrieving portfolios: " + ex.Message, ex);
            }
        }

        public void AddOrUpdatePortfolio(int userId, int stockId, int quantityChange)
        {
            try
            {
                var query = "SELECT * FROM Portfolios WHERE UserId = @UserId AND StockId = @StockId";
                using (var command = new SqlCommand(query, _connection))
                {
                    command.Parameters.AddWithValue("@UserId", userId);
                    command.Parameters.AddWithValue("@StockId", stockId);

                    using (var reader = command.ExecuteReader())
                    {
                        if (reader.Read())
                        {
                            var currentQuantity = (int)reader["Quantity"];
                            var newQuantity = currentQuantity + quantityChange;

                            reader.Close();

                            if (newQuantity <= 0)
                            {
                                var deleteQuery = "DELETE FROM Portfolios WHERE UserId = @UserId AND StockId = @StockId";
                                using (var deleteCommand = new SqlCommand(deleteQuery, _connection))
                                {
                                    deleteCommand.Parameters.AddWithValue("@UserId", userId);
                                    deleteCommand.Parameters.AddWithValue("@StockId", stockId);
                                    deleteCommand.ExecuteNonQuery();
                                }
                            }
                            else
                            {
                                var updateQuery = "UPDATE Portfolios SET Quantity = @Quantity WHERE UserId = @UserId AND StockId = @StockId";
                                using (var updateCommand = new SqlCommand(updateQuery, _connection))
                                {
                                    updateCommand.Parameters.AddWithValue("@Quantity", newQuantity);
                                    updateCommand.Parameters.AddWithValue("@UserId", userId);
                                    updateCommand.Parameters.AddWithValue("@StockId", stockId);
                                    updateCommand.ExecuteNonQuery();
                                }
                            }
                        }
                        else
                        {
                            reader.Close();

                            var insertQuery = "INSERT INTO Portfolios (UserId, StockId, Quantity) VALUES (@UserId, @StockId, @Quantity)";
                            using (var insertCommand = new SqlCommand(insertQuery, _connection))
                            {
                                insertCommand.Parameters.AddWithValue("@UserId", userId);
                                insertCommand.Parameters.AddWithValue("@StockId", stockId);
                                insertCommand.Parameters.AddWithValue("@Quantity", quantityChange);
                                insertCommand.ExecuteNonQuery();
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Error adding or updating portfolio: " + ex.Message, ex);
            }
        }
    }
}
