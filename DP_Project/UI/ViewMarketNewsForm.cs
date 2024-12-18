using System;
using System.Windows.Forms;
using DP_PROJECT.Controllers;

namespace DP_PROJECT.UI
{
    public partial class ViewMarketNewsForm : Form
    {
        private readonly MarketNewsController _newsController;

        public ViewMarketNewsForm()
        {
            InitializeComponent();

            // Get connection from Singleton
            var connection = DatabaseConnection.GetInstance().GetConnection();
            _newsController = new MarketNewsController(connection.ConnectionString);
        }

        private void ViewMarketNewsForm_Load(object sender, EventArgs e)
        {
            LoadNews();
        }

        private void LoadNews()
        {
            lstNews.Items.Clear();
            var newsList = _newsController.GetAllNews();
            foreach (var news in newsList)
            {
                lstNews.Items.Add($"{news.PublishedAt}: {news.Title}");
            }
        }

        private void btnAddNews_Click(object sender, EventArgs e)
        {
            var title = txtTitle.Text;
            var content = txtContent.Text;

            if (string.IsNullOrWhiteSpace(title) || string.IsNullOrWhiteSpace(content))
            {
                MessageBox.Show("Title and Content cannot be empty.");
                return;
            }

            _newsController.AddNews(title, content);
            LoadNews();
            txtTitle.Clear();
            txtContent.Clear();
            MessageBox.Show("News added successfully!");
        }

        private void btnDeleteNews_Click(object sender, EventArgs e)
        {
            if (lstNews.SelectedIndex == -1)
            {
                MessageBox.Show("Select a news item to delete.");
                return;
            }

            var selectedNews = lstNews.SelectedItem.ToString();
            var newsId = int.Parse(selectedNews.Split(':')[0]);

            _newsController.DeleteNews(newsId);
            LoadNews();
            MessageBox.Show("News deleted successfully!");
        }
    }
}
