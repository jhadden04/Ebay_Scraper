import webbrowser
import bs4
import requests
import ezgmail

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


def Ebay_scrape(emails_on, email):
    global description, url
    item = x
    hi = y
    lo = z
    item = item.replace(' ', '+')
    site = f'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw={item}&_sacat=0&LH_ItemCondition=3000&_udlo={lo}&_udhi={hi}&rt=nc&LH_BIN=1'
    res = requests.get(site)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    soupy = soup.select('#srp-river-results > ul > li:nth-child(2) > div > div.s-item__info.clearfix > a')
    try:
        global description
        description = (soupy[0].get_text())
    except:
        Ebay_scrape(emails_on, email)
    for tag in soupy:
        global url
        url = (tag.get('href'))
    if emails_on:
        ezgmail.send(email, description, url)
    print(description, url)
    return description, url


class EbayScraper(App):

    def build(self):
        self.layout = BoxLayout(padding=10, orientation='vertical')
        self.label = Label(text='Description')
        self.label1 = Label(text='URL')
        self.box = BoxLayout(orientation='vertical', padding=10)
        self.txt = TextInput(hint_text='The Item', size_hint=(2, .4), multiline=False)
        self.txt1 = TextInput(hint_text='Maximum Price', size_hint=(2, .4), multiline=False)
        self.txt2 = TextInput(hint_text='Minimum Price', size_hint=(2, .4), multiline=False)
        self.btn = Button(text='done')
        self.btn.bind(on_press=self.buttonClicked)
        self.layout.add_widget(self.txt)
        self.layout.add_widget(self.txt1)
        self.layout.add_widget(self.txt2)
        self.layout.add_widget(self.btn)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.label1)
        return self.layout

    def buttonClicked(self, btn):
        global x
        global y
        global z
        x = self.txt.text
        y = self.txt1.text
        z = self.txt2.text
        self.label.text = Ebay_scrape(False, None)[0]
        self.label1.text = Ebay_scrape(False, None)[1]




EbayScraper().run()
