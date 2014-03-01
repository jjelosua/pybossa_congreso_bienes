#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script is used to split the deputies declarations into individual pages
# to be treated as tasks inside the crowdcrafting app

from urllib2 import Request, urlopen
from PyPDF2 import PdfFileWriter, PdfFileReader
from StringIO import StringIO
import csv

if __name__ == "__main__":
    rownum = 0
    csvfile = open( "data/dip_declaration_pages.csv", "wb" )
    writer = csv.writer( csvfile )
    writer.writerow(["id_legislatura","id_diputado","nombre","fecha","page","pdffile"])
    with open('data/dip_declaration_DB.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            #Skip header
            if rownum == 0:
                header = row
                rownum += 1
                continue
            url = row[4]
            remoteFile = urlopen(Request(url)).read()
            memoryFile = StringIO(remoteFile)
            inputpdf = PdfFileReader(memoryFile)
            for i in xrange(inputpdf.numPages):
                output = PdfFileWriter()
                output.addPage(inputpdf.getPage(i))
                pdf = 'data/pdf/%s_%s_%s-page%s.pdf' % (row[0],row[1],row[3], i+1)
                pdffile = open(pdf, "wb")
                output.write(pdffile)
                pdffile.close()
                writer.writerow([row[0],row[1],row[2],row[3],i+1,pdf])
        csvfile.close()    
                
            
            
