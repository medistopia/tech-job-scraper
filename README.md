# Tech Job Scraper & Analyzer

A Python-based web scraper that collects tech job listings from multiple sources, analyzes trends, and visualizes in-demand skills. Designed to help job seekers identify market trends and find entry-level/internship opportunities.

## Features

- 🔍 **Multi-Source Scraping**: Pulls job listings from RemoteOK and Remotive.io APIs
- 🎯 **Entry-Level Focus**: Automatically identifies and prioritizes internships and junior positions
- 📊 **Data Analysis**: Analyzes job titles, companies, skills, and location trends
- 📈 **Visualizations**: Generates professional charts showing most in-demand skills
- 💾 **Export to CSV**: Saves all job data for further analysis or applications
- 🌐 **Remote-First**: Highlights remote job opportunities

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/medistopia/tech-job-scraper.git
cd tech-job-scraper
```

2. Install required packages:
```bash
pip install requests beautifulsoup4 pandas matplotlib lxml
```

## Usage

Run the scraper:
```bash
python tech_job_scraper.py
```

The script will:
1. Scrape up to 150 job listings from multiple sources
2. Filter and prioritize entry-level/internship positions
3. Generate `tech_jobs.csv` with all job data
4. Create `top_skills.png` visualization
5. Display summary statistics in the terminal

### Output Files

- **`tech_jobs.csv`**: Complete job listing data including:
  - Job title
  - Company name
  - Location
  - Required skills
  - Application URL
  - Job level (Entry-Level vs Other)
  - Source

- **`top_skills.png`**: Bar chart showing the top 10 most demanded skills

## Sample Output

```
📈 TECH JOB MARKET SUMMARY
==================================================
Total Jobs Analyzed: 100
Unique Companies: 87
Remote Jobs: 35 (35.0%)
Entry-Level/Intern: 7 (7.0%)

📊 Top 15 Skills in Demand:
----------------------------------------
engineer.................  40 (40.0%)
software.................  32 (32.0%)
digital nomad............  30 (30.0%)
technical................  29 (29.0%)
support..................  29 (29.0%)
```

## Customization

### Change Search Keywords
Modify the `main()` function to search for different roles:
```python
scraper.scrape_remoteok_api(limit=100, filter_entry_level=True)
```

### Adjust Number of Listings
Change the `limit` parameter:
```python
scraper.scrape_remotive_rss(limit=100)  # Get more jobs
```

### Filter by Skills
The scraper automatically extracts common tech skills from job descriptions. You can modify the skill list in `_extract_skills_from_text()`.

## Project Structure

```
tech-job-scraper/
├── tech_job_scraper.py    # Main scraper script
├── tech_jobs.csv          # Generated job data
├── top_skills.png         # Generated visualization
└── README.md              # This file
```

## Technologies Used

- **Python 3**: Core programming language
- **Requests**: HTTP library for API calls
- **BeautifulSoup4**: HTML/XML parsing
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Data visualization
- **JSON**: API data handling

## Data Sources

- [RemoteOK](https://remoteok.com/) - Remote job listings API
- [Remotive.io](https://remotive.com/) - Remote tech jobs API

Both sources provide free, public APIs without authentication requirements.

## Future Enhancements

- [ ] Add email notifications for new entry-level positions
- [ ] Implement job tracking over time to identify trends
- [ ] Add salary range analysis
- [ ] Create interactive dashboard with Streamlit
- [ ] Add more job board sources
- [ ] Filter by specific technologies (Python, JavaScript, etc.)
- [ ] Geographic location filtering

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is open source and available under the MIT License.

## Author

**Joshua V.**  
University of North Georgia - Computer Science  
[LinkedIn](https://www.linkedin.com/in/jevene/) | [GitHub](https://github.com/medistopia)

## Acknowledgments

- Built as part of a machine learning engineer career roadmap
- Designed to help students and job seekers identify market trends
- Special thanks to RemoteOK and Remotive for providing public APIs

---

**Note**: This tool is for educational and personal job search purposes. Please be respectful with API requests and follow each platform's terms of service.