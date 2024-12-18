using DP_PROJECT.DataAccess;
using DP_PROJECT.Models;

namespace DP_PROJECT.Controllers
{
    public class UserController
    {
        private readonly UserDAO _userDAO;

        public UserController(string connectionString)
        {
            _userDAO = new UserDAO(connectionString);
        }

        public User Authenticate(string username, string password)
        {
            return _userDAO.AuthenticateUser(username, password);
        }

        public void AddUser(string username, string password, string email)
        {
            var user = new User
            {
                Username = username,
                PasswordHash = password, 
                Email = email,
                CreatedAt = DateTime.Now
            };

            _userDAO.AddUser(user);
        }
    }
}
