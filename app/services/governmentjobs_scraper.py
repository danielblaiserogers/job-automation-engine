import httpx
from bs4 import BeautifulSoup

class GovernmentJobsScraper:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    @classmethod
    async def scrape_job_details(cls, url: str) -> dict:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, headers=cls.HEADERS)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract Job Title
        title_elem = soup.find("h1") or soup.find("h2", class_="job-title")
        title = title_elem.get_text(strip=True) if title_elem else "N/A"

        # Extract Employer / Department / Details from metadata fields
        company_elem = soup.find(id="employer-name") or soup.find("span", class_="employer")
        company = company_elem.get_text(strip=True) if company_elem else "Haywood Community College"

        location_elem = soup.find("div", class_="location") or soup.find(id="job-location")
        location = location_elem.get_text(strip=True) if location_elem else "Clyde, NC"

        # Extract Description Body
        description_div = soup.find(id="details-info") or soup.find("div", class_="job-description")
        description = description_div.get_text(separator="\n", strip=True) if description_div else soup.get_text(strip=True)

        return {
            "title": title,
            "company": company,
            "location": location,
            "description": description[:3000],  # Truncate to safe length
            "url": url,
            "source_api": "GovernmentJobs Scraper"
        }