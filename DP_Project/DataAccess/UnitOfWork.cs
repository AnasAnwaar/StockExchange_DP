using System;
using System.Threading.Tasks;

public interface IUnitOfWork : IDisposable
{
    IRepository<Stock> Stocks { get; }
    IRepository<User> Users { get; }
    IRepository<Transaction> Transactions { get; }
    Task CommitAsync();
}

public class UnitOfWork : IUnitOfWork
{
    private readonly DatabaseConnection _db;
    private bool _disposed;

    public IRepository<Stock> Stocks { get; private set; }
    public IRepository<User> Users { get; private set; }
    public IRepository<Transaction> Transactions { get; private set; }

    public UnitOfWork(DatabaseConnection db)
    {
        _db = db;
        Stocks = new StockRepository(_db);
        Users = new UserRepository(_db);
        Transactions = new TransactionRepository(_db);
    }

    public async Task CommitAsync()
    {
        using var transaction = _db.GetConnection().BeginTransaction();
        try
        {
            await transaction.CommitAsync();
        }
        catch
        {
            await transaction.RollbackAsync();
            throw;
        }
    }

    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }

    protected virtual void Dispose(bool disposing)
    {
        if (!_disposed && disposing)
        {
            _db.GetConnection().Dispose();
            _disposed = true;
        }
    }
} 