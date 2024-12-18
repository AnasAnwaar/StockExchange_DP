using System.Linq;
using System.Collections.Generic;
using DP_PROJECT.Models;
using DP_PROJECT.Interfaces;

namespace DP_PROJECT.BusinessLogic.Strategies
{
    public class SortByPriceDescending : ISortingStrategy
    {
        public List<Stock> Sort(List<Stock> stocks)
        {
            return stocks.OrderByDescending(stock => stock.CurrentPrice).ToList();
        }
    }
}
