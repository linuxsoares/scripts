# coding: utf-8

import urllib
from bs4 import BeautifulSoup

def getConvertObjectSoup(url, codin='utf-8'):
	f = urllib.urlopen(url)
	html_doc = f.read()
	
	return BeautifulSoup(html_doc, from_encoding=codin)

def getPessoasDesaparecidas():
	for i in range(0, 11):
		url = 'http://www.desaparecidos.gov.br/index.php/desparecidos?pag='+ str(i)
		soup = getConvertObjectSoup(url)

		print soup.find_all('div',attrs = { 'class' : 'boxDesaparecidor'})
		print i
	
def main():
	getPessoasDesaparecidas()

if __name__ == '__main__':
	main()
