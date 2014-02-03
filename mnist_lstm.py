#!/usr/bin/python 
'''Script to run the RNNLIB library on MNIST dataset with single character output strings in Sequence classification mode . This is an example that uses one timestep as one column read from the image . We will stack together 2 images here so making 56 timesteps for one image for the LSTM to train on   '''

import netcdf_helpers
from scipy import * 
import cPickle 
from optparse import OptionParser
import numpy 

parser = OptionParser() 
parser.add_option("-p" , "--pad", action="store_true" , dest="pad" , help="pad image to 28*28 pixels")
parser.add_option("-d", "--dummy", action="store_true", dest="dummy", help="use dummy labels?")
parser.add_option("-c", "--chars", action="store_true", dest="chars", help="build char dataset?")

#parse command line options 
(options , args ) = parser.parse_args() 
if (len(args)<2):
     print "usage: -options input_filename output_filename"
     print options 
     sys.exit(2) 
labels = ['0','1','2','3','4','5','6','7','8','9'] 
inputFilename=args[0] 
ncFilename=args[1] 

#inputFilename is basically a pickled file that contains all the MNIST data 
#it can be mnist_train.pkl , mnist_valid.pkl , mnist_test.pkl 

print options 
print "Input Filename : " , inputFilename 
print "Data Filename : " , ncFilename 

seqDims=[] 
seqLengths=[] 
targetStrings=[] 
seqTags=[] 
filenames=[] 
print "Reading Data ... " 
f = open(inputFilename, "rb") 
inputvals , targetvals = cPickle.load(f) 
ndatavals = inputvals.shape[0] 
  
 
for n in range(ndatavals):
    label = targetvals[n] 
    targetStrings.append(str(label))  #remember to change labels to strings
    seqTags.append(str(n))
    dims=[28]    #no of the timesteps that are there in one sequence  
    seqLengths.append(28)
    seqDims.append(dims) 
     
 
print "Allocating input array ..." 
inputs=[]
print shape(inputs)
 
for i in range(ndatavals):
    for j in range(28):
      inp = inputvals[i][j*28:(j+1)*28]
      inputs.append(inp)


      
#inputs = numpy.array(inputs) 
print len(labels) , "labels:" 
print labels 
#create a new .nc file 
file = netcdf_helpers.NetCDFFile(ncFilename,'w') 

#create the netcdf dimensions 
netcdf_helpers.createNcDim(file,'numSeqs' , len(seqLengths))
netcdf_helpers.createNcDim(file,'numTimesteps' , len(inputs))
netcdf_helpers.createNcDim(file,'inputPattSize',len(inputs[0]))
netcdf_helpers.createNcDim(file,'numDims',1)
netcdf_helpers.createNcDim(file,'numLabels' , len(labels))

#create the variables 
netcdf_helpers.createNcStrings(file,'seqTags',seqTags,('numSeqs','maxSeqTagLength'),'sequence tags')
netcdf_helpers.createNcStrings(file,'labels',labels,('numLabels','maxLabelLength'),'labels')
netcdf_helpers.createNcStrings(file,'targetStrings',targetStrings,('numSeqs','maxTargStringLength'),'target strings')
netcdf_helpers.createNcVar(file,'seqLengths',seqLengths,'i',('numSeqs',),'sequence lengths')
netcdf_helpers.createNcVar(file,'seqDims',seqDims,'i',('numSeqs','numDims'),'sequence dimensions')
netcdf_helpers.createNcVar(file,'inputs',inputs,'f',('numTimesteps','inputPattSize'),'input patterns')

#write the data to disk
print "closing file", ncFilename
file.close()
