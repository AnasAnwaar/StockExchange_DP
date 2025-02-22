using System;
using DP_PROJECT.BusinessLogic;
using DP_PROJECT.DataAccess;
using DP_PROJECT.Models;
using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace DP_PROJECT.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class StockController : ControllerBase
    {
        private readonly IStockService _stockService;
        private readonly CommandHistory _commandHistory;
        private readonly ILogger<StockController> _logger;

        public StockController(
            IStockService stockService, 
            CommandHistory commandHistory,
            ILogger<StockController> logger)
        {
            _stockService = stockService ?? throw new ArgumentNullException(nameof(stockService));
            _commandHistory = commandHistory ?? throw new ArgumentNullException(nameof(commandHistory));
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        }

        [HttpPost("buy")]
        public async Task<IActionResult> BuyStock([FromBody] BuyStockRequest request)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            try
            {
                var command = new BuyStockCommand(_stockService, request.UserId, 
                    request.StockId, request.Quantity, request.Price);
                
                _commandHistory.ExecuteCommand(command);
                return Ok(new { Message = "Stock purchase executed successfully" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing buy request {@Request}", request);
                return StatusCode(500, new { Message = "An error occurred while processing your request" });
            }
        }

        [HttpPost("undo")]
        public IActionResult UndoLastTransaction()
        {
            try
            {
                if (_commandHistory.Undo())
                    return Ok(new { Message = "Last transaction undone successfully" });
                return BadRequest(new { Message = "No transaction to undo" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing undo request");
                return StatusCode(500, new { Message = "An error occurred while processing your request" });
            }
        }

        // Implement other endpoints...
    }
}
