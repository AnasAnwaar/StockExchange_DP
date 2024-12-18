using DP_PROJECT.DataAccess;
using DP_PROJECT.Models;
using System.Collections.Generic;

namespace DP_PROJECT.Controllers
{
    public class PortfolioController
    {
        private readonly PortfolioDAO _portfolioDAO;

        public PortfolioController(string connectionString)
        {
            _portfolioDAO = new PortfolioDAO(connectionString);
        }

        public List<Portfolio> GetUserPortfolio(int userId)
        {
            return _portfolioDAO.GetPortfoliosByUserId(userId);
        }
    }
}
