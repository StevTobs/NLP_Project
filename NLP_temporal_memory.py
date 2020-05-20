# # uncomment if running from colab
# !pip install https://github.com/PyThaiNLP/pythainlp/archive/dev.zip
# !pip install epitran
# !pip install sklearn_crfsuite

import json
import pythainlp
import pandas as pd
import numpy as np
from pythainlp.tag.named_entity import ThaiNameTagger
from datetime import date, datetime

NameEntity = ThaiNameTagger()
from numpy.random import randn
np.random.seed(101) 
pythainlp.__version__

class NLP_THAI_PEA:

    def __init__(self, message, JS_timestamp_ms, userId, path):
        self.timestamp_s = JS_timestamp_ms / 1000
        self.txt_path = path
        self.word_dmm = NameEntity.get_ner(message)
        print("userId: ", userId)
        print("Recorded Data\n", self.display_recorded() )
        pythainlp.__version__
        print("NLP Thai PEA is ready!!")
        print("------------------------------------------------------------------------------")

    def concadDf(self, df1, df2):
        frames = [df1, df2]
        result = pd.concat(frames)
        return result

    def getPronoun(self):
        word_Pron = []
        
        for i in range( len( self.word_dmm) ):
            if 'PRON' in self.word_dmm[i][1] :
                word_Pron.append(self.word_dmm[i][0])

        return word_Pron 

    def getAction(self ):
        word_verb = []
        for i in range( len( self.word_dmm ) ):
            if self.word_dmm[i][1] == 'VERB':
                if( self.word_dmm[i][2] == 'O' ):
                    word_verb.append(self.word_dmm[i][0])

        return word_verb  

    def getTheme(self ):
        word_theme = []
        check_Last_Noun = False
        for i in range( len( self.word_dmm ) ):
            if len( self.word_dmm[i]) > 1 and check_Last_Noun:
                if (self.word_dmm[i][1] == 'NOUN'):
                    if(self.word_dmm[i][2] == 'O' ):
                        word_theme[-1] = word_theme[-1] + self.word_dmm[i][0]
                        
            
                        
                        
            if (self.word_dmm[i][1] == 'NOUN'): 
                if( self.word_dmm[i][2] == 'O' ): 
                    word_theme.append(self.word_dmm[i][0])
                    check_Last_Noun = True
                    if len( word_theme) > 1 and word_theme[-1] in  word_theme[-2] :
                        del word_theme[-1]
            
                    
            else :
                check_Last_Noun = False
                

        return word_theme 

    def getLocation(self ):
        #print(len(word_dmm))
        word_loc = []
        check_Last_B_location = False
        for i in range( len( self.word_dmm ) ):

            if len( self.word_dmm[i]) > 1 and check_Last_B_location :
                if( self.word_dmm[i][2] == 'I-LOCATION'):
                    word_loc[-1] = word_loc[-1] + self.word_dmm[i][0]
                    
                
            if self.word_dmm[i][2] == 'B-LOCATION':
                word_loc.append(self.word_dmm[i][0])
                
                check_Last_B_location = True
            else :
                check_Last_B_location = False
            
            if self.word_dmm[i][2] == 'I-LOCATION':
                check_Last_B_location = True

        return word_loc

    def getTemporal( self ):
        #print(len(word_dmm))
        word_date = []
        check_Last_B_date = False
        for i in range( len( self.word_dmm ) ):

            if len( self.word_dmm[i]) > 1 and check_Last_B_date :
                if( 'I-DATE' in self.word_dmm[i][2] ):
                    word_date[-1] = word_date[-1] + self.word_dmm[i][0]

            if 'B-DATE' in self.word_dmm[i][2] :
                word_date.append(self.word_dmm[i][0])
                
                check_Last_B_date = True
            else :
                check_Last_B_date = False
            
            if 'I-DATE' in self.word_dmm[i][2] :
                check_Last_B_date = True

        return word_date

    def getTime( self ):
        timestamp = []
        timestamp.append( str( date.fromtimestamp(int( self.timestamp_s))  ))
        # print("Date =", timestamp)

        return  timestamp

    def reportTable(self):
        # pd.DataFrame.from_dict({'a': a, 'b': b}, orient='index').T
        df_res = pd.DataFrame.from_dict({ 'Agent':  self.getPronoun(  ), 
                                         'Action':  self.getAction( ) ,
                                          'Theme':  self.getTheme( )  ,
                                       'Location':  self.getLocation( ), 
                                       'Temporal':  self.getTemporal(  ),
                                        'Timestamp':  self.getTime(  )  }, orient='index').T
        return df_res

    def reportDict(self):
        # pd.DataFrame.from_dict({'a': a, 'b': b}, orient='index').T
        dict_dmm = { 'Agent'     :  self.getPronoun(  ), 
                    'Action'    :  self.getAction( ) ,
                    'Theme'     :  self.getTheme( )  ,
                    'Location'  :  self.getLocation( ), 
                    'Temporal'  :  self.getTemporal(  ),
                    'Timestamp' :  self.getTime(  )  }


        dict_res= { 'E0000' : dict_dmm}
        return dict_res   

    def getCurrentDict(self):
        # pd.DataFrame.from_dict({'a': a, 'b': b}, orient='index').T
        dict_dmm = { 'Agent'     :  self.getPronoun(  ), 
                    'Action'    :  self.getAction( ) ,
                    'Theme'     :  self.getTheme( )  ,
                    'Location'  :  self.getLocation( ), 
                    'Temporal'  :  self.getTemporal(  ),
                    'Timestamp' :  self.getTime(  )  }
        return dict_dmm 

    def loadTxt(self, txt_path):
        with open(txt_path ) as json_file:
            data = json.load(json_file)
        return data

    def display_recorded (self ) :
        
        with open(self.txt_path ) as json_file:
            data = json.load(json_file)

        return data

    def getEventID(self, dict_dmm ):

        return sorted( dict_dmm.keys())[-1]

    def updateEventID(self, curr_dict):
      
        last_key =  self.getEventID(curr_dict) 
        # print("last key",last_key )
        new_key = str(int( '1'+last_key[1:]  ) + 1)
        res_key = 'E'+ new_key[1:] 
        return res_key 

    def updateRecorded (self) :
        data = self.loadTxt(self.txt_path)
        ID_new = self.updateEventID( data )

        data[ID_new]=[]
        data[ID_new].append( self.getCurrentDict() )
            #save
        with open(self.txt_path , 'w') as outfile:
            json.dump(data, outfile)

        print("The record has been updated to ", self.txt_path)

    def clear_file(self):
        data = {}
        ID = '0000'
        data[ID]  = ['initial']

        with open(self.txt_path , 'w') as outfile:
            json.dump(data, outfile)
        
        print("Data has been deleted!!")


if __name__ == "__main__":
    userId = "U99648c35cb84f0ab7ca8e22bf2b375f7"
    JS_timestamp_ms = 1589920755744
    message = "ขออนุญาตสอบถามเรื่องติดตั้งหม้อแปลงที่จังหวัดนนทบุรีหน่อยครับ พรุ่งนี้จะต้องมีงานเลี้ยงด่วน"

    # txt_file = 'json_recored_file.txt'
    txt_path = r"G:\\CODE\\Git\\NLP_Project\\json_recored_file.txt"
    NLP = NLP_THAI_PEA(message  ,  JS_timestamp_ms , userId , txt_path )
    # NLP.updateRecorded()
    NLP.display_recorded()
    # print( NLP.get_previous_recorded(  txt_file) )
    # NLP.save_recorded ()
    

 
    