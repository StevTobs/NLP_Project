# # uncomment if running from colab
# !pip install https://github.com/PyThaiNLP/pythainlp/archive/dev.zip
# !pip install epitran
# !pip install sklearn_crfsuite


import pythainlp
import pandas as pd
import numpy as np
from pythainlp.tag.named_entity import ThaiNameTagger

NameEntity = ThaiNameTagger()
from numpy.random import randn
np.random.seed(101) 
pythainlp.__version__

class NLP_THAI_PEA:

    def __init__(self, inputTxt):
        self.word_dmm = NameEntity.get_ner(inputTxt)
        pythainlp.__version__
        print("NLP Thai PEA is ready!!")

    def concadDf(self, df1, df2):
        frames = [df1, df2]
        result = pd.concat(frames)
        return result


    def getPronoun(self ):
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
    def reportTable(self):
        # pd.DataFrame.from_dict({'a': a, 'b': b}, orient='index').T

        df_res = pd.DataFrame.from_dict({ 'Agent':  self.getPronoun(  ), 
                                         'Action':  self.getAction( ) ,
                                          'Theme':  self.getTheme( )  ,
                                       'Location':  self.getLocation( ), 
                                       'Temporal':  self.getTemporal(  ) }, orient='index').T
        return df_res
        


if __name__ == "__main__":
    NLP = NLP_THAI_PEA("ทำงานแม้งตลอด")
    NLP.reportTable()
    print("Fuck")