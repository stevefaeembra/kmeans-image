'''
Created on 10 May 2013

@author: steven
'''
import unittest
from kmeans.kmeans import KMeans
from PIL import Image

class Test(unittest.TestCase):


    def setUp(self):
        self.km = KMeans()

    def testIsRGBA(self):
        fi=open("Mona_Lisa.jpg","r")
        isRGBA = self.km.testRGBA(Image.open(fi))
        fi.close()
        assert not isRGBA
        
    def testProcessFile(self):
        fi=open("Mona_Lisa.jpg","r")
        fo=open("result.jpg","w")
        self.km.process(fi,fo)
        fo.close()
        fi.close()
        
        totalnumberofpixels = self.km.im.size[0]*self.km.im.size[1]
        assert len(self.km.pixels) == totalnumberofpixels
        for x in self.km.pixels:
            #print x
            r,g,b,centroid = x
            assert r in range(0,256)
            assert g in range(0,256)
            assert b in range(0,256)
            assert centroid in range(0,self.km.numbercentroids)
        
        totpixels=0
        assert len(self.km.clusters.keys())==self.km.numbercentroids
        for x in self.km.clusters.keys():
            assert len(self.km.clusters[x])>0
            totpixels+= len(self.km.clusters[x])
            print "Cluster %d has %d elements" % (x,len(self.km.clusters[x]))
        assert totpixels == totalnumberofpixels
        
        for x in range(0,len(self.km.means)):
            r,g,b = self.km.means[x]
            assert r in range(0,256)
            assert g in range(0,256)
            assert b in range(0,256)
            print "Cluster %d is centered at (%d,%d,%d)" % (x,r,g,b)

if __name__ == "__main__":
    unittest.main()