using System;
using System.Collections.Generic;
using Microsoft.Data.SqlClient;
using DP_PROJECT.Models;

namespace DP_PROJECT.DataAccess
{
    public class MarketNewsDAO
    {
        private readonly SqlConnection _connection;

        public MarketNewsDAO(string connectionString)
        {
            _connection = DatabaseConnection.GetInstance(connectionString).GetConnection();
        }

        
        public void AddNews(MarketNews news)
        {
            var query = "INSERT INTO MarketNews (Title, Content, PublishedAt) VALUES (@Title, @Content, @PublishedAt)";
            using (var command = new SqlCommand(query, _connection))
            {
                command.Parameters.AddWithValue("@Title", news.Title);
                command.Parameters.AddWithValue("@Content", news.Content);
                command.Parameters.AddWithValue("@PublishedAt", news.PublishedAt);
                command.ExecuteNonQuery();
            }
        }

       
        public List<MarketNews> GetAllNews()
        {
            var newsList = new List<MarketNews>();
            var query = "SELECT * FROM MarketNews ORDER BY PublishedAt DESC";

            using (var command = new SqlCommand(query, _connection))
            using (var reader = command.ExecuteReader())
            {
                while (reader.Read())
                {
                    newsList.Add(new MarketNews
                    {
                        NewsId = (int)reader["NewsId"],
                        Title = reader["Title"].ToString(),
                        Content = reader["Content"].ToString(),
                        PublishedAt = (DateTime)reader["PublishedAt"]
                    });
                }
            }

            return newsList;
        }

       
        public MarketNews GetNewsById(int newsId)
        {
            var query = "SELECT * FROM MarketNews WHERE NewsId = @NewsId";

            using (var command = new SqlCommand(query, _connection))
            {
                command.Parameters.AddWithValue("@NewsId", newsId);
                using (var reader = command.ExecuteReader())
                {
                    if (reader.Read())
                    {
                        return new MarketNews
                        {
                            NewsId = (int)reader["NewsId"],
                            Title = reader["Title"].ToString(),
                            Content = reader["Content"].ToString(),
                            PublishedAt = (DateTime)reader["PublishedAt"]
                        };
                    }
                }
            }

            return null;
        }

       
        public void DeleteNews(int newsId)
        {
            var query = "DELETE FROM MarketNews WHERE NewsId = @NewsId";
            using (var command = new SqlCommand(query, _connection))
            {
                command.Parameters.AddWithValue("@NewsId", newsId);
                command.ExecuteNonQuery();
            }
        }
    }
}
