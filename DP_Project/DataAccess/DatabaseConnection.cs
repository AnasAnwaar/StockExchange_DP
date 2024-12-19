using Microsoft.Data.SqlClient;
using System;

namespace DP_PROJECT.DataAccess
{
    public sealed class DatabaseConnection
    {
        private static DatabaseConnection _instance;
        private static readonly object _lock = new object();
        private readonly SqlConnection _connection;

        private DatabaseConnection(string connectionString)
        {
            if (string.IsNullOrWhiteSpace(connectionString))
            {
                throw new ArgumentException("Connection string cannot be null or empty.", nameof(connectionString));
            }

            _connection = new SqlConnection(connectionString);
        }

        public static DatabaseConnection GetInstance(string connectionString = null)
        {
            if (_instance == null)
            {
                lock (_lock)
                {
                    if (_instance == null)
                    {
                        if (connectionString == null)
                        {
                            throw new InvalidOperationException("Connection string must be provided when initializing the singleton.");
                        }
                        _instance = new DatabaseConnection(connectionString);
                    }
                }
            }
            return _instance;
        }

        public SqlConnection GetConnection()
        {
            if (_connection.State == System.Data.ConnectionState.Closed || _connection.State == System.Data.ConnectionState.Broken)
            {
                try
                {
                    _connection.Open();
                }
                catch (SqlException ex)
                {
                    throw new Exception("Failed to open the database connection. Check the connection string and database availability.", ex);
                }
            }
            return _connection;
        }

        public void CloseConnection()
        {
            if (_connection.State == System.Data.ConnectionState.Open)
            {
                _connection.Close();
            }
        }

        public bool IsConnectionOpen()
        {
            return _connection.State == System.Data.ConnectionState.Open;
        }
    }
}
