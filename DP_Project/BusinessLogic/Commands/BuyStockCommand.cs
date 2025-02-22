using DP_PROJECT.BusinessLogic;

namespace DP_PROJECT.BusinessLogic.Commands
{
    public class BuyStockCommand : ICommand
    {
        private readonly IStockService _stockService;
        private readonly int _userId;
        private readonly int _stockId;
        private readonly int _quantity;
        private readonly decimal _price;

        public BuyStockCommand(IStockService stockService, int userId, int stockId, int quantity, decimal price)
        {
            _stockService = stockService;
            _userId = userId;
            _stockId = stockId;
            _quantity = quantity;
            _price = price;
        }

        public bool Execute()
        {
            return _stockService.BuyStock(_userId, _stockId, _quantity, _price);
        }

        public bool Undo()
        {
            return _stockService.SellStock(_userId, _stockId, _quantity, _price);
        }

        public string GetDescription() => 
            $"Buy {_quantity} shares of stock {_stockId} at {_price:C} for user {_userId}";
    }
}
