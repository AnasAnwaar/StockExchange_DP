public interface IStockService
{
    Task<bool> BuyStock(int userId, int stockId, int quantity, decimal price);
    Task<bool> SellStock(int userId, int stockId, int quantity, decimal price);
    Task<IEnumerable<Stock>> GetAllStocks();
    Task<Stock> GetStockById(int id);
} 