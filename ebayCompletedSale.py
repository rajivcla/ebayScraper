from lxml import html
import sys
import requests


def scrape_page(url):
    # set headers for downloading
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    print("Retrieving %s" % url)
    response = requests.get(url, headers=headers, verify=False)
    # response = requests.get(url)
    html_elem = html.fromstring(response.text)  # make html element

    # extract all child nodes from the list
    items = html_elem.xpath('//*[@id="srp-river-results"]/ul/child::node()')
    results = []

    # loop through completed ebay items
    for item in items:
        if item.tag == 'div':
            # check div tag for sold / completed listings.  don't include results matching fewer words
            if item.xpath('.//span[@class="BOLD"]/text()')[0] == "Results matching fewer words":
                break
        else:
            # extract
            itemlocal = item.xpath('.//a[@class="s-item__link"]')[0]
            link = itemlocal.xpath('@href')[0]
            title = itemlocal.xpath('h3/text()')[0]
            price = item.xpath('.//span[@class="s-item__price"]/span/text()')[0]
            results.append((link, title, price))
            # add shipping

    # print out results
    for r in results:
        print('{};{};{}'.format(r[0], r[1], r[2]))

    # check if results paginated. if so call scrape page again.  limit to 10x?


# read in command line arguments
if len(sys.argv) > 1:
    urlG = sys.argv[1]
    scrape_page(urlG)
