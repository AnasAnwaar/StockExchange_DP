using System;
using Microsoft.Data.SqlClient;
using DP_PROJECT.Models;
using Microsoft.AspNetCore.Identity;

namespace DP_PROJECT.DataAccess
{
    public class UserDAO
    {
        private readonly SqlConnection _connection;
        private readonly PasswordHasher<User> _passwordHasher;

        public UserDAO(string connectionString)
        {
            _connection = DatabaseConnection.GetInstance(connectionString).GetConnection();
            _passwordHasher = new PasswordHasher<User>(); 
        }

        public User AuthenticateUser(string username, string password)
        {
            try
            {
                var query = "SELECT * FROM Users WHERE Username = @Username";
                using (var command = new SqlCommand(query, _connection))
                {
                    command.Parameters.AddWithValue("@Username", username);

                    using (var reader = command.ExecuteReader())
                    {
                        if (reader.Read())
                        {
                            var user = new User
                            {
                                UserId = (int)reader["UserId"],
                                Username = reader["Username"].ToString(),
                                Email = reader["Email"].ToString(),
                                PasswordHash = reader["PasswordHash"].ToString(),
                                CreatedAt = (DateTime)reader["CreatedAt"]
                            };

                            var result = _passwordHasher.VerifyHashedPassword(user, user.PasswordHash, password);
                            if (result == PasswordVerificationResult.Success)
                            {
                                return user;
                            }
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
                user.PasswordHash = _passwordHasher.HashPassword(user, user.PasswordHash);

                var query = "INSERT INTO Users (Username, PasswordHash, Email, CreatedAt) VALUES (@Username, @PasswordHash, @Email, @CreatedAt)";
                using (var command = new SqlCommand(query, _connection))
                {
                    command.Parameters.AddWithValue("@Username", user.Username);
                    command.Parameters.AddWithValue("@PasswordHash", user.PasswordHash);
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
