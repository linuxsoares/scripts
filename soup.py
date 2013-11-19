# coding: iso-8859-15

import urllib
from bs4 import BeautifulSoup
import MySQLdb

#Arquivos TXT
encontrados = open('/Users/gilmar/Documents/Projetos/verbos/verbos_encontrados.txt', 'w')
nao_encontrados = open('/Users/gilmar/Documents/Projetos/verbos/verbos_nao_encontrados.txt', 'w')

try:
        db = MySQLdb.connect(host='localhost' , port=3306 ,user='gilmar', passwd='', db='verbos')

        cursor = db.cursor()

        cursor.execute('select * from verbos')

        for x in cursor.fetchall():
                verbo = x[1]

                url = 'http://www.dicionariodoaurelio.com/'+verbo+'.html'
                f = urllib.urlopen(url)

                html_doc = f.read()
                soup = BeautifulSoup(html_doc)

                if soup.find(id="box1") == None:
                        print 'Verbo ' + verbo +' Inexistente!! Delete BD'
                        nao_encontrados.write('Verbo ' + verbo +' Inexistente!! Delete BD. \n')
                else:
                        #print (soup.find(id="box1").h4.string)
                        print 'Verbo '+ verbo + ' Ok na base do Aurelio'
                        encontrados.write('Verbo '+ verbo + ' Ok na base do Aurelio. \n')

        nao_encontrados.close()
        encontrados.close()
        db.close()

except Exception, e:
        print 'Erro ao connectar no BD ' + e.message
else:
        pass
finally:
        pass