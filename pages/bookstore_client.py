from playwright.sync_api import APIRequestContext

class BookStoreAPI:
    def __init__(self, request: APIRequestContext):
        self.request = request
        self.base_url = "https://demoqa.com"
        self.username = "Test_User123!"
        self.password = "Test_User"
        self.token = None
        self.user_id = None

    def generate_token(self):
        """Отримує токен доступу"""
        payload = {
            "userName": self.username,
            "password": self.password
        }
        response = self.request.post(f"{self.base_url}/Account/v1/GenerateToken", data=payload)
        result = response.json()
        
        if result.get("status") == "Success":
            self.token = result.get("token")
            return self.token
        return None

    def login_and_get_user_id(self):
        """Авторизується та отримує UUID користувача"""
        payload = {
            "userName": self.username,
            "password": self.password
        }
        response = self.request.post(f"{self.base_url}/Account/v1/Login", data=payload)
        result = response.json()
        self.user_id = result.get("userId")
        return self.user_id

    def get_all_books(self):
        """Отримує список усіх книг (публічний запит)"""
        return self.request.get(f"{self.base_url}/BookStore/v1/Books")

    def add_book_to_user(self, isbn: str):
        """Додає книгу до колекції (потребує токена)"""
        payload = {
            "userId": self.user_id,
            "collectionOfIsbns": [{"isbn": isbn}]
        }
        headers = {"Authorization": f"Bearer {self.token}"}
        return self.request.post(f"{self.base_url}/BookStore/v1/Books", data=payload, headers=headers)

    def delete_all_books(self):
        """Очищує колекцію користувача"""
        headers = {"Authorization": f"Bearer {self.token}"}
        return self.request.delete(
            f"{self.base_url}/BookStore/v1/Books?UserId={self.user_id}", 
            headers=headers
        )