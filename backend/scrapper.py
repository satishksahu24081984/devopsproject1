import mechanicalsoup
import re
import pymysql
import os

# --- DB CONFIGURATION (using environment variables) ---
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# --- Clean field names and values ---
def clean_label(label):
    label = label.lower().strip()
    label = re.sub(r'[^a-z0-9 ]+', '', label)
    return label.replace(' ', '_')

def clean_value(value):
    return value.strip().replace('\n', ' ').replace('\r', '').replace('|', '').strip()

# --- Mapping of scraped fields to DB columns ---
DB_FIELDS = {
    'tender_id': 'tender_id',
    'work_description': 'work_description',
    'organisation_chain': 'tender_organisation'
}

# --- Store tender in DB (with env-based config) ---
def store_to_db(tender_data):
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

# --- Print cleaned data in readable format ---
def print_clean_table(data_dict):
    print("\n📌 Final Cleaned Tender Data:\n")
    max_width = max(len(k) for k in data_dict.keys())
    for k in sorted(data_dict):
        print(f"{k.ljust(max_width)} : {data_dict[k]}")
    print("-" * 60)

# --- Extract tender detail fields ---
def extract_tender_details(browser, url):
    browser.open(url)
    page = browser.get_current_page()
    tables = page.find_all("table", class_="tablebg")

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

# --- Main Execution ---
def main():
    browser = mechanicalsoup.StatefulBrowser()
    browser.session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    })

    # Step 1: Open main and organisation tender page
    browser.open("https://mahatenders.gov.in/nicgep/app?page=Home&service=page")
    detail_url = "https://mahatenders.gov.in/nicgep/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct&session=T&sp=Sdtz14ez7ZUEvqftoWmZMMNS0Fec7wUuNy1YFXyqSerE%3D"
    browser.open(detail_url)

    page = browser.get_current_page()
    table_rows = page.find_all("tr", id=lambda x: x and x.startswith("informal_"))

    tender_links = []
    for row in table_rows:
        cols = row.find_all("td")
        if len(cols) >= 6:
            anchor = cols[4].find("a")
            if anchor and anchor.has_attr("href"):
                href = "https://mahatenders.gov.in" + anchor["href"]
                tender_links.append(href)

    if not tender_links:
        print("❌ No tender links found.Please check website url")
        return

    # Step 2: Print only the first link
    first_tender_url = tender_links[0]
    print(f"\n🔗 First Tender Link:\n{first_tender_url}")

    # Step 3: Fetch and process only the first tender
    print("\n📥 Fetching data from first tender link...")
    try:
        tender_data = extract_tender_details(browser, first_tender_url)
        if tender_data:
            print_clean_table(tender_data)
            store_to_db(tender_data)
        else:
            print("⚠️ No data found on tender page.")
    except Exception as e:
        print(f"❌ Error while processing {first_tender_url}: {e}")

# Run it
if __name__ == "__main__":
    main()
