from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from collections import Counter
import time

BASE_URL = "https://drawabox.com/community/sketchbooks/{}/"

# Change these
START_PAGE = 1
END_PAGE = 10


def scrape_pages(start_page, end_page):

    prompt_counts = Counter()

    # -----------------------------------------
    # Configure Chrome
    # -----------------------------------------

    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    try:

        for page in range(start_page, end_page + 1):

            url = BASE_URL.format(page)

            print(f"\nScraping page {page}...")
            print(url)

            driver.get(url)

            # Give the page time to load
            time.sleep(3)

            # -----------------------------------------
            # Parse page
            # -----------------------------------------

            soup = BeautifulSoup(driver.page_source, "html.parser")

            # -----------------------------------------
            # Find the "Sketchbooks" section
            # -----------------------------------------

            sketchbooks_section = None

            for section in soup.select("div.community-submissions"):

                heading = section.find("h2")

                if heading and heading.get_text(strip=True) == "Sketchbooks":
                    sketchbooks_section = section
                    break

            if sketchbooks_section is None:

                print("Could not find the Sketchbooks section.")
                continue

            # -----------------------------------------
            # Find submissions ONLY inside
            # the Sketchbooks section
            # -----------------------------------------

            titles = sketchbooks_section.select(
                "li.homework-submission > div.meta > h3"
            )

            print(f"Found {len(titles)} Sketchbook entries.")

            # -----------------------------------------
            # Extract prompts
            # -----------------------------------------

            for title in titles:

                text = title.get_text(" ", strip=True)

                print(f"  {text}")

                # Expected format:
                #
                # User's Sketchbook:
                # Drawing Prompt:
                # Spreading the Good Word

                parts = text.split(":", 2)

                if len(parts) != 3:
                    continue

                prompt = parts[2].strip()

                if prompt:
                    prompt_counts[prompt] += 1

            # Don't request pages too quickly
            time.sleep(1)

    finally:

        driver.quit()

    return prompt_counts


# ==================================================
# RUN SCRAPER
# ==================================================

counts = scrape_pages(START_PAGE, END_PAGE)


# ==================================================
# DISPLAY RESULTS
# ==================================================

print("\n")
print("=" * 60)
print("PROMPT FREQUENCIES")
print("=" * 60)

if not counts:

    print("No prompts were found.")

else:

    for prompt, count in counts.most_common():

        print(f"{count:5} | {prompt}")


print("=" * 60)
print(f"Total prompt submissions counted: {sum(counts.values())}")
print(f"Unique prompts: {len(counts)}")
print("=" * 60)
