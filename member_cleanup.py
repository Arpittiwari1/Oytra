import pandas as pd
import re
from datetime import datetime, timedelta
import csv
import os

INPUT_FILE = "signup.csv"
OUTPUT_FINAL = "members_final.csv"
OUTPUT_QUARANTINE = "quarantine.csv"

def read_file(path):
    try:
        df = pd.read_csv(path,sep=None,engine="python",encoding="utf-8")
    except Exception:
        df = pd.read_csv(path,header=None,encoding="utf-8",dtype=str,engine="python" )
    if len(df.columns) == 1:
        raw = pd.read_csv(path, header=None, encoding="utf-8", dtype=str, engine="python")
        df = raw[0].str.split(",", expand=True)
    df = df.dropna(axis=1, how="all")
    return df

def ensure_columns(df):
    first = df.iloc[0].astype(str).str.lower().tolist()
    expected = ["name","email","signup_date","plan","notes"]
    if all(any(e == cell for cell in first) for e in expected):
        df.columns = df.iloc[0].tolist()
        df = df.drop(index=0).reset_index(drop=True)
    if len(df.columns) < 5:
        raise SystemExit("CSV does not contain at least 5 columns.")
    df = df.iloc[:, :5]
    df.columns = ["name","email","signup_date","plan","notes"]
    df = df.fillna("")
    return df

def date_parsing(s):
    s = str(s).strip()
    if not s:
        return pd.NaT
    if s.lower() == "yesterday":
        return pd.to_datetime(datetime.today() - timedelta(days=1)).normalize()
    for fmt in ("%Y-%m-%d","%d/%m/%y","%m/%d/%y","%d/%m/%Y","%m/%d/%Y"):
        try:
            return pd.to_datetime(s, format=fmt, errors="raise")
        except Exception as e:
            pass
    return pd.to_datetime(s, errors="coerce")

def normalize_email(e):
    e = str(e).strip().lower()
    if "@" not in e:
        return e
    local, domain = e.split("@",1)
    if domain in ("gmail.com","googlemail.com"):
        local = local.split("+",1)[0].replace(".","")
        return f"{local}@{domain}"
    return e

def low_quality(row):
    text = " ".join([row["name"], row["email"], row["notes"]]).lower()
    if any(tok in text for tok in ("test","ignore","ignore this","fake","asdf","example")):
        return True
    if re.search(r"(^test@|@example\.com$|^test\.)", row["email"].lower()):
        return True
    return False

def main():
    if not os.path.exists(INPUT_FILE):
        raise SystemExit(f"Place {INPUT_FILE} in the script folder.")
    raw = read_file(INPUT_FILE)
    df = ensure_columns(raw)
    df["signup_date_parsed"] = df["signup_date"].apply(date_parsing)
    df["signup_date"] = df["signup_date_parsed"].dt.strftime("%Y-%m-%d").fillna("")
    df["email_norm"] = df["email"].apply(normalize_email)
    df["low_quality"] = df.apply(low_quality, axis=1)
    quarantine = df[df["low_quality"]].copy()
    keep = df[~df["low_quality"]].copy()
    keep["sort_date"] = keep["signup_date_parsed"].fillna(pd.Timestamp("1900-01-01"))
    keep = keep.sort_values("sort_date", ascending=False)

    def pick_latest(group):
        plans = group["plan"].dropna().unique().tolist()
        latest = group.iloc[0].copy()
        latest["is_multi_plan"] = len(plans) > 1
        return latest
    cleaned = keep.groupby("email_norm", group_keys=False).apply(pick_latest).reset_index(drop=True)
    out_cols = ["name","email","signup_date","plan","notes","is_multi_plan"]
    for c in out_cols:
        if c not in cleaned.columns:
            cleaned[c] = False if c == "is_multi_plan" else ""
    cleaned = cleaned[out_cols]
    quarantine_out = quarantine[["name","email","signup_date","plan","notes"]].copy()
    cleaned.to_csv(OUTPUT_FINAL, index=False, quoting=csv.QUOTE_MINIMAL)
    quarantine_out.to_csv(OUTPUT_QUARANTINE, index=False, quoting=csv.QUOTE_MINIMAL)

if __name__ == "__main__":
    main()
