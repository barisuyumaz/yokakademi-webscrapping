# 🎓 Turkish Universities & Academic Staff Scraper

This project scrapes data about academic staff from all universities in Turkey using the official [YÖK Academic Portal](https://akademik.yok.gov.tr/). It automatically extracts personal info, academic duties, and educational background, and exports the results into a `.txt` file in CSV format (delimiter=`$`), which can be opened and analyzed with Excel or Pandas.

📌 **Note:** This project is for academic/non-commercial purposes only.

---

## ⚙️ How it Works

1. The script (`yok-akademi-main.py`) first retrieves all universities listed on the YÖK Academic portal.
2. It then uses Selenium with a headless Chrome browser to visit each university's academic staff pages.
3. For each academic member, it scrapes:
   - Name, department, field
   - Email (if public)
   - Faculty info, ORCID (if available)
   - Academic position history
   - Education background (bachelor’s, master’s, PhD)
   - Interests and other tags
4. Data is appended line-by-line into a custom `.txt` file with `$`-separated columns.

## Usage

1. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the script:

    ```bash
    yok-akademi-main.py
    ```


## ✅ Example Use Cases

- Analyze trends in academic appointments across Turkish universities.
- Map academic research areas based on departments and institutions.
- Create structured datasets for educational or sociological studies.
- Generate visualizations and statistics to explore the structure of Turkish academia.
