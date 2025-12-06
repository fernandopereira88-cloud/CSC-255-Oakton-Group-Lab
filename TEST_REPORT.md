# TEST REPORT – Password Vault Application
DRI: Jiajun Wang  
Date: Dec 5, 2025

This document summarizes automated tests for the Password Vault Application.  
Two levels of testing were performed:

1. Database-level testing (`test_database.py`)
2. Full CLI integration testing (`test_vault_cli.py`)

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

## 2. CLI Integration Tests

Test file: `test_vault_cli.py`  
Tests call `main()` directly and simulate user input using `unittest.mock.patch`.

Menu options tested:

1. Create password ✔  
2. Retrieve password ✔  
3. Update password ✔  
4. Delete password ✔  
5. Recent passwords ✔  
6. Exit ✔  

click.prompt, pwinput.pwinput, and click.echo were mocked successfully.  
All CLI flows completed with expected output.

---

## 3. Test Results

All tests passed.  
The application behaves correctly at both database and CLI levels.

---

## 4. How to Run Tests
`python test_database.py`

`python -m unittest test_vault_cli.py`

`python -m unittest discover `

