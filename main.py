import bs4


html = open("xml_test.xml", 'r')
soup = bs4.BeautifulSoup(html, 'lxml')
print(soup)
