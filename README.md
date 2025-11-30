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
- Encryption module secures passwords before writing to disk.

### 3.2 CLI Flow
1. Run the app:  
   ```bash
   python main.py
