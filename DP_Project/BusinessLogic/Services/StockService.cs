using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using DP_Project.BusinessLogic.Commands;
using DP_Project.BusinessLogic.Factory;
using DP_Project.BusinessLogic.Observers;
using DP_Project.DataAccess.UnitOfWork;
using DP_Project.Models;
using Microsoft.Extensions.Logging;

namespace DP_Project.BusinessLogic.Services
{
    public class StockService : IStockService
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly StockMarket _stockMarket;
        private readonly IStockFactory _stockFactory;
        private readonly ILogger<StockService> _logger;

        public StockService(
            IUnitOfWork unitOfWork, 
            StockMarket stockMarket, 
            IStockFactory stockFactory,
            ILogger<StockService> logger)
        {
            _unitOfWork = unitOfWork ?? throw new ArgumentNullException(nameof(unitOfWork));
            _stockMarket = stockMarket ?? throw new ArgumentNullException(nameof(stockMarket));
            _stockFactory = stockFactory ?? throw new ArgumentNullException(nameof(stockFactory));
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        }

        public async Task<bool> BuyStock(int userId, int stockId, int quantity, decimal price)
        {
            if (quantity <= 0) throw new ArgumentException("Quantity must be positive", nameof(quantity));
            if (price <= 0) throw new ArgumentException("Price must be positive", nameof(price));

            try
            {
                var stock = await _unitOfWork.Stocks.GetByIdAsync(stockId);
                if (stock == null)
                {
                    _logger.LogWarning("Stock not found with ID {StockId}", stockId);
                    return false;
                }

                var user = await _unitOfWork.Users.GetByIdAsync(userId);
                if (user == null)
                {
                    _logger.LogWarning("User not found with ID {UserId}", userId);
                    return false;
                }

                decimal totalCost = price * quantity;
                if (user.Balance < totalCost)
                {
                    _logger.LogWarning("Insufficient funds for user {UserId}", userId);
                    return false;
                }

                var transaction = new Transaction
                {
                    UserId = userId,
                    StockId = stockId,
                    Quantity = quantity,
                    Price = price,
                    Type = TransactionType.Buy,
                    Date = DateTime.UtcNow
                };

                await _unitOfWork.Transactions.AddAsync(transaction);
                
                // Update user balance
                user.Balance -= totalCost;
                await _unitOfWork.Users.UpdateAsync(user);
                
                await _unitOfWork.CommitAsync();

                _stockMarket.UpdateStockPrice(stockId, price);
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing buy order for user {UserId}, stock {StockId}", 
                    userId, stockId);
                return false;
            }
        }

        // Implement other methods...
    }
} 