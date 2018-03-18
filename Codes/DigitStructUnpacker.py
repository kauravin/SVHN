import h5py
import time
class DigitStructWrapper:
    """
    Wrapper for the H5PY digitStruct files from the SVHN dataset
    Creates an array of Dictionaries containing filename and boundingBoxes parameter
    Adapted from https://github.com/thomalm    
    
    """
    def __init__(self,path):
        #reading the file to whom we will pass appropriate references to get the values
        self.inf=h5py.File(path,'r')

        #here we are getting the HDf5 object references in one go, which we will give to self.inf to access individual elements
        self.digitStructName=self.inf['digitStruct']['name']
        self.digitStructBbox=self.inf['digitStruct']['bbox']
    
    def get_name(self,n):
        """
        Returns the name of the nth image that we are trying to read and work on. Ex: "1.png" etc.
        """
        #print([chr(c) for c in self.inf[self.digitStructName[n][0]].value])
        return "".join([chr(c) for c in self.inf[self.digitStructName[n][0]].value])
    def get_attribute(self,attr):
        """
        This function returns a list of the attribute
        """
        if (len(attr)>1):
            attr=[self.inf[attr.value[j].item()].value[0][0] for j in range(len(attr))]
        else:
            attr=[attr.value[0][0]]
        #print(self.inf[attr.value[j].item()].value[0][0] for j in range(len(attr)))
        return attr
    def get_bbox(self,n):
        """
        this function returns a dictionary which consists the list of all the attributes of the bounding boxes of the nth image
        """
        bbox={}
        bb=self.digitStructBbox[n].item()
        bbox['height']=self.get_attribute(self.inf[bb]['height'])
        bbox['width']=self.get_attribute(self.inf[bb]['width'])
        bbox['label']=self.get_attribute(self.inf[bb]['label'])
        bbox['left']=self.get_attribute(self.inf[bb]['left'])
        bbox['top']=self.get_attribute(self.inf[bb]['top'])
        #print(bbox['height'])
        return bbox
    def get_item(self,n):
        """
        This function returns a packed version of the bbox dictionary and filename in a bigger dictionary
        """
        #print("Inside get item")
        packFilenameNdBbox=self.get_bbox(n)
        packFilenameNdBbox['filename']=self.get_name(n)
        #print(packFilenameNdBbox)
        return packFilenameNdBbox
    
    def unpack(self):
        """
        This function returns list of all the dictionaries containing the information of individual Filenames and Bboxes
        """
        print("inside the unpack function")
        return ([self.get_item(i) for i in range (len(self.digitStructName))])
   
    def unpack_all(self):
        """
        This function returns the array of dictionaries of each input image...kind of unpacking the whole input provide
        """
        packedData=self.unpack()
        structCnt = 1
        finalDictList=[]
        for i in range(len(packedData)):
            #print('Unpacking Image No:'+str(i))
            item={'filename':packedData[i]['filename']}
            DictList=[]
            for j in range(len(packedData[i]['height'])):
                dictOfAttributes={}
                dictOfAttributes['height']=packedData[i]['height'][j]
                dictOfAttributes['width']=packedData[i]['width'][j]
                dictOfAttributes['left']=packedData[i]['left'][j]
                dictOfAttributes['top']=packedData[i]['top'][j]
                dictOfAttributes['label']=packedData[i]['label'][j]
                DictList.append(dictOfAttributes)
            item['boxes']=DictList
            structCnt = structCnt + 1
            finalDictList.append(item)
        return finalDictList