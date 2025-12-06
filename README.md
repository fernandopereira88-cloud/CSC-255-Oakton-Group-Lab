# CSC 255 – Password Vault Application  
Group Programming Assignment

## 1. Overview
The **Password Vault Application** is a Python command-line tool that allows users to securely store and manage passwords.  
Instead of keeping passwords on paper or in unsecured files, users can save, update, delete, and retrieve encrypted password entries in a local vault.

The project demonstrates the use of:
- Cryptography (custom encryption module)
- Data structures (hash table + max heap)
- File-based storage
- Command-line user interface
- Software design & team collaboration

---

## 2. Features

### ✔ Implemented
- **Create** a password entry (name + password)
- **Retrieve** password by name
- **Update** password for an existing entry
- **Delete** a password entry
- **View Top 5 recently updated** entries (using a max heap)
- **Encrypt / decrypt** passwords before storage
- **CLI menu** for user interaction
- **Local file database** to store all entries

---

## 3. How It Works

### 3.1 Architecture
- The vault contents are stored in a **file**.
- A **hash table** is used for in-memory fast lookups.
- A **max heap** tracks recently updated items for reporting.
- Passwords are encrypted with Vigenere algorithm before writing to disk.

### 3.2 Usage
1. Create a virtual environment to install dependencies
```sh
# Create a virtual environment named .venv
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate # For POSIX systems (macOS, Linux)
.\MyEnv\Scripts\Activate # For Windows

# Install dependencies
pip install -r requirements.txt

```
2. Run the app:  
```sh
python main.py
# OR
python3 main.py
```

## 4. Running Tests

This project includes **two automated test suites**:

### **4.1 Database Tests (low-level logic)**

Verifies vault file operations such as create, retrieve, update, delete, and recent-list logic.

Run:

```sh
python test_database.py
```

---

### **4.2 CLI Menu Tests**

Unit tests call `menu_execution()` directly and mock:

* `click.prompt`
* `pwinput.pwinput`
* `click.echo`
* database helpers

Run:

```sh
python -m unittest test_vault_cli.py
```

---

### **4.3 Run all tests**

```sh
python -m unittest discover .
```
