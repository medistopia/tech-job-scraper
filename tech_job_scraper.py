"""
Tech Job Scraper & Analyzer v2
Improved version with multiple free job sources

Requirements:
pip install requests beautifulsoup4 pandas matplotlib lxml
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import json
import time

class TechJobScraper:
    def __init__(self):
        self.jobs = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_remoteok_api(self, limit=100, filter_entry_level=True):
        """
        Uses RemoteOK's JSON API endpoint (more reliable than HTML scraping)
        Args:
            limit: Number of jobs to scrape (default 100)
            filter_entry_level: If True, prioritize entry-level/intern positions
        """
        print("Scraping RemoteOK via API...")
        
        try:
            url = "https://remoteok.com/api"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # RemoteOK returns JSON array, first element is metadata
            all_jobs = response.json()[1:]  # Skip first element
            
            # Keywords that indicate entry-level or internship
            entry_keywords = ['intern', 'junior', 'entry', 'graduate', 'associate', 'trainee']
            
            entry_level_jobs = []
            other_jobs = []
            
            for job in all_jobs:
                position = job.get('position', '').lower()
                is_entry = any(keyword in position for keyword in entry_keywords)
                
                if is_entry:
                    entry_level_jobs.append(job)
                else:
                    other_jobs.append(job)
            
            # Prioritize entry-level jobs if filter is on
            if filter_entry_level:
                jobs_data = (entry_level_jobs + other_jobs)[:limit]
                print(f"Found {len(entry_level_jobs)} entry-level/intern positions")
            else:
                jobs_data = all_jobs[:limit]
            
            for job in jobs_data:
                try:
                    # Extract tags/skills
                    tags = job.get('tags', [])
                    if isinstance(tags, list):
                        skills = [tag for tag in tags if tag]
                    else:
                        skills = []
                    
                    job_data = {
                        'title': job.get('position', 'N/A'),
                        'company': job.get('company', 'N/A'),
                        'location': job.get('location', 'Remote'),
                        'skills': skills,
                        'url': job.get('url', ''),
                        'date': job.get('date', ''),
                        'level': 'Entry-Level' if is_entry else 'Other',
                        'source': 'RemoteOK'
                    }
                    
                    # Only add if we have a valid title
                    if job_data['title'] != 'N/A':
                        self.jobs.append(job_data)
                        
                except Exception as e:
                    print(f"Error parsing job: {e}")
                    continue
            
            print(f"✓ Scraped {len(self.jobs)} jobs from RemoteOK API")
            return True
            
        except Exception as e:
            print(f"✗ Error scraping RemoteOK API: {e}")
            return False
    

    def _extract_skills_from_text(self, text):
        """
        Extract common tech skills from job description text
        """
        common_skills = [
            'python', 'java', 'javascript', 'react', 'node', 'sql', 'aws', 'docker',
            'kubernetes', 'git', 'linux', 'c\\+\\+', 'c#', 'typescript', 'angular',
            'machine learning', 'data science', 'tensorflow', 'pytorch', 'pandas',
            'django', 'flask', 'mongodb', 'postgresql', 'redis', 'rest api'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in common_skills:
            if re.search(r'\b' + skill + r'\b', text_lower):
                found_skills.append(skill.title())
        
        return found_skills[:10]  # Limit to top 10 to avoid clutter
    
    def scrape_remotive_rss(self, limit=30):
        """
        Scrapes Remotive.io RSS feed for remote tech jobs
        Good source for remote internships and entry-level positions
        """
        print("Scraping Remotive.io RSS feed...")
        
        try:
            url = "https://remotive.com/api/remote-jobs?category=software-dev"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get('jobs', [])[:limit]
            
            for job in jobs:
                try:
                    title = job.get('title', 'N/A')
                    
                    # Determine if entry-level
                    entry_keywords = ['intern', 'junior', 'entry', 'graduate', 'associate']
                    is_entry = any(keyword in title.lower() for keyword in entry_keywords)
                    
                    # Extract skills from description
                    description = job.get('description', '')
                    skills = self._extract_skills_from_text(description)
                    
                    job_data = {
                        'title': title,
                        'company': job.get('company_name', 'N/A'),
                        'location': 'Remote',
                        'skills': skills,
                        'url': job.get('url', ''),
                        'date': job.get('publication_date', ''),
                        'level': 'Entry-Level' if is_entry else 'Other',
                        'source': 'Remotive'
                    }
                    
                    if job_data['title'] != 'N/A':
                        self.jobs.append(job_data)
                        
                except Exception as e:
                    continue
            
            print(f"✓ Scraped {len(jobs)} jobs from Remotive.io")
            return True
            
        except Exception as e:
            print(f"✗ Error scraping Remotive: {e}")
            return False
        """
        Adds sample data for testing/demonstration purposes
        """
        print("Adding sample tech job data for demonstration...")
        
        sample_jobs = [
            {
                'title': 'Machine Learning Engineer',
                'company': 'TechCorp',
                'location': 'Remote',
                'skills': ['Python', 'TensorFlow', 'PyTorch', 'AWS', 'Docker'],
                'source': 'Sample'
            },
            {
                'title': 'Senior Data Scientist',
                'company': 'DataWorks',
                'location': 'San Francisco, CA',
                'skills': ['Python', 'SQL', 'Machine Learning', 'Pandas', 'Scikit-learn'],
                'source': 'Sample'
            },
            {
                'title': 'AI Research Engineer',
                'company': 'AI Labs',
                'location': 'Remote',
                'skills': ['Python', 'Deep Learning', 'Research', 'TensorFlow', 'Mathematics'],
                'source': 'Sample'
            },
            {
                'title': 'Junior ML Engineer',
                'company': 'StartupXYZ',
                'location': 'New York, NY',
                'skills': ['Python', 'Machine Learning', 'Git', 'Docker', 'SQL'],
                'source': 'Sample'
            },
            {
                'title': 'Full Stack Developer',
                'company': 'WebSolutions',
                'location': 'Remote',
                'skills': ['JavaScript', 'React', 'Node.js', 'Python', 'MongoDB'],
                'source': 'Sample'
            },
            {
                'title': 'Backend Engineer',
                'company': 'CloudTech',
                'location': 'Austin, TX',
                'skills': ['Python', 'Django', 'PostgreSQL', 'Redis', 'AWS'],
                'source': 'Sample'
            },
            {
                'title': 'Data Engineer',
                'company': 'BigData Inc',
                'location': 'Remote',
                'skills': ['Python', 'Spark', 'Airflow', 'SQL', 'AWS', 'ETL'],
                'source': 'Sample'
            },
            {
                'title': 'ML Ops Engineer',
                'company': 'AI Platform',
                'location': 'Seattle, WA',
                'skills': ['Python', 'Kubernetes', 'Docker', 'MLflow', 'CI/CD'],
                'source': 'Sample'
            },
            {
                'title': 'Computer Vision Engineer',
                'company': 'Vision Labs',
                'location': 'Remote',
                'skills': ['Python', 'OpenCV', 'PyTorch', 'Deep Learning', 'CNNs'],
                'source': 'Sample'
            },
            {
                'title': 'NLP Engineer',
                'company': 'Language AI',
                'location': 'Boston, MA',
                'skills': ['Python', 'NLP', 'Transformers', 'BERT', 'Hugging Face'],
                'source': 'Sample'
            }
        ]
        
        self.jobs.extend(sample_jobs)
        print(f"✓ Added {len(sample_jobs)} sample jobs")
    
    def save_to_csv(self, filename="tech_jobs.csv"):
        """Save scraped jobs to CSV"""
        if not self.jobs:
            print("No jobs to save!")
            return
        
        # Flatten skills list for CSV
        jobs_flat = []
        for job in self.jobs:
            job_copy = job.copy()
            job_copy['skills'] = ', '.join(job['skills']) if job['skills'] else ''
            jobs_flat.append(job_copy)
        
        df = pd.DataFrame(jobs_flat)
        df.to_csv(filename, index=False)
        print(f"✓ Saved {len(self.jobs)} jobs to {filename}")
    
    def analyze_skills(self):
        """Analyze most common skills across job postings"""
        if not self.jobs:
            print("No jobs to analyze!")
            return
        
        # Flatten all skills into one list
        all_skills = []
        for job in self.jobs:
            all_skills.extend(job['skills'])
        
        # Count occurrences
        skill_counts = Counter(all_skills)
        top_skills = skill_counts.most_common(15)
        
        print("\n📊 Top 15 Skills in Demand:")
        print("-" * 40)
        for skill, count in top_skills:
            percentage = (count / len(self.jobs)) * 100
            print(f"{skill:.<25} {count:>3} ({percentage:.1f}%)")
        
        return top_skills
    
    def analyze_titles(self):
        """Analyze job titles to find common roles"""
        if not self.jobs:
            print("No jobs to analyze!")
            return
        
        titles = [job['title'] for job in self.jobs]
        
        # Extract key role types
        role_keywords = {
            'Engineer': 0,
            'Developer': 0,
            'Data': 0,
            'Machine Learning': 0,
            'ML': 0,
            'AI': 0,
            'Senior': 0,
            'Junior': 0,
            'Full Stack': 0,
            'Backend': 0,
            'Frontend': 0,
            'Scientist': 0
        }
        
        for title in titles:
            for keyword in role_keywords.keys():
                if keyword.lower() in title.lower():
                    role_keywords[keyword] += 1
        
        print("\n📋 Job Title Analysis:")
        print("-" * 40)
        sorted_roles = sorted(role_keywords.items(), key=lambda x: x[1], reverse=True)
        for role, count in sorted_roles:
            if count > 0:
                percentage = (count / len(self.jobs)) * 100
                print(f"{role:.<25} {count:>3} ({percentage:.1f}%)")
    
    def visualize_skills(self, top_n=10):
        """Create visualization of top skills"""
        if not self.jobs:
            print("No jobs to visualize!")
            return
        
        all_skills = []
        for job in self.jobs:
            all_skills.extend(job['skills'])
        
        skill_counts = Counter(all_skills)
        top_skills = skill_counts.most_common(top_n)
        
        if not top_skills:
            print("No skills data to visualize!")
            return
        
        skills, counts = zip(*top_skills)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.barh(skills, counts, color='#4A90E2')
        
        # Add value labels on bars
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, 
                   f'{int(width)}', 
                   ha='left', va='center', fontweight='bold', fontsize=10)
        
        ax.set_xlabel('Number of Job Postings', fontsize=12, fontweight='bold')
        ax.set_title(f'Top {top_n} Most Demanded Skills in Tech Jobs', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig('top_skills.png', dpi=300, bbox_inches='tight')
        print(f"\n✓ Visualization saved as 'top_skills.png'")
        plt.show()
    
    def get_summary(self):
        """Print summary statistics"""
        if not self.jobs:
            print("No jobs scraped yet!")
            return
        
        df = pd.DataFrame(self.jobs)
        
        print("\n" + "="*50)
        print("📈 TECH JOB MARKET SUMMARY")
        print("="*50)
        print(f"Total Jobs Analyzed: {len(self.jobs)}")
        print(f"Unique Companies: {df['company'].nunique()}")
        
        # Count remote vs onsite
        remote_count = sum(1 for job in self.jobs if 'remote' in job['location'].lower())
        print(f"Remote Jobs: {remote_count} ({(remote_count/len(self.jobs)*100):.1f}%)")
        
        # Count entry-level positions
        entry_count = sum(1 for job in self.jobs if job.get('level') == 'Entry-Level')
        if entry_count > 0:
            print(f"Entry-Level/Intern: {entry_count} ({(entry_count/len(self.jobs)*100):.1f}%)")
        
        print(f"\nTop 5 Companies Hiring:")
        company_counts = df['company'].value_counts().head()
        for company, count in company_counts.items():
            print(f"  {company}: {count} positions")


def main():
    """Main execution function"""
    
    # Initialize scraper
    scraper = TechJobScraper()
    
    print("Starting Tech Job Scraper v2...")
    print("Searching for internships and entry-level positions...")
    print("="*50)
    
    # Scrape from multiple sources
    # RemoteOK - 100 listings
    scraper.scrape_remoteok_api(limit=100, filter_entry_level=True)
    time.sleep(2)  # Be respectful with requests
    
    # Remotive - Remote jobs API (free, no auth)
    scraper.scrape_remotive_rss(limit=50)
    
    # If we got very few results, add sample data
    if len(scraper.jobs) < 10:
        print("\nNote: Using sample data for demonstration")
        scraper.add_sample_data()
    
    time.sleep(1)  # Brief pause
    
    # Save data
    scraper.save_to_csv("tech_jobs.csv")
    
    # Analyze data
    scraper.get_summary()
    scraper.analyze_titles()
    scraper.analyze_skills()
    
    # Create visualization
    scraper.visualize_skills(top_n=10)
    
    print("\n" + "="*50)
    print("✓ Analysis complete!")
    print("="*50)
    print("📁 Files created:")
    print("  • tech_jobs.csv - Raw job data")
    print("  • top_skills.png - Skills visualization")
    print("\n📊 Sources scraped:")
    print("  • RemoteOK API (up to 100 listings)")
    print("  • Remotive.io API (up to 50 listings)")
    print("\n💡 Tips:")
    print("  • Filter CSV for 'Entry-Level' jobs only")
    print("  • Check URLs to apply directly")
    print("  • Modify search keywords in main() function")


if __name__ == "__main__":
    main()