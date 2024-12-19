using System;
using System.Collections.Generic;
using DP_PROJECT.Models;
using DP_PROJECT.Interfaces;

namespace DP_PROJECT.BusinessLogic
{
    public class StockSorter
    {
        private ISortingStrategy _strategy;

        public void SetStrategy(ISortingStrategy strategy)
        {
            _strategy = strategy;
        }

        public List<Stock> SortStocks(List<Stock> stocks)
        {
            if (_strategy == null)
                throw new InvalidOperationException("Sorting strategy is not set.");

            return _strategy.Sort(stocks);
        }
    }
}
