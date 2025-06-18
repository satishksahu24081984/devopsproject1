import mechanicalsoup
import re
import pymysql

# --- DB CONFIGURATION (update with your credentials) ---
import os

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# --- Field mapping to clean field names ---
def clean_label(label):
    label = label.lower().strip()
    label = re.sub(r'[^a-z0-9 ]+', '', label)
    return label.replace(' ', '_')

def clean_value(value):
    return value.strip().replace('\n', ' ').replace('\r', '').replace('|', '').strip()

# --- Mappings to DB table fields ---
DB_FIELDS = {
    'tender_id': 'tender_id',
    'work_description': 'work_description',
    'organisation_chain': 'tender_organisation'
}

def get_tender_data():
    browser = mechanicalsoup.StatefulBrowser()

    # Step 1: Get tender list page
    print("🔍 Launching browser and opening homepage...")
    browser.open("https://mahatenders.gov.in/nicgep/app?page=Home&service=page")
    print("✅ Homepage opened. Navigating directly to organisation tenders...")
    detail_url = "https://mahatenders.gov.in/nicgep/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct&session=T&sp=SHZZjrmmzbnr9k5AksX9MldS0Fec7wUuNy1YFXyqSerE%3D"
    browser.open(detail_url)
    print(browser.get_current_page())

    page = browser.get_current_page()
    table_rows = page.find_all("tr", id=lambda x: x and x.startswith("informal_"))

    tender_links = []
    for row in table_rows:
        cols = row.find_all("td")
        if len(cols) >= 6:
            anchor = cols[4].find("a")
            if anchor:
                href = "https://mahatenders.gov.in" + anchor["href"]
                tender_links.append(href)

    if not tender_links:
        print("No tenders found.")
        return None

    # Step 2: Open first tender detail page
    browser.open(tender_links[0])
    tender_page = browser.get_current_page()

    # Step 3: Extract all .tablebg tables
    tables = tender_page.find_all("table", class_="tablebg")

    tender_data = {}

    for table in tables:
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            for i in range(0, len(cols) - 1, 2):
                key = clean_label(cols[i].get_text())
                val = clean_value(cols[i + 1].get_text())
                if key and val:
                    tender_data[key] = val

    return tender_data

def store_to_db(tender_data):
    # Extract only relevant fields
    db_values = {
        db_field: tender_data.get(scraped_field, '') for scraped_field, db_field in DB_FIELDS.items()
    }

    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        query = """
            INSERT INTO mytender (tender_id, work_description, tender_organisation)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (
            db_values['tender_id'],
            db_values['work_description'],
            db_values['tender_organisation']
        ))

        conn.commit()
        print("\n✅ Tender data stored successfully in database.")

    except Exception as e:
        print(f"\n❌ Database error: {e}")
    finally:
        if conn:
            conn.close()

def print_clean_table(data_dict):
    print("\n📌 Final Cleaned Tender Data:\n")
    max_width = max(len(k) for k in data_dict.keys())
    for k in sorted(data_dict):
        print(f"{k.ljust(max_width)} : {data_dict[k]}")

# ---  Main execution ---
if __name__ == "__main__":
    tender_data = get_tender_data()
    if tender_data:
        print_clean_table(tender_data)
        store_to_db(tender_data)