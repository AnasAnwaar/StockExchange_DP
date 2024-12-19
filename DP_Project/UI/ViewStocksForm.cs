using DP_PROJECT.Controllers;
using System;
using System.Windows.Forms;


namespace DP_PROJECT.UI
{
    public partial class ViewStocksForm : Form
    {
        private readonly StockController _stockController;

        public ViewStocksForm()
        {
            InitializeComponent();

            // Get connection from Singleton
            var connection = DatabaseConnection.GetInstance().GetConnection();
            _stockController = new StockController(connection.ConnectionString);
        }

        private void ViewStocksForm_Load(object sender, EventArgs e)
        {
            var stocks = _stockController.GetAllStocks();
            foreach (var stock in stocks)
            {
                lstStocks.Items.Add($"{stock.StockId}: {stock.StockName} - {stock.CurrentPrice:C}");
            }
        }
    }
}
