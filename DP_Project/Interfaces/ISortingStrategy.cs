using DP_PROJECT.Models;
using System.Collections.Generic;

namespace DP_PROJECT.Interfaces
{
    public interface ISortingStrategy
    {
        List<Stock> Sort(List<Stock> stocks);
    }
}
