# 📋 Signup Data Cleaner using pandas

A Python script that cleans and processes raw signup CSV data.

It standardizes dates, removes low-quality/test entries, normalizes emails (including Gmail handling), deduplicates users, and exports clean member data.

---

## 🚀 Features

* ✅ Handles messy CSV files
* ✅ Standardizes column names
* ✅ Parses multiple date formats
* ✅ Supports `"yesterday"` as a signup date
* ✅ Normalizes Gmail addresses (removes dots and `+` aliases)
* ✅ Detects and quarantines fake/test entries
* ✅ Deduplicates users by email
* ✅ Flags users with multiple plan types
* ✅ Exports:

  * `members_final.csv`
  * `quarantine.csv`

---

## 📂 Project Structure

```
.
├── signup.csv              # Input file
├── script.py               # Main processing script
├── members_final.csv       # Cleaned output
├── quarantine.csv          # Filtered low-quality entries
└── README.md
```

---

## 📥 Input Format

The script expects a CSV file named:

```
signup.csv
```

With at least 5 columns:

| name | email | signup_date | plan | notes |

Example:

```csv
name,email,signup_date,plan,notes
John Doe,john@gmail.com,2024-01-10,Basic,
Jane Smith,jane@gmail.com,yesterday,Premium,test entry
```

---

## 📤 Output Files

### 1️⃣ `members_final.csv`

Cleaned and deduplicated member list.

Columns:

| name | email | signup_date | plan | notes | is_multi_plan |

---

### 2️⃣ `quarantine.csv`

Contains low-quality or suspicious entries that were filtered out.

---

## 🛠 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/signup-data-cleaner.git
cd signup-data-cleaner
```

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 📦 requirements.txt

```
pandas>=1.5.0
```

---

## ▶️ Usage

Place your `signup.csv` file in the project folder, then run:

```bash
python script.py
```

After execution, you will see:

* `members_final.csv`
* `quarantine.csv`

generated in the same directory.

---

## 🧠 How It Works

1. Reads raw CSV (even if formatting is inconsistent)
2. Standardizes column names
3. Parses and normalizes dates
4. Normalizes email addresses
5. Flags low-quality/test entries
6. Sorts by latest signup date
7. Deduplicates users by normalized email
8. Exports cleaned results

---

## 🔍 Low-Quality Detection Rules

Entries are flagged if:

* Name/email/notes contain:

  * `test`
  * `fake`
  * `ignore`
  * `asdf`
* Email patterns like:

  * `test@`
  * `@example.com`
  * `test.`

---

## 📌 Notes

* Gmail normalization removes:

  * Dots in the local part
  * Anything after `+`
* Oldest fallback date used for sorting: `1900-01-01`
* Invalid dates are safely handled

---

## 📄 License

MIT License

---

## ✨ Author

Arpit tiwari

---

