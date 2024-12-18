using System;
using System.Windows.Forms;

namespace DP_PROJECT.UI
{
    public partial class MainForm : Form
    {
        public MainForm()
        {
            InitializeComponent();
        }

        private void btnViewStocks_Click(object sender, EventArgs e)
        {
            var viewStocksForm = new ViewStocksForm();
            viewStocksForm.ShowDialog();
        }

        private void btnManagePortfolio_Click(object sender, EventArgs e)
        {
            var portfolioForm = new PortfolioForm();
            portfolioForm.ShowDialog();
        }

        private void btnCreateStock_Click(object sender, EventArgs e)
        {
            var createStockForm = new CreateStockForm();
            createStockForm.ShowDialog();
        }

        private void btnExit_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }
    }
}
