using DP_PROJECT.BusinessLogic;
using DP_PROJECT.DataAccess;

namespace DP_PROJECT.BusinessLogic.Commands
{
    public class BuyStockCommand
    {
        private readonly StockFacade _facade;
        private readonly int _userId;
        private readonly int _stockId;
        private readonly int _quantity;

        public BuyStockCommand(StockFacade facade, int userId, int stockId, int quantity)
        {
            _facade = facade;
            _userId = userId;
            _stockId = stockId;
            _quantity = quantity;
        }

        public void Execute()
        {
            _facade.BuyStock(_userId, _stockId, _quantity);
        }
    }
}
