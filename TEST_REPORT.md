# 🧪 **CSC 255 – Password Vault Application**

# **Automated Testing Report**

**DRI:** *Jiajun Wang*
**Date:** *Nov 28, 2025*

---

## 📌 **1. Overview**

This document summarizes the automated tests performed for the **Password Vault Application** developed by the CSC 255 Oakton group.
The purpose of this testing was to validate the core functionalities of the system to ensure correctness, stability, and reliability.

Testing aligns with the following backlog task:

> **Nov 28, 2025 – App Dev – Create, run, and report test on implemented features**
> **DRI: Jiajun Wang**

All tests were executed locally using Python and were designed to validate the non-interactive program logic in `main.py`.

---

## 📁 **2. Files Tested**

The test suite (`test_vault.py`) focuses on the following functional modules:

| File            | Functionality                                     |
| --------------- | ------------------------------------------------- |
| **main.py**     | create, lookup, update, and list recent passwords |
| **vigenere.py** | encryption & decryption logic (implicitly used)   |
| **goodrich/**   | hash table & heap structure (used internally)     |

Interactive CLI (`cli_input.py`) was excluded from automation because it requires user input.

---

## 🧰 **3. Test Environment**

* **Device:** macOS (MacBook Air)
* **Python Version:** Python 3.x
* **Run command:**

  ```
  python3 test_vault.py
  ```

A separate test file (`test_vault.txt`) was used to avoid polluting the real `vault.txt` data.

---

## 🧪 **4. Test Cases & Results**

### ### ✔ Test 1: Create Password Entry

**Function:** `create_password_name(name, pwd)`
**Goal:** Ensure new password entries are stored correctly.
**Result:**

* Password successfully saved.
* Verified using `lookup_password_name(privateCall=1)`.

**Status:** ✅ Passed

---

### ✔ Test 2: Lookup Password Entry

**Function:** `lookup_password_name(name, privateCall=1)`
**Goal:** Confirm correct retrieval of previously stored passwords.
**Result:**

* Password returned matches stored value.

**Status:** ✅ Passed

---

### ✔ Test 3: Update Password Entry

**Function:** `update_password_name(name, pwd)`
**Goal:** Ensure existing entries can be updated with new values.
**Result:**

* Timestamp updated properly.
* Updated password retrieved correctly.

**Status:** ✅ Passed

---

### ✔ Test 4: Top 5 Most Recent Passwords

**Function:** `get_most_recent_password_names()`
**Goal:** Verify the function prints the 5 most recently updated entries.
**Result:**

* Function executed without crashing.
* Output list order was correct based on timestamps.

**Status:** ✅ Passed

---

## 📊 **5. Test Execution Output (Summary)**

```
✔ test_create_password passed
✔ test_lookup_password passed
✔ test_update_password passed
✔ test_top5_most_recent passed

ALL TESTS PASSED ✓
```

Screenshot or full output can be added as appendix if needed.

---

## 🔍 **6. Observations / Notes**

* The automated tests cover the **core logic** of the application.
* Interactive functions requiring user input were intentionally excluded.
* The system correctly handles file creation, updates, and hashed lookups.
* Max heap structure works as expected in ranking most recent updates.

---

## ⭐ **7. Conclusion**

All implemented features **passed automated testing successfully**.

The application’s core password storage and retrieval logic appears **functional, stable, and reliable**.
This completes the assigned task for Nov 28 under Jiajun Wang as the DRI.

---

## 📎 **8. Appendix: Files Used**

* `test_vault.py` (automated test suite)
* `test_vault.txt` (temporary test vault file)
* Core program files:

  * `main.py`
  * `vigenere.py`
  * `cli_input.py`
  * `goodrich/` data structures

---
