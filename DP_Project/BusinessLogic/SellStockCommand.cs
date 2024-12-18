using DP_PROJECT.BusinessLogic;

namespace DP_PROJECT.BusinessLogic.Commands
{
    public class SellStockCommand
    {
        private readonly StockFacade _facade;
        private readonly int _userId;
        private readonly int _stockId;
        private readonly int _quantity;

        public SellStockCommand(StockFacade facade, int userId, int stockId, int quantity)
        {
            _facade = facade;
            _userId = userId;
            _stockId = stockId;
            _quantity = quantity;
        }

        public void Execute()
        {
            _facade.SellStock(_userId, _stockId, _quantity);
        }
    }
}
