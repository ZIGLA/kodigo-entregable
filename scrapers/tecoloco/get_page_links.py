from bs4 import BeautifulSoup

def get_page_links(response):
    soup = BeautifulSoup(response.content, features="lxml")

    # Find all div elements with class "two-thirds" and class "job-result"
    job_result_divs = soup.find_all('div', class_='module job-result')
    
    links = []
    # Loop through the found divs and extract the href attribute
    for div in job_result_divs:
        # Find the anchor tag within the div with class "show-more"
        show_more_anchor = div.find('a', class_='show-more')
        if show_more_anchor:
            # Get the href attribute value
            href_value = show_more_anchor.get('href')
            links.append(href_value)
    
    return links