# Drawabox Prompt Frequency Scraper

A Python web scraper that collects sketchbook submission titles from the [Drawabox Community Sketchbooks](https://drawabox.com/community/sketchbooks/) and analyzes how frequently different drawing prompts appear.

The scraper uses Selenium to load the Drawabox pages in a real browser, then BeautifulSoup to parse the resulting HTML.

## Features

- Scrapes multiple Drawabox sketchbook pages
- Extracts sketchbook submission titles
- Filters results to the **Sketchbooks** section
- Extracts drawing prompts from submission titles
- Counts the frequency of each prompt
- Displays prompts from most common to least common
- Uses a single Selenium browser session for multiple pages

## Example

A submission title on Drawabox may look like:

```text
DevyAmethyst's Sketchbook: Drawing Prompt: Spreading the Good Word
```

The scraper extracts:

```text
Spreading the Good Word
```

and adds it to the prompt frequency count.

Example output:

```text
============================================================
PROMPT FREQUENCIES
============================================================
  102 | Tiny Alien Terrarium
   55 | Spreading the Good Word
   20 | Parenting Practices
    1 | Spreading the Good Word about Lolipops
============================================================
Total prompt submissions counted: 178
Unique prompts: 4
============================================================
```

## Technologies

- **Python**
- **Selenium** — loads Drawabox pages and executes JavaScript
- **BeautifulSoup** — parses the HTML
- **Collections.Counter** — counts prompt frequencies

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Git Bash:**

```bash
source .venv/Scripts/activate
```

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate
```

**PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install selenium beautifulsoup4
```

## Usage

Run the scraper:

```bash
python scraper.py
```

The page range can be changed in the script:

```python
START_PAGE = 1
END_PAGE = 10
```

For example, to scrape pages 1–50:

```python
START_PAGE = 1
END_PAGE = 50
```

The scraper visits URLs in the following format:

```text
https://drawabox.com/community/sketchbooks/{page}/
```

## How It Works

### 1. Selenium loads the page

Drawabox may initially return a JavaScript-based waiting page instead of the actual content. Because `requests` does not execute JavaScript, Selenium is used to load the page in Chrome.

### 2. BeautifulSoup parses the page

Once the page has loaded, Selenium's `page_source` is passed to BeautifulSoup:

```python
soup = BeautifulSoup(driver.page_source, "html.parser")
```

### 3. The Sketchbooks section is located

The page contains multiple community submission sections. The scraper specifically looks for the section whose heading is:

```text
Sketchbooks
```

This prevents unrelated submissions elsewhere on the page from being counted.

### 4. Submission titles are extracted

The scraper searches for:

```css
li.homework-submission > div.meta > h3
```

within the Sketchbooks section.

### 5. The prompt is extracted

For a title such as:

```text
Username's Sketchbook: Drawing Prompt: Tiny Alien Terrarium
```

the text is split at the first two colons, producing:

```text
Tiny Alien Terrarium
```

### 6. Prompts are counted

Python's `Counter` keeps track of how many times each prompt appears:

```python
prompt_counts[prompt] += 1
```

Finally, the results are displayed using:

```python
prompt_counts.most_common()
```

## Project Structure

```text
drawabox-prompt-scraper/
│
├── scraper.py
├── .gitignore
└── README.md
```

## Notes

This project is intended for personal data collection and analysis of publicly accessible Drawabox community submission pages.

The scraper includes a short delay between page requests to avoid making requests too rapidly.

The website's HTML structure may change over time. If Drawabox changes its page layout or class names, the CSS selectors used by the scraper may need to be updated.

## Future Improvements

Possible improvements include:

- Automatically detect the last available page
- Export results to CSV
- Export individual submissions and prompts to JSON
- Add retry handling for failed page loads
- Replace fixed `sleep()` calls with Selenium's explicit waits
- Track prompt frequency over time
- Generate charts showing prompt popularity

## License

This project is for educational and personal use. Check Drawabox's terms and policies before using the scraper for large-scale or commercial data collection.
