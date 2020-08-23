import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
import datetime
#from ElementTree_pretty import prettify

def createTMX(source_file, output_file, srclang, targetlang, adminlang='en', segtype='phrase', datatype='PlainText', oEncoding='UTF-8', source_filter_delimiter=","):


    generated_on = str(datetime.datetime.now())

    root = Element('tmx')
    root.set('version', '1.4')

    header = SubElement(root, 'header')
    header.set('creationtool','')
    header.set('creationtoolversion', '')
    header.set('segtype', segtype)
    header.set('o-tmf', '')
    header.set('adminlang', adminlang)
    header.set('srclang', srclang)
    header.set('datatype', datatype)
    header.set('o-encoding', oEncoding)


    body = SubElement(root, 'body')

    with open(source_file) as f:
        reader = csv.DictReader(f, delimiter=source_filter_delimiter)
        for row in reader:
            print("row:", row)
            tu = SubElement(body, 'tu')
            
            tuv_src = SubElement(tu, 'tuv')
            tuv_src.set('xml:lang', srclang)
            seg_src = SubElement(tuv_src, 'seg')
            seg_src.text = row[srclang].strip()
            
            tuv_target = SubElement(tu, 'tuv')
            tuv_target.set('xml:lang', targetlang)
            seg_target = SubElement(tuv_target, 'seg')
            seg_target.text = row[targetlang].strip()

    ElementTree(root).write(output_file)
