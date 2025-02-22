using System.ComponentModel.DataAnnotations;

public class BuyStockRequest
{
    [Required]
    public int UserId { get; set; }

    [Required]
    public int StockId { get; set; }

    [Required]
    [Range(1, int.MaxValue, ErrorMessage = "Quantity must be positive")]
    public int Quantity { get; set; }

    [Required]
    [Range(0.01, double.MaxValue, ErrorMessage = "Price must be positive")]
    public decimal Price { get; set; }
} 