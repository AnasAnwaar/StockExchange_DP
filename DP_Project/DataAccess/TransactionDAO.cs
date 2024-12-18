using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using DP_PROJECT.Models;

namespace DP_PROJECT.DataAccess
{
    public class TransactionDAO
    {
        private readonly SqlConnection _connection;

        public TransactionDAO(string connectionString)
        {
            _connection = DatabaseConnection.GetInstance(connectionString).GetConnection();
        }

       
        public void AddTransaction(Transaction transaction)
        {
            var query = "INSERT INTO Transactions (UserId, StockId, TransactionType, Quantity, Price, TransactionDate) " +
                        "VALUES (@UserId, @StockId, @TransactionType, @Quantity, @Price, @TransactionDate)";

            using (var command = new SqlCommand(query, _connection))
            {
                command.Parameters.AddWithValue("@UserId", transaction.UserId);
                command.Parameters.AddWithValue("@StockId", transaction.StockId);
                command.Parameters.AddWithValue("@TransactionType", transaction.TransactionType);
                command.Parameters.AddWithValue("@Quantity", transaction.Quantity);
                command.Parameters.AddWithValue("@Price", transaction.Price);
                command.Parameters.AddWithValue("@TransactionDate", transaction.TransactionDate);

                command.ExecuteNonQuery();
            }
        }

        
        public List<Transaction> GetTransactionsByUserId(int userId)
        {
            var transactions = new List<Transaction>();
            var query = "SELECT * FROM Transactions WHERE UserId = @UserId";

            using (var command = new SqlCommand(query, _connection))
            {
                command.Parameters.AddWithValue("@UserId", userId);

                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        transactions.Add(new Transaction
                        {
                            TransactionId = (int)reader["TransactionId"],
                            UserId = (int)reader["UserId"],
                            StockId = (int)reader["StockId"],
                            TransactionType = reader["TransactionType"].ToString(),
                            Quantity = (int)reader["Quantity"],
                            Price = (decimal)reader["Price"],
                            TransactionDate = (DateTime)reader["TransactionDate"]
                        });
                    }
                }
            }

            return transactions;
        }
    }
}
