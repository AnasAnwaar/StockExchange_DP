using System;
using System.Windows.Forms;
using DP_PROJECT.UI;

namespace DP_PROJECT
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            // Connection string for database
            var connectionString = "YourConnectionStringHere";

            // Start with the login form
            var loginForm = new LoginForm(connectionString);
            Application.Run(loginForm);
        }
    }
}
