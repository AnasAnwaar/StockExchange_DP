using DP_PROJECT.Controllers;
using System;
using System.Windows.Forms;

namespace DP_PROJECT.UI
{
    public partial class CreateStockForm : Form
    {
        private readonly StockController _stockController;

        public CreateStockForm()
        {
            InitializeComponent();

            // Get connection from Singleton
            var connection = DatabaseConnection.GetInstance().GetConnection();
            _stockController = new StockController(connection.ConnectionString);
        }

        private void btnCreate_Click(object sender, EventArgs e)
        {
            var type = txtType.Text;
            var name = txtName.Text;
            var symbol = txtSymbol.Text;
            var price = decimal.Parse(txtPrice.Text);

            try
            {
                _stockController.CreateStock(type, name, symbol, price);
                MessageBox.Show("Stock created successfully!");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error: {ex.Message}");
            }
        }
    }
}
