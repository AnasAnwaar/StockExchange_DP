using System.Collections.Generic;
using DP_PROJECT.DataAccess;
using DP_PROJECT.Models;

namespace DP_PROJECT.Controllers
{
    public class MarketNewsController
    {
        private readonly MarketNewsDAO _newsDAO;

        public MarketNewsController(string connectionString)
        {
            _newsDAO = new MarketNewsDAO(connectionString);
        }

        public List<MarketNews> GetAllNews()
        {
            return _newsDAO.GetAllNews();
        }

        public void AddNews(string title, string content)
        {
            var news = new MarketNews
            {
                Title = title,
                Content = content,
                PublishedAt = DateTime.Now
            };
            _newsDAO.AddNews(news);
        }

        public void DeleteNews(int newsId)
        {
            _newsDAO.DeleteNews(newsId);
        }
    }
}
