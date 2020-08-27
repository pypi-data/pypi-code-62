#! /usr/bin/env python

import cssutils

from color import *

class CSSColorRule:
    def __init__(self, rule):
        self.selectors = [] 
        self.color = None
        self.background_color = None

        for prop in rule.style:
            if prop.propertyValue.item(0).type == cssutils.css.Value.COLOR_VALUE:
                if prop.name == 'background-color':
                    self.background_color = prop.propertyValue.item(0) 
                elif prop.name == 'color':
                    self.color = prop.propertyValue.item(0)
        
        for selector in rule.selectorList:
            self.selectors.append(selector)

    def result(self):
        """ Return the contrast between color and background_color, rounded 
        to 2 decimals """

        if self.color != None and self.background_color != None:
            return round(contrast(self.color, self.background_color), 2)
        else:
            return None
