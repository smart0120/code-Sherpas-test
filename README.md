# Bank Account Kata

This project is a full-stack application for managing bank accounts, built using Django for the backend and HTML/JavaScript with Bootstrap for the frontend. The application supports functionalities such as deposit, withdrawal, transfer, and viewing transactions.

## Requirements

- Python 3.x
- Django
- Django REST Framework

## Installation

1. **Clone the repository:**

   ```sh
    git clone https://github.com/yourusername/bankaccount.git
    cd bankaccount
    ```

2. **Create a virtual environment:**

   ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

   ```sh
    pip install -r requirements.txt
    ```

4. **Run migrations:**

   ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser (optional):**

   ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**

   ```sh
    python manage.py runserver
    ```

7. **Access the application:**

Open a web browser and go to http://127.0.0.1:8000 to view the frontend interface.


## API Endpoints
**Accounts:**

- POST /api/accounts/login_or_create/ - Login or create an account
- POST /api/accounts/{id}/deposit/ - Deposit money to the account
- POST /api/accounts/{id}/withdraw/ - Withdraw money from the account
- POST /api/accounts/{id}/transfer/ - Transfer money to another account

**Transactions:**

- GET /api/transactions/ - List all transactions (filter by account)