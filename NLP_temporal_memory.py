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

    def __init__(self):
        pass

    def concadDf(self, df1, df2):
        frames = [df1, df2]
        result = pd.concat(frames)
        return result


    def getPronoun(self,    word_dmm ):
        word_Pron = []
        for i in range( len( word_dmm ) ):
            if word_dmm[i][1] == 'PRON':
                word_Pron.append(word_dmm[i][0])

        return word_Pron 


    def getAction(self,    word_dmm ):
        word_verb = []
        for i in range( len( word_dmm ) ):
            if word_dmm[i][1] == 'VERB':
                if( word_dmm[i][2] == 'O' ):
                    word_verb.append(word_dmm[i][0])

        return word_verb  


    def getTheme(self,    word_dmm ):
        word_theme = []
        check_Last_Noun = False
        for i in range( len( word_dmm ) ):
            if len( word_dmm[i]) > 1 and check_Last_Noun:
                if (word_dmm[i][1] == 'NOUN'):
                    if( word_dmm[i][2] == 'O' ):
                        word_theme[-1] = word_theme[-1] + word_dmm[i][0]
                        
            
                        
                        
            if (word_dmm[i][1] == 'NOUN'): 
                if( word_dmm[i][2] == 'O' ): 
                    word_theme.append(word_dmm[i][0])
                    check_Last_Noun = True
                    if len( word_theme) > 1 and word_theme[-1] in  word_theme[-2] :
                        del word_theme[-1]
            
                    
            else :
                check_Last_Noun = False
                

        return word_theme 


    def getLocation(self,    word_dmm ):
        #print(len(word_dmm))
        word_loc = []
        check_Last_B_location = False
        for i in range( len( word_dmm ) ):

            if len( word_dmm[i]) > 1 and check_Last_B_location :
                if( word_dmm[i][2] == 'I-LOCATION'):
                    word_loc[-1] = word_loc[-1] + word_dmm[i][0]
                    
                
            if word_dmm[i][2] == 'B-LOCATION':
                word_loc.append(word_dmm[i][0])
                
                check_Last_B_location = True
            else :
                check_Last_B_location = False
            
            if word_dmm[i][2] == 'I-LOCATION':
                check_Last_B_location = True

        return word_loc


    def getTemporal( self,   word_dmm ):
        #print(len(word_dmm))
        word_date = []
        check_Last_B_date = False
        for i in range( len( word_dmm ) ):

            if len( word_dmm[i]) > 1 and check_Last_B_date :
                if( word_dmm[i][2] == 'I-DATE'):
                    word_date[-1] = word_date[-1] + word_dmm[i][0]
        
                
            if word_dmm[i][2] == 'B-DATE':
                word_date.append(word_dmm[i][0])
                
                check_Last_B_date = True
            else :
                check_Last_B_date = False
            
            if word_dmm[i][2] == 'I-DATE':
                check_Last_B_date = True

        return word_date


if __name__ == "__main__":
    print("Fuck")