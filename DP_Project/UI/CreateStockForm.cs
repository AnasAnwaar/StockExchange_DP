using DP_PROJECT.Controllers;
using DP_PROJECT.DataAccess;
using Microsoft.Data.SqlClient;
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

            // Initialize the StockController with a connection string from the singleton DatabaseConnection
            var connection = DatabaseConnection.GetInstance("Server=DESKTOP-HS9F6CR\\MSSQLSERVER01;Database=DB_StockExchange;Trusted_Connection=True;").GetConnection();
            _stockController = new StockController(connection.ConnectionString);
        }

        private void btnCreate_Click(object sender, EventArgs e)
        {
            try
            {
                // Validate input fields
                var type = txtType.Text;
                var name = txtName.Text;
                var symbol = txtSymbol.Text;

                if (string.IsNullOrWhiteSpace(type) || string.IsNullOrWhiteSpace(name) || string.IsNullOrWhiteSpace(symbol))
                {
                    MessageBox.Show("Type, Name, and Symbol fields cannot be empty.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    return;
                }

                if (!decimal.TryParse(txtPrice.Text, out var price) || price <= 0)
                {
                    MessageBox.Show("Invalid price. Please enter a valid positive number.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    return;
                }

                // Create stock using the controller
                _stockController.CreateStock(type, name, symbol, price);

                // Display success message
                MessageBox.Show("Stock created successfully!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);

                // Clear input fields
                ClearFormFields();
            }
            catch (Exception ex)
            {
                // Display error message
                MessageBox.Show($"Error: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void ClearFormFields()
        {
            txtType.Clear();
            txtName.Clear();
            txtSymbol.Clear();
            txtPrice.Clear();
        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            // Close the form
            this.Close();
        }

        private void InitializeComponent()
        {
            this.txtType = new System.Windows.Forms.TextBox();
            this.txtName = new System.Windows.Forms.TextBox();
            this.txtSymbol = new System.Windows.Forms.TextBox();
            this.txtPrice = new System.Windows.Forms.TextBox();
            this.btnCreate = new System.Windows.Forms.Button();
            this.btnCancel = new System.Windows.Forms.Button();
            this.SuspendLayout();

            // txtType
            this.txtType.Location = new System.Drawing.Point(50, 30);
            this.txtType.Name = "txtType";
            this.txtType.Size = new System.Drawing.Size(200, 23);

            // txtName
            this.txtName.Location = new System.Drawing.Point(50, 70);
            this.txtName.Name = "txtName";
            this.txtName.Size = new System.Drawing.Size(200, 23);

            // txtSymbol
            this.txtSymbol.Location = new System.Drawing.Point(50, 110);
            this.txtSymbol.Name = "txtSymbol";
            this.txtSymbol.Size = new System.Drawing.Size(200, 23);

            // txtPrice
            this.txtPrice.Location = new System.Drawing.Point(50, 150);
            this.txtPrice.Name = "txtPrice";
            this.txtPrice.Size = new System.Drawing.Size(200, 23);

            // btnCreate
            this.btnCreate.Location = new System.Drawing.Point(50, 200);
            this.btnCreate.Name = "btnCreate";
            this.btnCreate.Size = new System.Drawing.Size(75, 23);
            this.btnCreate.Text = "Create";
            this.btnCreate.Click += new System.EventHandler(this.btnCreate_Click);

            // btnCancel
            this.btnCancel.Location = new System.Drawing.Point(175, 200);
            this.btnCancel.Name = "btnCancel";
            this.btnCancel.Size = new System.Drawing.Size(75, 23);
            this.btnCancel.Text = "Cancel";
            this.btnCancel.Click += new System.EventHandler(this.btnCancel_Click);

            // Form properties
            this.ClientSize = new System.Drawing.Size(300, 300);
            this.Controls.Add(this.txtType);
            this.Controls.Add(this.txtName);
            this.Controls.Add(this.txtSymbol);
            this.Controls.Add(this.txtPrice);
            this.Controls.Add(this.btnCreate);
            this.Controls.Add(this.btnCancel);
            this.Name = "CreateStockForm";
            this.Text = "Create Stock";
            this.ResumeLayout(false);
        }

        private System.Windows.Forms.TextBox txtType;
        private System.Windows.Forms.TextBox txtName;
        private System.Windows.Forms.TextBox txtSymbol;
        private System.Windows.Forms.TextBox txtPrice;
        private System.Windows.Forms.Button btnCreate;
        private System.Windows.Forms.Button btnCancel;
    }
}
