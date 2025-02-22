using System;
using System.Collections.Generic;

public class StockMarket
{
    private readonly List<IStockObserver> _observers = new();
    private readonly Dictionary<int, Stock> _stocks = new();

    public void Attach(IStockObserver observer)
    {
        _observers.Add(observer);
    }

    public void Detach(IStockObserver observer)
    {
        _observers.Remove(observer);
    }

    public void UpdateStockPrice(int stockId, decimal newPrice)
    {
        if (_stocks.TryGetValue(stockId, out var stock))
        {
            stock.CurrentPrice = newPrice;
            NotifyObservers(stock);
        }
    }

    private void NotifyObservers(Stock stock)
    {
        foreach (var observer in _observers)
        {
            observer.Update(stock);
        }
    }
} 