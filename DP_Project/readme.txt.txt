
# **Stock Exchange Management System**

## **Project Overview**
This project is a desktop application for managing a stock exchange system. It includes features like user authentication, portfolio management, stock transactions (buy/sell), market news management, and stock sorting. The application is built using C# with Windows Forms and integrates several design patterns to ensure scalability, maintainability, and robustness.

---

## **Design Patterns Implemented**

This project successfully implements the following design patterns:

### **1. Singleton Pattern**
- **Purpose**: Ensures that a single instance of the database connection is shared across the entire application to avoid redundant connections and resource usage.
- **Implemented in**:
  - **Class**: `DatabaseConnection`
    - **Methods**:
      - `GetInstance(string connectionString)`: Ensures only one instance of the `SqlConnection` is created.
      - `GetConnection()`: Provides access to the single connection instance.
    - **Why**: Reduces resource usage and ensures efficient database access.

---

### **2. Data Access Object (DAO) Pattern**
- **Purpose**: Abstracts database operations and provides a clean interface for CRUD operations on database tables.
- **Implemented in**:
  - **Classes**:
    - `UserDAO`: Manages operations related to the `Users` table.
      - **Methods**:
        - `AuthenticateUser(string username, string password)`: Authenticates a user by verifying their credentials.
        - `AddUser(User user)`: Adds a new user to the database.
    - `StockDAO`: Manages operations related to the `Stocks` table.
      - **Methods**:
        - `GetAllStocks()`: Retrieves all stocks.
        - `GetStockById(int stockId)`: Fetches stock details by ID.
    - `PortfolioDAO`: Manages operations for the `Portfolios` table.
      - **Methods**:
        - `GetPortfoliosByUserId(int userId)`: Retrieves the portfolio for a specific user.
        - `AddOrUpdatePortfolio(int userId, int stockId, int quantityChange)`: Adds or updates a user's portfolio.
    - `TransactionDAO`: Handles operations for the `Transactions` table.
      - **Methods**:
        - `AddTransaction(Transaction transaction)`: Logs a stock transaction.
    - `MarketNewsDAO`: Handles operations for the `MarketNews` table.
      - **Methods**:
        - `AddNews(MarketNews news)`: Adds a news entry.
        - `GetAllNews()`: Retrieves all market news.
    - **Why**: Promotes separation of concerns, improves code readability, and ensures modularity for database-related operations.

---

### **3. Facade Pattern**
- **Purpose**: Simplifies interactions between the user interface and the complex subsystems (DAOs) by providing a unified API.
- **Implemented in**:
  - **Class**: `StockFacade`
    - **Methods**:
      - `BuyStock(int userId, int stockId, int quantity)`: Handles the logic for buying stocks, including updating the portfolio and logging the transaction.
      - `SellStock(int userId, int stockId, int quantity)`: Handles selling stocks, including validation, updating the portfolio, and logging the transaction.
    - **Why**: Reduces complexity by providing a single interface for multiple DAO interactions and encapsulates business logic for stock transactions.

---

### **4. Command Pattern**
- **Purpose**: Encapsulates user actions (e.g., buying or selling stocks) as commands to decouple the sender from the logic of the action.
- **Implemented in**:
  - **Classes**:
    - `BuyStockCommand`
      - **Method**: `Execute()`: Executes the logic for buying stocks via the `StockFacade`.
    - `SellStockCommand`
      - **Method**: `Execute()`: Executes the logic for selling stocks via the `StockFacade`.
    - **Why**: Improves flexibility by decoupling the UI actions from the underlying logic and allows easy addition of new commands in the future.

---

### **5. Strategy Pattern**
- **Purpose**: Defines a family of algorithms (sorting strategies) and allows them to be interchangeable at runtime.
- **Implemented in**:
  - **Classes**:
    - `StockSorter`
      - **Methods**:
        - `SetStrategy(ISortingStrategy strategy)`: Sets the sorting strategy.
        - `SortStocks(List<Stock> stocks)`: Sorts the stocks using the selected strategy.
    - **Strategies**:
      - `SortByPriceAscending`: Sorts stocks by price in ascending order.
      - `SortByPriceDescending`: Sorts stocks by price in descending order.
    - **Why**: Provides flexibility to change sorting behavior dynamically based on user input without modifying the `StockSorter` class.

---

### **6. Factory Method Pattern**
- **Purpose**: Provides a way to create objects dynamically based on input without specifying their concrete classes.
- **Implemented in**:
  - **Class**: `StockFactory`
    - **Method**: `CreateStock(string type, string name, string symbol, decimal price)`: Creates a stock object based on the provided type (`equity`, `bond`, `etf`).
    - **Why**: Simplifies object creation and ensures scalability for adding new stock types.

---

## **Detailed Class and Method Usage**

| **Class**           | **Pattern**          | **Methods**                                         | **Purpose**                                                                 |
|----------------------|----------------------|----------------------------------------------------|-----------------------------------------------------------------------------|
| `DatabaseConnection` | Singleton           | `GetInstance`, `GetConnection`                     | Ensures a single database connection instance is used throughout the app.   |
| `UserDAO`            | DAO                 | `AuthenticateUser`, `AddUser`                      | Handles database operations for user authentication and registration.       |
| `StockDAO`           | DAO                 | `GetAllStocks`, `GetStockById`                     | Manages CRUD operations for the `Stocks` table.                             |
| `PortfolioDAO`       | DAO                 | `GetPortfoliosByUserId`, `AddOrUpdatePortfolio`    | Manages user portfolios.                                                    |
| `TransactionDAO`     | DAO                 | `AddTransaction`                                   | Logs stock transactions.                                                    |
| `MarketNewsDAO`      | DAO                 | `AddNews`, `GetAllNews`                            | Manages market news entries.                                                |
| `StockFacade`        | Facade              | `BuyStock`, `SellStock`                            | Simplifies stock transaction operations by interacting with multiple DAOs.  |
| `BuyStockCommand`    | Command             | `Execute`                                          | Executes stock purchase logic via `StockFacade`.                            |
| `SellStockCommand`   | Command             | `Execute`                                          | Executes stock selling logic via `StockFacade`.                             |
| `StockSorter`        | Strategy            | `SetStrategy`, `SortStocks`                        | Dynamically applies sorting strategies to stocks.                           |
| `SortByPriceAscending`, `SortByPriceDescending` | Strategy | N/A                                                | Implements sorting logic for stocks.                                        |
| `StockFactory`       | Factory Method      | `CreateStock`                                      | Dynamically creates stock objects based on type.                            |

---

## **Why Use Design Patterns?**
Design patterns ensure:
1. **Scalability**: The application can easily accommodate new features or changes.
2. **Maintainability**: Code is modular, making it easier to debug, test, and update.
3. **Reusability**: Patterns like DAO and Singleton promote code reuse.
4. **Decoupling**: Patterns like Command and Facade reduce dependencies between components.

---

