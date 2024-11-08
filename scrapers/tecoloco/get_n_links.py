from lxml import html

def get_n_links(html_content):
    RESULTS_Q_XPATH = '//*[@id="page"]/div[3]/div/div[2]/div[3]/label/span'
    parsed_html = html.fromstring(html_content)
    results_q = parsed_html.xpath(RESULTS_Q_XPATH)
    results_q = int(results_q[0].text)
    return results_q