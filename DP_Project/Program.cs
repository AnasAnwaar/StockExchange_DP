using System;
using System.Windows;
using System.Data.SqlClient;
using System.Windows.Forms;
using DP_PROJECT.UI;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;

namespace DP_PROJECT
{
    static class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            var builder = WebApplication.CreateBuilder(args);

            // Add services to the container
            builder.Services.AddSingleton<DatabaseConnection>();
            builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();
            builder.Services.AddScoped<IStockService, StockService>();
            builder.Services.AddSingleton<StockMarket>();
            builder.Services.AddSingleton<IStockFactory, StockFactory>();
            builder.Services.AddScoped<CommandHistory>();

            // Add controllers
            builder.Services.AddControllers();

            var app = builder.Build();

            // Configure the HTTP request pipeline
            app.UseHttpsRedirection();
            app.UseAuthorization();
            app.MapControllers();

            app.Run();
        }
    }
}
