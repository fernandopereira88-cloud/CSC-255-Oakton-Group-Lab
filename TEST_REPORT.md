# TEST REPORT – Password Vault Application
DRI: Jiajun Wang  
Date: Dec 5, 2025

This document summarizes automated tests for the Password Vault Application.  
Two levels of testing were performed:

1. Database-level testing (`test_database.py`)
2. CLI menu unit tests (`test_vault_cli.py`)

---

## 1. Database Tests

Test file: `test_database.py`  
A temporary vault file is used to avoid modifying `vault.txt`.

Functions tested:

- create_password_name() ✔  
- lookup_password_name() ✔  
- update_password_name() ✔  
- delete_password_name() ✔  
- get_most_recent_password_names() (no-crash check) ✔  

All database operations behaved correctly, including timestamp updates and hash-map lookups.

---

## 2. CLI Menu Tests

Test file: `test_vault_cli.py`  
Unit tests exercise `menu_execution()` directly, mocking `click` and database dependencies.

Menu paths covered:

- Create password success + mismatch handling ✔  
- Retrieve password (found/missing) ✔  
- Exit option ✔  

Update, delete, and recent-report paths are not yet covered.

---

## 3. Test Results

All tests passed.  
The application behaves correctly at both database and CLI levels.

---

## 4. How to Run Tests
`python test_database.py`

`python -m unittest test_vault_cli.py`

`python -m unittest discover `
