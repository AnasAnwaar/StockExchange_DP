using DP_PROJECT.Controllers;
using System;
using System.Windows.Forms;

namespace DP_PROJECT.UI
{
    public partial class PortfolioForm : Form
    {
        private readonly PortfolioController _portfolioController;

        public PortfolioForm()
        {
            InitializeComponent();

            // Get connection from Singleton
            var connection = DatabaseConnection.GetInstance().GetConnection();
            _portfolioController = new PortfolioController(connection.ConnectionString);
        }

        private void PortfolioForm_Load(object sender, EventArgs e)
        {
            var userId = 1; // Replace with dynamic user ID if authentication is implemented
            var portfolios = _portfolioController.GetUserPortfolio(userId);
            foreach (var portfolio in portfolios)
            {
                lstPortfolio.Items.Add($"{portfolio.StockId}: {portfolio.Quantity} shares");
            }
        }
    }
}
