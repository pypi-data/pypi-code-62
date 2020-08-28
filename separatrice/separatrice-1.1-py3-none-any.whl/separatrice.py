import re
import pymorphy2

class Separatrice:
  def __init__(self):
    self.alphabets= "([А-Яа-я])"
    self.acronyms = "([А-Яа-я][.][А-Яа-я][.](?:[А-Яа-я][.])?)"
    self.prefixes = "(Mr|Mrs|Ms|акад|чл.-кор|канд|доц|проф|ст|мл|ст. науч|мл. науч|рук|тыс|млрд|млн|кг|км|м|мин|сек|ч|мл|нед|мес|см|сут|проц)[.]"
    self.starters = "(Mr|Mrs|Ms|Dr)"
    self.websites = "[.](com|net|org|io|gov|ru|xyz|ру)"
    self.suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    self.conjs = '(чтобы|когда|несмотря на то что|вопреки|а также|либо|но|зато|а|тогда|а то|так что|чтоб|затем|дабы|коль скоро|если бы|если б|коль скоро|тогда как|как только|подобно тому как|будто бы)'
    self.morph = pymorphy2.MorphAnalyzer()
  
  def into_sents(self,text):
    if text[-1] != '.' and text[-1] != '!' and text[-1] != '?':
      text += '.'
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(' '+self.prefixes,"\\1<prd>",text)
    text = re.sub(self.websites,"<prd>\\1",text)
    print(text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + self.alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(self.acronyms+" "+self.starters,"\\1<stop> \\2",text)
    text = re.sub(self.alphabets + "[.]" + self.alphabets + "[.]" + self.alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(self.alphabets + "[.]" + self.alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+self.suffixes+"[.] "+self.starters," \\1<stop> \\2",text)
    text = re.sub(" "+self.suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + self.alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences
  
  def _pred_in(self,text):
    tokenized = text.strip(' ').split(' ')
    noun = False
    pron = False
    adj = False
    prt = False
    for word in tokenized:
      word = word.strip('.')
      word = word.strip('!')
      word = word.strip('?')
      word = word.strip(',')
      if 'NOUN' in self.morph.parse(word)[0].tag:
        noun = True
      if 'NPRO' in self.morph.parse(word)[0].tag:
        pron = True
      elif 'ADJF' in self.morph.parse(word)[0].tag or 'ADJS' in self.morph.parse(word)[0].tag:
        adj = True
      elif 'PRTF' in self.morph.parse(word)[0].tag or 'PRTS' in self.morph.parse(word)[0].tag:
        prt = True
      elif 'VERB' in self.morph.parse(word)[0].tag or 'INFN' in self.morph.parse(word)[0].tag or 'PRED' in self.morph.parse(word)[0].tag:
        #print(text, ' has a pred')
        return True
      if len(self.morph.parse(word)) > 1:
        if 'VERB' in self.morph.parse(word)[1].tag:
          #print(text, ' has a pred')
          return True
    if ((noun == True or pron == True) and adj == True):
      return True
    if ((noun == True or pron == True) and prt == True):
      return True
    if (noun == True and pron == True):
      return True
    return False
  
  def _util(self,text):
    result = []
    cands = re.split(',',text)
    for i in range(len(cands)):
      if self._pred_in(cands[i]) == False:
        if cands[i-1] in result:
          result.remove(cands[i-1])
        result.append(cands[i-1] + ' ' + cands[i])
      else:
        result.append(cands[i])
    return result

  def into_clauses(self,text):
    text = ' ' + text + ' '
    text = re.sub(', ' + self.conjs + ' | ' + self.conjs + ' ', '<stop>',text)
    clauses = text.split('<stop>')
    temp = []
    for clause in clauses:
      for x in self._util(clause):
        temp.append(x.strip(' '))
    return [x for x in temp if x != '']

