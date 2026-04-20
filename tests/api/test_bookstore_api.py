import pytest
from api.bookstore_client import BookStoreAPI


@pytest.fixture(scope="session")
def api_client():
    from playwright.sync_api import sync_playwright
    p_cm = sync_playwright()
    p = p_cm.__enter__()  # start playwright and get Playwright instance
    request_context = p.request.new_context()
    client = BookStoreAPI(request_context)
    client.generate_token()
    client.login_and_get_user_id()
    yield client
    request_context.dispose()
    p_cm.__exit__(None, None, None)  # stop playwright


@pytest.fixture(autouse=True)
def clean_books(api_client):
    api_client.delete_all_books()
    yield
    api_client.delete_all_books()


@pytest.fixture(scope="session")
def all_isbns(api_client):
    books = api_client.get_all_books().json()["books"]
    return [b["isbn"] for b in books]


# ===================== Account =====================

def test_generate_token(api_client):
    # Перевіряє, що токен успішно згенеровано і він не порожній
    assert api_client.token is not None
    assert len(api_client.token) > 10


def test_is_authorized(api_client):
    # Перевіряє, що авторизований користувач отримує відповідь true
    resp = api_client.is_authorized()
    assert resp.status == 200
    assert resp.text() == "true"


def test_is_authorized_wrong_password(playwright):
    # Перевіряє, що користувач з невірним паролем не авторизований
    req = playwright.request.new_context()
    import json
    resp = req.post(
        "https://demoqa.com/Account/v1/Authorized",
        data=json.dumps({"userName": "Test_User123!", "password": "WrongPass"}),
        headers={"Content-Type": "application/json"}
    )
    assert resp.status in (200, 404)  # 404 якщо пароль не збігається
    if resp.status == 200:
        assert resp.text() == "false"
    req.dispose()


def test_login_returns_user_id(api_client):
    # Перевіряє, що після логіну повертається коректний UUID користувача
    assert api_client.user_id is not None
    assert len(api_client.user_id) == 36  # UUID format


def test_get_user(api_client):
    # Перевіряє, що GET /User повертає правильні дані авторизованого користувача
    resp = api_client.get_user()
    assert resp.status == 200
    data = resp.json()
    assert data["userId"] == api_client.user_id
    assert data["username"] == api_client.username


def test_get_user_unauthorized(playwright):
    # Перевіряє, що запит без токена повертає 401
    req = playwright.request.new_context()
    resp = req.get("https://demoqa.com/Account/v1/User/fake-id")
    assert resp.status == 401
    req.dispose()


# ===================== BookStore =====================

def test_get_all_books(api_client):
    # Перевіряє, що список книг містить 8 записів з обов'язковими полями isbn та title
    resp = api_client.get_all_books()
    assert resp.status == 200
    books = resp.json()["books"]
    assert len(books) == 8
    assert all("isbn" in b and "title" in b for b in books)


def test_get_book_by_isbn(api_client, all_isbns):
    # Перевіряє, що GET /Book повертає коректну книгу за ISBN з полями title та author
    resp = api_client.get_book(all_isbns[0])
    assert resp.status == 200
    data = resp.json()
    assert data["isbn"] == all_isbns[0]
    assert "title" in data
    assert "author" in data


def test_get_book_invalid_isbn(api_client):
    # Перевіряє, що запит з неіснуючим ISBN повертає 400 з відповідним повідомленням
    resp = api_client.get_book("0000000000000")
    assert resp.status == 400
    assert resp.json()["message"] == "ISBN supplied is not available in Books Collection!"


def test_add_book_to_collection(api_client, all_isbns):
    # Перевіряє успішне додавання книги до колекції користувача (статус 201)
    resp = api_client.add_book_to_user(all_isbns[0])
    assert resp.status == 201
    assert resp.json()["books"][0]["isbn"] == all_isbns[0]


def test_add_duplicate_book(api_client, all_isbns):
    # Перевіряє, що повторне додавання тієї самої книги повертає 400
    api_client.add_book_to_user(all_isbns[0])
    resp = api_client.add_book_to_user(all_isbns[0])
    assert resp.status == 400
    assert resp.json()["message"] == "ISBN already present in the User's Collection!"


def test_add_book_unauthorized(playwright, all_isbns):
    # Перевіряє, що додавання книги без токена повертає 401
    req = playwright.request.new_context()
    import json
    payload = {"userId": "fake", "collectionOfIsbns": [{"isbn": all_isbns[0]}]}
    resp = req.post(
        "https://demoqa.com/BookStore/v1/Books",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )
    assert resp.status == 401
    req.dispose()


def test_replace_book(api_client, all_isbns):
    # Перевіряє заміну книги в колекції: стара книга зникає, нова з'являється
    api_client.add_book_to_user(all_isbns[0])
    resp = api_client.replace_book(all_isbns[0], all_isbns[1])
    assert resp.status == 200
    isbns_in_collection = [b["isbn"] for b in resp.json()["books"]]
    assert all_isbns[1] in isbns_in_collection
    assert all_isbns[0] not in isbns_in_collection


def test_replace_book_not_in_collection(api_client, all_isbns):
    # Перевіряє, що заміна книги, якої немає в колекції, повертає 400
    resp = api_client.replace_book(all_isbns[0], all_isbns[1])
    assert resp.status == 400


def test_delete_all_books(api_client, all_isbns):
    # Перевіряє видалення всіх книг з колекції: статус 204, колекція порожня
    api_client.add_book_to_user(all_isbns[0])
    api_client.add_book_to_user(all_isbns[1])
    resp = api_client.delete_all_books()
    assert resp.status == 204
    user = api_client.get_user().json()
    assert user["books"] == []


def test_delete_single_book(api_client, all_isbns):
    # Перевіряє видалення однієї книги: статус 204, книга відсутня в колекції
    api_client.add_book_to_user(all_isbns[0])
    resp = api_client.delete_book(all_isbns[0])
    assert resp.status == 204
    user = api_client.get_user().json()
    assert all(b["isbn"] != all_isbns[0] for b in user["books"])


def test_delete_book_not_in_collection(api_client, all_isbns):
    # Перевіряє, що видалення книги, якої немає в колекції, повертає 400
    resp = api_client.delete_book(all_isbns[0])
    assert resp.status == 400
    assert resp.json()["message"] == "ISBN supplied is not available in User's Collection!"


def test_delete_books_unauthorized(playwright):
    # Перевіряє, що видалення книг без токена повертає 401
    req = playwright.request.new_context()
    resp = req.delete("https://demoqa.com/BookStore/v1/Books?UserId=fake-id")
    assert resp.status == 401
    assert resp.json()["message"] == "User not authorized!"
    req.dispose()