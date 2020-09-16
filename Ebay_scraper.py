import webbrowser
import bs4
import requests
import ezgmail


def Ebay_scrape(item, lo, hi,emails_on, email):
    global description, url
    item = item.replace(' ', '+')
    site = f'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw={item}&_sacat=0&LH_ItemCondition=3000&_udlo={lo}&_udhi={hi}&rt=nc&LH_BIN=1'
    res = requests.get(site)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    soupy = soup.select('#srp-river-results > ul > li:nth-child(2) > div > div.s-item__info.clearfix > a')
    try:
        description = (soupy[0].get_text())
    except:
        Ebay_scrape(item, lo, hi, emails_on, email)
    for tag in soupy:
        url = (tag.get('href'))
    print(description)
    print(url)
    if emails_on:
        ezgmail.send(email, description, url)


Ebay_scrape('monitor 1080', '15', '30', False, None)
