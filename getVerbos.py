# coding: utf-8

import urllib
from bs4 import BeautifulSoup
import codecs
import MySQLdb
import types
import re
from smtplib import SMTP
from smtplib import SMTPException
from email.mime.text import MIMEText
from unicodedata import normalize 

#'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'
arrayLetras = ('z')

def enviaEmail(texto):
    sender = 'linux.soares@gmail.com'
    receivers = ['linux.soares@gmail.com']
    subject = 'Verbos - ConjugVerbos'
    texto = texto.upper()
    
    message= """
        Titulo: %s

        Mensagem: %s
    """ % (subject, texto)

    try:
        session = SMTP('smtp.gmail.com',587)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login(sender,'password')
        session.sendmail(sender,receivers,message)
        session.quit()      
    except SMTPException as e:
        print "Error: unable to send email" + e.message

def remover_acentos(txt, codif='utf-8'):
    return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')

def usarReplace(palavra):
    palavra = palavra.replace('não', '').replace('para ', '').replace('eu','').replace('voc','').replace(' ele/ela','').replace('vocs','').replace('tu','').replace('vs','').replace('no','').replace('ns','').replace('eles/elas','').replace('ele/ela','').replace(' s','').replace(' ','').replace('ês', '').replace('vós', '').replace('nós', '')
    pattern = re.compile('(ê)$')
    return  re.sub(pattern, '', palavra)


def getConvertObjectSoup(url, codin='utf-8'):
    f = urllib.urlopen(url)

    html_doc = f.read()
        
    return BeautifulSoup(html_doc, from_encoding=codin)

def getVerbos():
    verbos = file('verbos.txt', 'w')
    palavras = []
         
    try:
         
        for i in arrayLetras:
            url = 'http://www.achando.info/verbos/conjugar/dicionario-'+i+'.html'

            soup = getConvertObjectSoup(url)

            print i
            if soup.find_all('li') == []:
                for s in soup.find_all('td', text=True):
                                        #+ ' - ' + s.string
                    if s.string and s.string != None and s.string != '':
                        #print s.string
                        palavras.append(s.string.encode('utf-8')  + '\n')
            else:
                for a in soup.find_all('li'):             
                    soup = getConvertObjectSoup(a.find('a')['href'])
                                        
                                        #print soup
                                        #verbos.write(url.encode('ascii', 'ignore') + '\n')
                    for s in soup.find_all('td', text=True):
                                                #+ ' - ' + s.string
                        if s.string and s.string != None and s.string != '':
                                                        #print s.string.encode('utf-8')
                            palavras.append(s.string.encode('utf-8')  + '\n')
                                          
                                                                                                                                                               
        verbos.writelines(palavras)
        verbos.close()
        return palavras
    except Exception, e:
        erro = 'Erro ao executar getVerbos verbos: ' + e.message
        enviaEmail(erro)
        print erro
    else:
        pass
    finally:
        pass

def validaVerbos(lista):
    #cursor MySQL
    db = MySQLdb.connect(host='localhost' , port=3306 ,user='root', passwd='', db='verbos', use_unicode=1, charset='utf8')
    cursor = db.cursor()
    try:
        for i in sorted(lista):
            if i > 0 and i:
                url = remover_acentos('http://www.dicionariodoaurelio.com/'+i.strip()+'.html')
                
                soup = getConvertObjectSoup(url)
                #print soup.find(id="box1")
                if soup.find(id="box1") is None and soup.find(id="box1") is False:
                    print 'Verbo ' + i.strip()+' Inexistente!! Delete BD'
                    lista.remove(i)
                else:
                                    #print (soup.find(id="box1").h4.string)
                    #print 'Verbo '+ str(i.strip()) + ' Ok na base do Aurelio'
                    print 'Insert '+str(i.strip())
                    sql = 'insert into verbos (nome) values ("'+ str(i.strip()) + '")'
                    db.commit()
                    cursor.execute(sql)
            else:
                print 'None'
        cursor.close()
        return sorted(lista)                

    except Exception, e:
        erro = 'Erro ao executar validaVerbos verbos: ' + e.message
        enviaEmail(erro)
        print erro
    else:
        pass
    finally:
        pass
                
def getVerbosConjugados(listaVerbos):
    count = [1, 3, 2]
    contador = 0
    num = 0
    valida = [4, 7, 10, 13, 17]
    count_valida = 0
    #cursor MySQL
    db = MySQLdb.connect(host='localhost' , port=3306 ,user='root', passwd='', db='verbos', use_unicode=1, charset='utf8')
    cursor = db.cursor()

    try:
        for verbo in listaVerbos:
            print 'http://www.conjuga-me.net/verbo-'+verbo
            soup = getConvertObjectSoup('http://www.conjuga-me.net/verbo-'+verbo, 'iso8859-1')
            
            for s in soup.find_all('td', attrs = { 'class' : 'output'}):
                if s.text and s.text != None and s.text != '' and s.text != '\t' and s.text != '\n' and s.text != ' ' and s.text != '–' and s.text != ' - ':
                    palavra = usarReplace(s.text.encode('utf-8'))
                    cursor.execute('select id_verbos from verbos where nome = "'+ verbo.strip() +'"')
                    if palavra and re.search('[a-zA-Z]', palavra):
                        id_verbo = cursor.fetchone()
                        if count[0] == 10 and count_valida in valida:
                            print 'id_verbo: '+ str(id_verbo[0]) + ' - ' + palavra
                            sql = 'insert into conjulgacao_verbal (nome_conjulgacao, id_tempo_verbal, id_verbo) value (%s, %s, %s)'
                            db.commit()
                            cursor.execute(sql, (palavra, count[num], id_verbo[0]))    
                        if count[0] != 10 and count_valida not in valida:
                            print 'id_verbo: '+ str(id_verbo[0]) + ' - ' + palavra
                            sql = 'insert into conjulgacao_verbal (nome_conjulgacao, id_tempo_verbal, id_verbo) value (%s, %s, %s)'
                            db.commit()
                            cursor.execute(sql, (palavra, count[num], id_verbo[0]))    


                    num += 1
                    if num == 3:
                       num = 0
                    contador += 1
                    if contador == 18:
                        count = [4, 6, 5]
                    if contador == 36:
                        count = [7, 9, 8]
                    if contador == 54:
                        count = [10, 10, 10]
                    if contador == 72:
                        contador = 0
                        count = [1, 3, 2]

                    if count[0] == 10:
                        count_valida += 1
                    if  count_valida > 17:
                        count_valida = 0


        cursor.close() 
    except Exception, e:
        erro = 'Erro ao executar getVerbosConjugados verbos: ' + e.message
        enviaEmail(erro)
        print erro
    else:
        pass
    finally:
        pass                

def main():
    verbos = getVerbos()
    verbosValidados = validaVerbos(verbos)
    getVerbosConjugados(verbosValidados)

    enviaEmail('Todos os verbos foram inseridos com SUCESSO! - TESTE')

if __name__ == '__main__':
    main()