import xml.etree.ElementTree as ET

import os
import time
import string
import sys


def process(text, caratteri):
    text = text.lower()
    text = text.replace('0',' zero ')
    text = text.replace('1',' one ')
    text = text.replace('2',' two ')
    text = text.replace('3',' three ')
    text = text.replace('4',' four ')
    text = text.replace('5',' five ')
    text = text.replace('6',' six ')
    text = text.replace('7',' seven ')
    text = text.replace('8',' eight ')
    text = text.replace('9',' nine ')
    text = text.replace('$',' dollars ')
    char_to_remove = str.maketrans({a:' ' for a in caratteri})
    text = text.translate(char_to_remove)
    text = text.replace('   ', ' ')
    text = text.replace('  ', ' ')
    return text

i = 0
children=['Article','ArticleTitle','Abstract','AbstractText']
punteggiatura='!\"\'()*+,-./:;<=>?@[]^_{|}&%'
cartella_input = sys.argv[1]
cartella_output = sys.argv[2]
lista_file = sorted(os.listdir(path=cartella_input))
file_totali = len(lista_file)

print('Verranno processati ', file_totali, ' file .xml')
tempo_iniziale = time.time()

for doc in lista_file:
    with open(cartella_input+doc,'r', encoding='utf-8') as xml_file:
        j=0
        nome_doc = doc.replace('.xml','')
        #os.mkdir(cartella_output+nome_doc)
        nome=cartella_output+ nome_doc
        f = open(nome + '.txt', 'w', encoding='utf-8')

        for event, elem in ET.iterparse(xml_file):
            temp=list()
            if elem.tag == 'MedlineCitation':
                #pmid = elem.find('PMID')
                article = elem.find('Article')
                if article != None:
                    article_title = article.find('ArticleTitle')
                    if article_title != None:
                        if article_title.text != None:
                            f.write(process(article_title.text, punteggiatura) + '\n')
                            abstract = article.find('Abstract')
                            if abstract != None:
                                testo_abstract=''
                                for paragrafi in abstract.iter('AbstractText'):
                                    if paragrafi.text != None:
                                        testo_abstract = testo_abstract + paragrafi.get('Label','') + ' ' + paragrafi.text + ' '                    
                                f.write(process(testo_abstract, punteggiatura)+'\n')
                                testo_abstract=''
                                abstract.clear()
                            j+=1
                        article_title.clear()
                    article.clear()
                #pmid.clear()
                elem.clear()
                for child in temp:
                    child.clear()
            elif elem.tag not in children and elem.tag != 'MedlineCitation':
                elem.clear()
            else:
                temp.append(elem)
        f.close()
    i=i+1
    perc = ((i)/file_totali)*100
    print('Processati ', j, ' articoli in ', doc, ', processo completo al ', perc, '%' )

tempo_finale = time.time()
print('Processati ', i, ' documenti in ', tempo_finale - tempo_iniziale, ' secondi.')
