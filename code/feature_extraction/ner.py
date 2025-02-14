#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Named-entity-recognition (NER): Feature that recognizes named entities in the tweet.
@author: louiskhub
"""

import numpy as np
import spacy
from code.feature_extraction.feature_extractor import FeatureExtractor


class NER(FeatureExtractor):
    """class for recognition of named entities in the tweet"""

    # constructor
    def __init__(self, input_column):
        super().__init__([input_column], "{0}_ner".format(input_column))

    # don't need to fit, so don't overwrite _set_variables()

    # compute the named entities based on the inputs
    def _get_values(self, inputs):
        
        result = np.empty(shape=(0,18))         # for later storage
        nlp = spacy.load("en_core_web_sm")      # trained English pipeline 

        for row in inputs[0]:
            
            tokens = ' '.join(row)              # SpaCy func needs a string not tokens 
            doc = nlp(tokens)
            ents = np.zeros(shape=18)
            
            for token in doc:
                ent_type = token.ent_type_      # look for all Entity types provided by SpaCy
                if ent_type != '':              # (Reference: https://miro.medium.com/max/2400/1*QXIMTMpUCUmS4CIjHQoM-Q.png)
                    if ent_type == 'PERSON':
                        ents[0] += 1
                    elif ent_type == 'NORP':
                        ents[1] += 1
                    elif ent_type == 'FAC':
                        ents[2] += 1
                    elif ent_type == 'ORG':
                        ents[3] += 1
                    elif ent_type == 'GPE':
                        ents[4] += 1
                    elif ent_type == 'LOC':
                        ents[5] += 1
                    elif ent_type == 'PRODUCT':
                        ents[6] += 1
                    elif ent_type == 'EVENT':
                        ents[7] += 1
                    elif ent_type == 'WORK_OF_ART':
                        ents[8] += 1
                    elif ent_type == 'LAW':
                        ents[9] += 1
                    elif ent_type == 'LANGUAGE':
                        ents[10] += 1
                    elif ent_type == 'DATE':
                        ents[11] += 1
                    elif ent_type == 'TIME':
                        ents[12] += 1
                    elif ent_type == 'PERCENT':
                        ents[13] += 1
                    elif ent_type == 'MONEY':
                        ents[14] += 1
                    elif ent_type == 'QUANTITY':
                        ents[15] += 1
                    elif ent_type == 'ORDINAL':
                        ents[16] += 1
                    elif ent_type == 'CARDINAL':
                        ents[17] += 1
            
            result = np.append(result, [ents], axis=0) 
                    
        return result