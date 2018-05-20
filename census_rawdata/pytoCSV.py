#!/usr/bin/python

import sys,re,csv,numpy

infile = sys.argv[1]
try:
    inputdata = __import__(infile.split('.py')[0])
except Exception,e:
    print >>sys.stderr,e
    print >>sys.stderr,'First parameter must be python structure of input data'
    sys.exit(1)

outfile = infile.split('.py')[0] + '.csv'
outputdata = open(outfile,'wb')

output = csv.writer(outputdata, quoting=csv.QUOTE_ALL)

structure = infile.split('.py')[0]
structdata = eval('inputdata.'+structure)
columns = structure + 'cols'
columnList = eval('inputdata.'+columns)
output.writerow(columnList)
for key in structdata.keys():
    for count in range(0,len(structdata[key][0])):
        output.writerow([structdata[key][0][count]] + numpy.array(structdata[key][1][count,:]).tolist())
