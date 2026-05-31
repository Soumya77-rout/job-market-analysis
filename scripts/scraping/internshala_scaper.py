
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ---------------------------------------
# HEADERS
# ---------------------------------------
headers = {
    "User-Agent": "Mozilla/5.0"
}

# ---------------------------------------
# INTERNSHIP CATEGORY URLS
# ---------------------------------------
internship_roles = {

    "Data Analyst Internship":
        "https://internshala.com/internships/data-analyst-internship/",

    "Data Science Internship":
        "https://internshala.com/internships/data-science-internship/",

    "Python Internship":
        "https://internshala.com/internships/python-internship/",

    "Machine Learning Internship":
        "https://internshala.com/internships/machine-learning-internship/",

    "Artificial Intelligence Internship":
        "https://internshala.com/internships/artificial-intelligence-internship/",

    "Business Analyst Internship":
        "https://internshala.com/internships/business-analyst-internship/",

    "Software Development Internship":
        "https://internshala.com/internships/software-development-internship/",

    "Backend Development Internship":
        "https://internshala.com/internships/backend-development-internship/",

    "Frontend Development Internship":
        "https://internshala.com/internships/front-end-development-internship/",

    "Full Stack Development Internship":
        "https://internshala.com/internships/full-stack-development-internship/",

    "Web Development Internship":
        "https://internshala.com/internships/web-development-internship/",

    "SQL Internship":
        "https://internshala.com/internships/sql-internship/",

    "Power BI Internship":
        "https://internshala.com/internships/power-bi-internship/",

    "Tableau Internship":
        "https://internshala.com/internships/tableau-internship/",

    "Data Engineering Internship":
        "https://internshala.com/internships/data-engineering-internship/",

    "Cloud Computing Internship":
        "https://internshala.com/internships/cloud-computing-internship/",

    "Cyber Security Internship":
        "https://internshala.com/internships/cyber-security-internship/",

    "DevOps Internship":
        "https://internshala.com/internships/devops-internship/",

    "UI UX Internship":
        "https://internshala.com/internships/ui-ux-design-internship/",

    "Mobile App Development Internship":
        "https://internshala.com/internships/mobile-app-development-internship/",

    "Android Development Internship":
        "https://internshala.com/internships/android-app-development-internship/",

    "Java Internship":
        "https://internshala.com/internships/java-internship/",

    "C++ Internship":
        "https://internshala.com/internships/c-plus-plus-internship/",

    "Digital Marketing Internship":
        "https://internshala.com/internships/digital-marketing-internship/"
}

# ---------------------------------------
# EMPTY LIST
# ---------------------------------------
internship_data = []

# ---------------------------------------
# LOOP THROUGH ALL INTERNSHIP CATEGORIES
# ---------------------------------------
for role_category, url in internship_roles.items():

    print(f"\nScraping {role_category}...")

    try:

        # Request page
        response = requests.get(url, headers=headers)

        # Parse HTML
        soup = BeautifulSoup(response.text, "lxml")

        # Find internship cards
        internship_cards = soup.find_all(
            "div",
            class_="individual_internship"
        )

        print("Internships Found:", len(internship_cards))

        # -----------------------------------
        # LOOP THROUGH INTERNSHIP CARDS
        # -----------------------------------
        for card in internship_cards:

            # -------------------------------
            # INTERNSHIP TITLE
            # -------------------------------
            title_tag = card.find(
                "a",
                class_="job-title-href"
            )

            title = (
                title_tag.text.strip()
                if title_tag else "Not Available"
            )

            # -------------------------------
            # COMPANY
            # -------------------------------
            company_tag = card.find(
                "p",
                class_="company-name"
            )

            company = (
                company_tag.text.strip()
                if company_tag else "Not Available"
            )

            # -------------------------------
            # LOCATION
            # -------------------------------
            location_tag = card.find(
                "p",
                class_="row-1-item locations"
            )

            location = (
                location_tag.text.strip()
                if location_tag else "Not Available"
            )

            # -------------------------------
            # STIPEND & DURATION
            # -------------------------------
            details = card.find_all(
                "div",
                class_="row-1-item"
            )

            stipend = "Not Available"
            duration = "Not Available"

            if len(details) >= 2:
                stipend = details[0].text.strip()
                duration = details[1].text.strip()

            # -------------------------------
            # POSTING DATE
            # -------------------------------
            date_tag = card.find(
                "div",
                class_="status-inactive"
            )

            posting_date = (
                date_tag.text.strip()
                if date_tag else "Not Available"
            )

            # -------------------------------
            # SKILLS
            # -------------------------------
            skill_tags = card.find_all(
                "span",
                class_="round_tabs"
            )

            skills = ", ".join([
                skill.text.strip()
                for skill in skill_tags
            ])

            if skills == "":
                skills = "Not Available"

            # -------------------------------
            # INTERNSHIP LINK
            # -------------------------------
            if title_tag and title_tag.get("href"):
                internship_link = (
                    "https://internshala.com"
                    + title_tag.get("href")
                )
            else:
                internship_link = "Not Available"

            # -------------------------------
            # REMOTE TYPE
            # -------------------------------
            remote_type = (
                "Remote"
                if "Work from home" in location
                else "Onsite"
            )

            # -------------------------------
            # STORE DATA
            # -------------------------------
            internship_data.append({
                "Role Category": role_category,
                "Internship Title": title,
                "Company": company,
                "Location": location,
                "Remote Type": remote_type,
                "Stipend": stipend,
                "Duration": duration,
                "Posting Date": posting_date,
                "Skills": skills,
                "Internship Link": internship_link
            })

        # Delay to avoid blocking
        time.sleep(2)

    except Exception as e:
        print(f"Error scraping {role_category}: {e}")

# ---------------------------------------
# CREATE DATAFRAME
# ---------------------------------------
df = pd.DataFrame(internship_data)

# ---------------------------------------
# REMOVE DUPLICATES
# ---------------------------------------
df.drop_duplicates(inplace=True)

# ---------------------------------------
# CLEAN WHITESPACES
# ---------------------------------------
df = df.applymap(
    lambda x: x.strip() if isinstance(x, str) else x
)

# ---------------------------------------
# SAVE CSV
# ---------------------------------------
df.to_csv("internships_raw.csv", index=False)

# ---------------------------------------
# FINAL OUTPUT
# ---------------------------------------
print("\n-----------------------------------")
print("SCRAPING COMPLETED SUCCESSFULLY")
print("-----------------------------------")

print("\nTotal Internships Scraped:", len(df))

print("\nCSV file saved as:")
print("internships_raw.csv")

print("\nDataset Preview:\n")
print(df.head())

