# Signup Data Cleaner using pandas

It:

* Fixes dates (supports multiple formats + "yesterday")
* Normalizes emails (handles Gmail dots and + aliases)
* Removes test/fake entries
* Deduplicates users by email
* Exports cleaned results and quarantined records

## Requirements

```
pandas
```

## Run

Put `signup.csv` in the folder and run:

```
python script.py
```

It will generate:

* `members_final.csv`
* `quarantine.csv`

---

Simple utility script for cleaning member signup data.


##  Project Structure

```
.
├── signup.csv              # Input file
├── script.py               # Main processing script
├── members_final.csv       # Cleaned output
├── quarantine.csv          # Filtered low-quality entries
└── README.md
```

---
With at least 5 columns:

| name | email | signup_date | plan | notes |

Example:

```csv
name,email,signup_date,plan,notes
John Doe,john@gmail.com,2024-01-10,Basic,
Jane Smith,jane@gmail.com,yesterday,Premium,test entry
```

---

Columns:

| name | email | signup_date | plan | notes | is_multi_plan |

---

###  `quarantine.csv`

Contains low-quality or suspicious entries that were filtered out.

---

## Installation

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

##  requirements.txt

```
pandas
```

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

## 📄 License

MIT License

---

## ✨ Author

Arpit tiwari

---

