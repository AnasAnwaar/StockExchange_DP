using Microsoft.Data.SqlClient;
using System;
using System.Threading.Tasks;

namespace DP_PROJECT.DataAccess
{
    public sealed class DatabaseConnection
    {
        private static volatile DatabaseConnection _instance;
        private static readonly object _lock = new();
        private readonly string _connectionString;
        private SqlConnection _connection;

        private DatabaseConnection(string connectionString)
        {
            _connectionString = connectionString ?? throw new ArgumentNullException(nameof(connectionString));
        }

        public static DatabaseConnection GetInstance(string connectionString = null)
        {
            if (_instance == null)
            {
                lock (_lock)
                {
                    _instance ??= new DatabaseConnection(connectionString ?? 
                        throw new ArgumentException("Connection string required for initialization"));
                }
            }
            return _instance;
        }

        public SqlConnection GetConnection()
        {
            if (_connection == null || _connection.State == System.Data.ConnectionState.Closed)
            {
                _connection = new SqlConnection(_connectionString);
                _connection.Open();
            }
            return _connection;
        }

        public async Task<SqlConnection> GetConnectionAsync()
        {
            if (_connection == null || _connection.State == System.Data.ConnectionState.Closed)
            {
                _connection = new SqlConnection(_connectionString);
                await _connection.OpenAsync();
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
