using System.Data.SqlClient;

namespace DP_PROJECT.DataAccess
{
    public sealed class DatabaseConnection
    {
        private static DatabaseConnection _instance;
        private readonly SqlConnection _connection;

        private DatabaseConnection(string connectionString)
        {
            _connection = new SqlConnection(connectionString);
        }

        public static DatabaseConnection GetInstance(string connectionString)
        {
            if (_instance == null)
            {
                _instance = new DatabaseConnection(connectionString);
            }
            return _instance;
        }

        public SqlConnection GetConnection()
        {
            if (_connection.State == System.Data.ConnectionState.Closed)
            {
                _connection.Open();
            }
            return _connection;
        }
    }
}
