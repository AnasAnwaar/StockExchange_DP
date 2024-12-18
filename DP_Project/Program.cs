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

            
            var connectionString = "Server=DESKTOP-HS9F6CR\\MSSQLSERVER01;Database=DB_StockExchange;Trusted_Connection=True;";

            
            var loginForm = new LoginForm(connectionString);
            Application.Run(loginForm);
        }
    }
}
