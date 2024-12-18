using System;
using System.Data.SqlClient;
using DP_PROJECT.Models;

namespace DP_PROJECT.DataAccess
{
    public class UserDAO
    {
        private readonly SqlConnection _connection;

        public UserDAO(string connectionString)
        {
            _connection = DatabaseConnection.GetInstance(connectionString).GetConnection();
        }

        
        public User AuthenticateUser(string username, string password)
        {
            try
            {
                
                string passwordHash = PasswordHasher.HashPassword(password);

              
                var query = "SELECT * FROM Users WHERE Username = @Username AND PasswordHash = @PasswordHash";
                using (var command = new SqlCommand(query, _connection))
                {
                    command.Parameters.AddWithValue("@Username", username);
                    command.Parameters.AddWithValue("@PasswordHash", passwordHash);

                    using (var reader = command.ExecuteReader())
                    {
                        if (reader.Read())
                        {
                            return new User
                            {
                                UserId = (int)reader["UserId"],
                                Username = reader["Username"].ToString(),
                                Email = reader["Email"].ToString(),
                                CreatedAt = (DateTime)reader["CreatedAt"]
                            };
                        }
                    }
                }

                return null; 
            }
            catch (Exception ex)
            {
                throw new Exception("Error authenticating user: " + ex.Message, ex);
            }
        }

        
        public void AddUser(User user)
        {
            try
            {
                
                string passwordHash = PasswordHasher.HashPassword(user.PasswordHash);

               
                var query = "INSERT INTO Users (Username, PasswordHash, Email, CreatedAt) VALUES (@Username, @PasswordHash, @Email, @CreatedAt)";
                using (var command = new SqlCommand(query, _connection))
                {
                    command.Parameters.AddWithValue("@Username", user.Username);
                    command.Parameters.AddWithValue("@PasswordHash", passwordHash);
                    command.Parameters.AddWithValue("@Email", user.Email);
                    command.Parameters.AddWithValue("@CreatedAt", user.CreatedAt);

                    command.ExecuteNonQuery();
                }
            }
            catch (Exception ex)
            {
                throw new Exception("Error adding user: " + ex.Message, ex);
            }
        }
    }
}
