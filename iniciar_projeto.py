#! /usr/bin/python
# -*- coding: latin-1 -*-

import os
import shutil
import platform

so = platform.system()

project = raw_input('USO: \t\a Insira o nome do projeto\n')
print 'Projeto: ',project
os.mkdir('projeto_'+project) 
os.chdir('projeto_'+project) 

#criando e configurando virtual env
#os.system('mkvirtualenv ve_',project)
#os.system('workon ve_',project)
#os.system('pip install django')

try:
	print 'criando e configurando projeto'
	criar = 'django-admin.py startproject '+project
	os.system(criar)
	os.chdir(project)
	
	print 'transformando o settings em modulo'
	os.mkdir('settings')
	shutil.move('settings.py', 'settings/production.py')

	if so != 'Windows':
		os.chdir('settings')
		os.system('echo > __init__.py')
		os.system('echo > stage.py')
		os.system('echo > development.py')
		#print os.getcwd()
		os.system('echo from production import *  >  stage.py')
		os.system('echo from production import *  >  development.py')
		os.system('echo import os > __init__.py')
		os.system('echo "global_settings = os.path.join(os.path.dirname(__file__), development.py)" >> __init__.py')
		os.system('echo "execfile(global_settings) >> __init__.py')

		print 'criando e configurando a aplicacao'
		os.chdir('..')
		os.system('django-admin.py startapp core')
		os.chdir('core')
		os.system('mkdir static')
		os.chdir('static')
		os.system('mkdir media')
		os.chdir('..')
		#os.chdir('core')
		os.system('mkdir templates')
		os.chdir('templates')
		os.system('mkdir core')
		os.chdir('core')
		os.system('mkdir static')
		os.chdir('..')
		os.chdir('..')
		os.chdir('static')
		os.system('mkdir css')
		os.system('mkdir img')
		os.system('mkdir js')
		
		print 'transformando os testes em modulo'
		os.chdir('..')
		
		os.system('mkdir tests')
		#os.system('mv core/tests.py core/tests/simple_test.py')
		shutil.move('tests.py', 'tests/simple_test.py')
		os.chdir('tests')
		os.system('echo > __init__.py')
		os.system('echo "from .simple_test import *" >> __init__.py')
		
		print 'criando o arquivo de requirements'
		os.chdir('..')
		os.chdir('..')
		os.system('pip freeze | grep -i django >> requirements.txt')
		
		print 'configurando o repositorio do git'
		#os.system('git init')
		#os.system('echo "*.pyc" > .gitignore')
		#os.system('git add .')
		#os.system('git commit -m "first commit :)"')

		print 'iniciando o servidor'
		#os.system('python ../manage.py runserver')
	else:
		os.chdir('settings')
		os.system('echo > __init__.py')
		os.system('echo > stage.py')
		os.system('echo > development.py')
		#print os.getcwd()
		os.system('echo from production import *  >  stage.py')
		os.system('echo from production import *  >  development.py')
		os.system('echo import os > __init__.py')
		os.system('echo global_settings = os.path.join(os.path.dirname(__file__), development.py) >> __init__.py')
		os.system('echo execfile(global_settings) > __init__.py')
		
		#criando e configurando a aplicacao
		os.chdir('..')
		os.system('django-admin.py startapp core')
		os.chdir('core')
		os.system('mkdir static')
		os.chdir('static')
		os.system('mkdir media')
		os.chdir('..')
		#os.chdir('core')
		os.system('mkdir templates')
		os.chdir('templates')
		os.system('mkdir core')
		os.chdir('core')
		os.system('mkdir static')
		os.chdir('static')
		os.system('mkdir css')
		os.system('mkdir img')
		os.system('mkdir js')
		
		#transformando os testes em modulo
		os.chdir('..')
		print os.getcwd()
		os.chdir('..')
		os.chdir('..')
		print os.getcwd()
		os.system('mkdir tests')
		#os.system('mv core/tests.py core/tests/simple_test.py')
		shutil.move('core/tests.py', 'core/tests/simple_test.py')
		os.system('echo from .simple_test import * > core\tests\__init__.py')
		
		#criando o arquivo de requirements
		#os.system('pip freeze | grep -i django > requirements.txt')
		
		#configurando o repositorio do git
		#os.system('git init')
		#os.system('echo "*.pyc" > .gitignore')
		#os.system('git add .')
		#os.system('git commit -m "first commit :)"')

		#iniciando o servidor
		os.system('python ../manage.py runserver')
		
except:
	print 'Projeto	 já existem!'
	
	





