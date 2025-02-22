using System.Collections.Generic;
using System.Threading.Tasks;
using Dapper;
using Microsoft.Extensions.Logging;

public class StockRepository : IRepository<Stock>
{
    private readonly DatabaseConnection _db;
    private readonly ILogger<StockRepository> _logger;

    public StockRepository(DatabaseConnection db, ILogger<StockRepository> logger)
    {
        _db = db ?? throw new ArgumentNullException(nameof(db));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }

    public async Task<Stock> GetByIdAsync(int id)
    {
        try
        {
            using var connection = await _db.GetConnectionAsync();
            return await connection.QueryFirstOrDefaultAsync<Stock>(
                "SELECT * FROM Stocks WHERE Id = @Id", new { Id = id });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting stock with ID {Id}", id);
            throw;
        }
    }

    public async Task<IEnumerable<Stock>> GetAllAsync()
    {
        try
        {
            using var connection = await _db.GetConnectionAsync();
            return await connection.QueryAsync<Stock>("SELECT * FROM Stocks");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting all stocks");
            throw;
        }
    }

    public async Task<Stock> AddAsync(Stock entity)
    {
        try
        {
            using var connection = await _db.GetConnectionAsync();
            var sql = @"
                INSERT INTO Stocks (Symbol, Name, CurrentPrice, Type) 
                VALUES (@Symbol, @Name, @CurrentPrice, @Type)
                RETURNING Id";
            
            entity.Id = await connection.QuerySingleAsync<int>(sql, entity);
            return entity;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error adding stock {@Stock}", entity);
            throw;
        }
    }

    public async Task UpdateAsync(Stock entity)
    {
        try
        {
            using var connection = await _db.GetConnectionAsync();
            var sql = @"
                UPDATE Stocks 
                SET Symbol = @Symbol, 
                    Name = @Name, 
                    CurrentPrice = @CurrentPrice, 
                    Type = @Type
                WHERE Id = @Id";
            
            await connection.ExecuteAsync(sql, entity);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error updating stock {@Stock}", entity);
            throw;
        }
    }

    public async Task DeleteAsync(int id)
    {
        try
        {
            using var connection = await _db.GetConnectionAsync();
            await connection.ExecuteAsync(
                "DELETE FROM Stocks WHERE Id = @Id", new { Id = id });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error deleting stock with ID {Id}", id);
            throw;
        }
    }

    // Implement other methods...
} 