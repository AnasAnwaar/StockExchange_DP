using System;
using System.Windows.Forms;
using DP_PROJECT.Controllers;

namespace DP_PROJECT.UI
{
    public partial class LoginForm : Form
    {
        private readonly UserController _userController;

        public LoginForm(string connectionString)
        {
            InitializeComponent();
            _userController = new UserController(connectionString);
        }

        private void btnLogin_Click(object sender, EventArgs e)
        {
            var username = txtUsername.Text;
            var password = txtPassword.Text;

            try
            {
                var user = _userController.Authenticate(username, password);
                if (user != null)
                {
                    MessageBox.Show($"Welcome, {user.Username}!");
                    this.Hide();
                    var mainForm = new MainForm();
                    mainForm.Show();
                }
                else
                {
                    MessageBox.Show("Invalid username or password.");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error: {ex.Message}");
            }
        }
    }
}
