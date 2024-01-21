import requests
from bs4 import BeautifulSoup
import time
import random
import fake_useragent

# Function to scrape content from a given URL and save it to a file
def scrape_and_save(url, output_file):
    try:
        headers = {'User-Agent': fake_useragent.UserAgent().random}
        # Send a GET request to the URL with a delay
        time.sleep(random.uniform(0.5, 3))  # random delay from 0.5 to 3 seconds between requests to avoid triggering rate limits
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the div with class "index content-within" containing an <ol> tag
            target_div = soup.find('div', {'class': 'index content-within'})
            
            # Check if the target_div and ol tag exist
            if target_div and target_div.find('ol'):
                # Extract text from each <li> tag
                items = target_div.find('ol').find_all('li')
                
                # Open the file for writing in append mode
                with open(output_file, 'a', encoding='utf-8') as file:
                    # Write each item to the file
                    for item in items:
                        # Find the first <span> or <a> tag and get its text
                        tag = item.find(['span', 'a'])
                        text = tag.text.strip() if tag else ''
                        
                        # Remove the specified suffix if present
                        if tag.name == 'span' and text.endswith(" (See:"):
                            text = text[:-6].strip()
                        
                        # Write the text to the file
                        file.write(text + '\n')

                print(f"Data from {url} has been extracted and saved to {output_file}")
            else:
                print(f"Couldn't find the target div or ol tag in {url}.")
        else:
            print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while processing {url}: {str(e)}")

# Loop through letters A to Z and digit 0
for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0']:
    # Construct the URL for the current letter
    current_url = f"https://www.mayoclinic.org/tests-procedures/index?letter={letter}"

    # Specify the output file for each letter
    output_file = '../procedure_names.txt'

    # Call the scraping function for the current URL and save it to the output file
    scrape_and_save(current_url, output_file)