import json
from playwright.sync_api import APIRequestContext

class BookStoreAPI:
    def __init__(self, request: APIRequestContext):
        self.request = request
        self.base_url = "https://demoqa.com"
        self.username = "Test_User123!"
        self.password = "Test@User1"
        self.token = None
        self.user_id = None

    def _post_json(self, url, payload, headers=None):
        h = {"Content-Type": "application/json"}
        if headers:
            h.update(headers)
        return self.request.post(url, data=json.dumps(payload), headers=h)

    def _put_json(self, url, payload, headers=None):
        h = {"Content-Type": "application/json"}
        if headers:
            h.update(headers)
        return self.request.put(url, data=json.dumps(payload), headers=h)

    def _delete_json(self, url, payload, headers=None):
        h = {"Content-Type": "application/json"}
        if headers:
            h.update(headers)
        return self.request.delete(url, data=json.dumps(payload), headers=h)

    @property
    def _auth(self):
        return {"Authorization": f"Bearer {self.token}"}

    # --- Account ---

    def generate_token(self):
        payload = {"userName": self.username, "password": self.password}
        response = self._post_json(f"{self.base_url}/Account/v1/GenerateToken", payload)
        result = response.json()
        if result.get("status") == "Success":
            self.token = result.get("token")
        return self.token

    def login_and_get_user_id(self):
        payload = {"userName": self.username, "password": self.password}
        response = self._post_json(f"{self.base_url}/Account/v1/Login", payload)
        result = response.json()
        self.user_id = result.get("userId")
        return self.user_id

    def is_authorized(self):
        payload = {"userName": self.username, "password": self.password}
        return self._post_json(f"{self.base_url}/Account/v1/Authorized", payload)

    def get_user(self):
        return self.request.get(
            f"{self.base_url}/Account/v1/User/{self.user_id}",
            headers=self._auth
        )

    def delete_user(self):
        return self.request.delete(
            f"{self.base_url}/Account/v1/User/{self.user_id}",
            headers=self._auth
        )

    # --- BookStore ---

    def get_all_books(self):
        return self.request.get(f"{self.base_url}/BookStore/v1/Books")

    def get_book(self, isbn: str):
        return self.request.get(f"{self.base_url}/BookStore/v1/Book?ISBN={isbn}")

    def add_book_to_user(self, isbn: str):
        payload = {"userId": self.user_id, "collectionOfIsbns": [{"isbn": isbn}]}
        return self._post_json(f"{self.base_url}/BookStore/v1/Books", payload, self._auth)

    def replace_book(self, old_isbn: str, new_isbn: str):
        payload = {"userId": self.user_id, "isbn": new_isbn}
        return self._put_json(
            f"{self.base_url}/BookStore/v1/Books/{old_isbn}", payload, self._auth
        )

    def delete_all_books(self):
        return self.request.delete(
            f"{self.base_url}/BookStore/v1/Books?UserId={self.user_id}",
            headers=self._auth
        )

    def delete_book(self, isbn: str):
        payload = {"isbn": isbn, "userId": self.user_id}
        return self._delete_json(f"{self.base_url}/BookStore/v1/Book", payload, self._auth)