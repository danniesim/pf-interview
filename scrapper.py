import string
import urllib.request as urllib2
from bs4 import BeautifulSoup
from bs4.element import Comment

quote_page = 'http://www.bloomberg.com/quote/SPX:IND'
page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
name_box = soup.find('h1', attrs={'class': 'name'})
name = name_box.text.strip()
price_box = soup.find('div', attrs={'class':'price'})
price = price_box.text

print(name, price)

html = urllib2.urlopen('https://www.harper-adams.ac.uk/courses/undergraduate/201020/agribusiness')

soup = BeautifulSoup(html, 'html.parser')

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()

text = soup.get_text()
# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)
print(text)

trans = {ord(c): ' ' for c in string.punctuation}

print('abc/xyz'.translate(trans))
