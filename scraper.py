# import requests
# from bs4 import BeautifulSoup
# import json

# def scrape_isro_missions(url="https://www.isro.gov.in/Mission_SSLV_D3.html"):
#     try:
#         # Send HTTP request
#         headers = {'User-Agent': 'Mozilla/5.0'}  # Avoid bot detection
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Check for request errors

#         # Parse HTML
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Extract mission data (adjust selectors based on ISRO website)
#         missions = []
#         # Example: Assuming mission data is in divs with class 'mission-card'
#         for item in soup.select('div.mission-card'):  # Update selector as needed
#             name = item.find('h2').text.strip() if item.find('h2') else "Unknown"
#             date = item.find('span', class_='date').text.strip() if item.find('span', class_='date') else "Unknown"
#             description = item.find('p').text.strip() if item.find('p') else "No description"
#             missions.append({
#                 "name": name,
#                 "date": date,
#                 "description": description
#             })

#         # Save to JSON
#         with open('missions.json', 'w') as f:
#             json.dump(missions, f, indent=4)
        
#         print(f"Scraped {len(missions)} missions.")
#         return missions
#     except Exception as e:
#         print(f"Error scraping data: {e}")
#         return []

# if __name__ == "__main__":
#     # Test the scraper
#     missions = scrape_isro_missions()
#     print(missions[:2])  # Print first two missions for testing
