# -*- coding: UTF-8 -*-
# PDF spell checker
# Kero2375

import sys
try:
	import textract
	import language_check
	import re
except ImportError:
    sys.exit("Please install textract and language-check before (pip3 install *). Or mabe you're not using python3.")

try:
	nf = str(sys.argv[1]) 
except IndexError:
	sys.exit("Please add filename")	

# RULES SET:
rules = [
        'MORFOLOGIK_RULE_IT_IT', # errori battitura
        'COMMA_PARENTHESIS_WHITESPACE', # spazi punteggiatura
        'WHITESPACE_PUNCTUATION', # spazi punteggiatura
        'GR_04_002', # forme abbreviate
        'ST_03_001', # ad / ed ..
        'ST_02_001', # frase troppo lunga
        'GR_05_002', # inizio con congiunzione
        'ER_01_001', # ha / a ...
        'ST_01_005', # suggerimenti traduzione dall'inglese
        'UPPERCASE_SENTENCE_START', # inizio minuscola
        'GR_10_001' # tempi verbali
        ]

# IGNORED WORDS:
ignore = [
        'Discalzi', 
        'Cannavò', 
        'Bari', 
        'Biolcati', 
        'Rinaldi', 
        'Piran',
        'Vardanega',
        'Cardin',
        'Zucchetti',
        'Grafana'
        ]
	
print ('selected file: ' + nf)
text = textract.process(nf, method='pdftotext') # extract text from pdf
text = text.decode('utf-8')

print('loading...')
tool = language_check.LanguageTool('it-IT') # language
matches = tool.check(text) # all errors
file = open('log.txt', 'w') # log file

for m in matches:
    if(m.ruleId in rules): # print just selected rules
	# avoid reporting '. .' (eg. in the index)
        if (m.ruleId == 'COMMA_PARENTHESIS_WHITESPACE'): 
            if('. .' not in str(m)):
                file.write(str(m) + '\n\n')
	
	# if any ignored word into message text, don't print it
        elif (m.ruleId == 'MORFOLOGIK_RULE_IT_IT'):
            t=0
            for i in ignore:
                if(i in str(m)):
                    t = 1
            if(t == 0):
                file.write(str(m) + '\n\n')
	
	# print everything else
        else:
            file.write(str(m) + '\n\n')
		       
file.close()
print('all done! check the file log.txt')
