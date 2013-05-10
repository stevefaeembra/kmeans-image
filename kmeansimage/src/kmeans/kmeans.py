'''
Created on 10 May 2013

@author: steven
'''

from PIL import Image
from random import randint
import math

class KMeans(object):
    
    def __init__(self,iterations=12):
        self._reset()
        self.iterations = iterations
        
    def _reset(self):
        self.pixels=[] # list of (r, g, b, centroid)
        self.clusters={} # key=centroid #, value = list of (r,g,b)
        self.rgb={} # key=(r,g,b), value = centroid #
        self.means=[] # list of N centroids in (r,g,b) format 
        
    def process(self,input_file_like_object,output_file_like_object,centroids=4):
        self._reset()
        self.im = Image.open(input_file_like_object)
        self.numbercentroids = centroids
        self.isRGBA = self.testRGBA(self.im)
        self.getpixels()
        self.initialAssignmentToCentroids()
        self.initialAssignmentOfCentroidColours()
        
        for q in range(0,self.iterations):
            print "Iteration %d" % q
            self.assign()
            self.reassigncentroids()
            self.updatecentroids()
            self._dumpClusterInfo()
        self.saveProcessedImage(output_file_like_object)
    
    def saveProcessedImage(self, file_like_object):
        ''' 
        save a copy of image with pixels rounded to their
        nearest centroid 
        '''
        w,h = self.im.size
        im2 = Image.new("RGB",self.im.size)
        for y in range(0,h):
            for x in range(0,w):
                if self.testRGBA(self.im):
                    r,g,b,a = self.im.getpixel((x,y))
                else:
                    r,g,b = self.im.getpixel((x,y))
                cent = self.rgb[(r,g,b)]
                newr,newg,newb = self.means[cent]
                # print "(%d,%d) -> (%d,%d,%d)" % (x,y,newr,newg,newb)
                im2.putpixel((x,y),(newr,newg,newb))
        im2.save(file_like_object)
        
    def testRGBA(self,img):
        try:
            r,g,b,a = img.getpixel((0,0))
            return True
        except:
            return False
        
    def getpixels(self):
        w,h = self.im.size
        for y in range(0,h):
            for x in range(0,w):
                if self.isRGBA:
                    r,g,b,a = self.im.getpixel((x,y))
                else:
                    r,g,b = self.im.getpixel((x,y))
                self.pixels.append((r,g,b,0))

    def initialAssignmentToCentroids(self):
        ''' assign each pixel to a randomly chosen centroid '''
        for x in range(0,len(self.pixels)):
            pix = self.pixels[x]
            r,g,b,centroid = pix
            centroid = randint(0,self.numbercentroids-1)
            self.pixels[x] = (r,g,b,centroid)
            if not centroid in self.clusters:
                self.clusters[centroid]=[(r,g,b)]
            else:
                self.clusters[centroid].append((r,g,b))
            self.rgb[(r,g,b)]=centroid    
            
    def initialAssignmentOfCentroidColours(self):
        ''' assign each centroid to a randomly chosen colour present in the image '''
        w,h = self.im.size
        for x in range(0,self.numbercentroids):
            randx = randint(0,w)
            randy = randint(0,h)
            if self.isRGBA:
                r,g,b,a = self.im.getpixel((randx,randy))
            else:
                r,g,b = self.im.getpixel((randx,randy))
            self.means.append((r,g,b))
            
    def assign(self):
        ''' 
        for each pixel, find which centroid is the closest to it using a Euclidean distance.
        '''
        print "Assigning pixels to closest centroids"
        self.newpixels=[]
        for x in range(0,len(self.pixels)):
            pix = self.pixels[x]
            r,g,b, centroid = pix
            mindist = 99999999999999999
            minix = 0
            for y in range(0,self.numbercentroids):
                rc,gc,bc=self.means[y]
                dist = math.sqrt(math.pow(r-rc,2.0)+math.pow(g-gc,2.0)+math.pow(b-bc,2.0))
                if (dist<mindist):
                    mindist = dist
                    minix = y
            #print "Reassigning (%d,%d,%d) to centroid %d" % (r,g,b,minix)
            self.newpixels.append((r,g,b,minix))
            self.rgb[(r,g,b)]=minix
        self.pixels = self.newpixels
    
    def reassigncentroids(self):
        '''
        for each pixel (r,g,b,centroid), reassign centroids
        '''
        print "Rebuilding set of centroid contents"
        self.clusters={}
        for x in range(0,len(self.pixels)):
            pix = self.pixels[x]
            r,g,b,centroid = pix
            if not centroid in self.clusters:
                self.clusters[centroid]=[(r,g,b)]
            else:
                self.clusters[centroid].append((r,g,b))
            self.rgb[(r,g,b)]=centroid
    
    def updatecentroids(self):
        ''' 
        for each centroid, work out its average (r,g,b) from the
        pixels in its cluster
        '''
        self.means=[]
        for x in range(0,self.numbercentroids):
            totr=0
            totg=0
            totb=0
            ct = 0
            for pix in self.clusters[x]:
                r,g,b = pix
                ct += 1
                totr += r
                totg += g
                totb += b
            avgr = totr / ct
            avgg = totg / ct
            avgb = totb / ct
            self.means.append((avgr,avgg,avgb))
            #print "Centroid %d moved to (%d,%d,%d)" % (x,avgr,avgg,avgb)
    
    def _dumpClusterInfo(self):
        for x in range(0,self.numbercentroids):
            r,g,b = self.means[x]
            clustpix = self.clusters[x]
            print "Cluster %d : (%d,%d,%d) - %d pixels" % (x,r,g,b,len(clustpix))
            