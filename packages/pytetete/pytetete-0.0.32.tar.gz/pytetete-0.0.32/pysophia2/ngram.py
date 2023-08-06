import numpy as np
from spacy import load as LOAD
from spacy.matcher import Matcher
from collections import Counter
import matplotlib.pyplot as plt
from spacy import util as util
import subprocess
from datetime import datetime


ngram_vars={
    "nlp":"",
    "matcher":""
}
plt.rcParams['figure.figsize'] = [6, 8]
def setup():
    global ngram_vars
    ngram_vars["nlp"] = LOAD('es_core_news_md', disable=['parser','ner','textcat','...'] )
    ngram_vars["matcher"] = Matcher(ngram_vars["nlp"].vocab)

    pattern_1 = [{"POS": "NOUN"},{"LOWER": "de"}, {"POS": "NOUN"}]
    pattern_2 = [{"POS": "NOUN"}, {"POS": "ADJ"}]

    ngram_vars["matcher"].add("NOUN-de-NOUN", [pattern_1])
    ngram_vars["matcher"].add("NOUN-ADJ", [pattern_2])   
    
if not util.is_package("es_core_news_md"):
    subprocess.run("python -m spacy download es_core_news_md")
    print("...instalando el modelo de leguanje 'es_core_news_md', porfavor reiniciar el kernel y vuelva a importar la libreria")
else:
    setup()


 


def get_keywords(dataFrame):
    new_row=np.zeros(len(dataFrame.index))
    dataFrame['keywords']=new_row
    for index,row in dataFrame.iterrows():
        text=row["text"]
        filteredText=''.strip()
        tokens = ngram_vars["nlp"](text.lower())
        '''tokens = [token
                 for token in tokens
                 if not token.is_stop and not token.is_punct]'''
        for token in tokens:
            if token.pos_ == "NOUN" :
                filteredText=filteredText+str(token.text.lower().strip())+","
                
        matches = ngram_vars["matcher"](tokens)
        for mach_id, start, end in matches:
            span = tokens[start:end]
            filteredText=filteredText+str(span.text.lower().strip())+","
        dataFrame.loc[index,'keywords']=filteredText
        
def get_frequency(df):
    if "keywords" not in df:
        get_keywords(df)
    concept_freq_total=Counter({})

    for index, row in df.iterrows():
        arreglo=row["keywords"].split(",")
        arreglo.pop()
        arreglo=list(dict.fromkeys(arreglo))#elimina los duplicados para contar una vez por noticia cada palabra
        concept_freq = Counter(arreglo)
        concept_freq_total = concept_freq_total + concept_freq
    return {"total_news":len(df),"total_elements": sum(concept_freq_total.values()), "dictionary": concept_freq_total}

def group_by_date(dataset, granularity="month"):
    if granularity == "month":
        return dataset.groupby(by=["month","year"])
    if granularity == "year":
        return dataset.groupby(by=["year"])
    if granularity == "day":
        return dataset.groupby(by=["date"])
    
    
def calculateDist(dataset,group_by="month"):
    if "keywords" not in dataset:
        get_keywords(dataset)
    dataset_=dataset.copy()
    dataset_["month"]=dataset_['date'].apply(lambda x: x.split("-")[1])
    dataset_["year"]=dataset_['date'].apply(lambda x: x.split("-")[0])
    gb_dataset=group_by_date(dataset_, group_by)
    sophia2_ngram_struct = {}
    if group_by == "day":
        for key, ds in gb_dataset:
            sophia2_ngram_struct[datetime.strptime(key, '%Y-%m-%d').strftime("%Y/%m/%d")] = get_frequency(ds)
    elif group_by == "month":
        for (month,year), ds in gb_dataset:
            sophia2_ngram_struct[(str(year)+"/"+str(month))] = get_frequency(ds)
    elif group_by == "year":
        for year, ds in gb_dataset:
            sophia2_ngram_struct[str(year)] = get_frequency(ds)
    else: return "Wrong granularity parameter, please use 'day', 'month' or 'year' as granularity parameter instead of "+granularity
    
    return sophia2_ngram_struct

def view(word_distribution, words, annotate, normalize=True): ##to word_distribution
    ngram_dictionary={}
    for palabra in words:
        ngram_dictionary[palabra]=[]
        keys=[]
        if normalize==True:
            for key in word_distribution:
                keys.append(key)
                ngram_dictionary[palabra].append(word_distribution[key]["dictionary"][palabra]/word_distribution[key]["total_news"])
        else:    
            for key in word_distribution:
                keys.append(key)
                ngram_dictionary[palabra].append(word_distribution[key]["dictionary"][palabra])
        plt.plot(keys,ngram_dictionary[palabra],label=palabra)
        plt.legend(loc=5, bbox_to_anchor=(1.3, 0.5), fancybox=True, shadow=True )
        plt.title("PySophia2 NGramViewer")
        if(annotate):
            for xy in zip(keys, ngram_dictionary[palabra]):                                       # <--
                plt.annotate(('%.2f' % xy[1]), xy=xy, textcoords='data')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.xticks(rotation=90)
    plt.rcParams['figure.figsize'] = [7, 7]
    
    
def get_n_most_freq(freq_struct, n, graph=False):
    '''provides a list with all the countries that currently have media outlets in Sun

    Returns:
        [string]: [country_name]
    '''
    dict_orders = sorted(freq_struct["dictionary"].items(), key=lambda x: x[1], reverse=True)
    if graph:
        
        x = [x[0] for x in dict_orders[:n]]
        y = [x[1]/freq_struct["total_elements"] for x in dict_orders[:n]]
        plt.bar(x,y)
        plt.title("term frequency top %i words" %(n))
    return dict_orders[:n]

def freq(word_distribution,top_n=None, words=None, graph=True):
    concept_freq_total=Counter({})
    total_news=0
    for a in word_distribution:
        concept_freq_total= concept_freq_total + word_distribution[a]["dictionary"]
        total_news=total_news+word_distribution[a]["total_news"]
    if top_n==None and words ==None:
        print("debes pasar como argumento top_n o un arreglo words")
    elif top_n!=None and words !=None:
        print("debes pasar como argumento top_n o un arreglo words, no ambos")
    elif top_n!=None:
        top=concept_freq_total.most_common(top_n)
        if graph:
        
            x = [x[0] for x in top]
            y = [x[1]/total_news for x in top]
            plt.bar(x,y)
            plt.title("Term frecuency top %i words" %(top_n))
        return top
    elif words!=None:
        y = []
        for word in words:
            y.append(concept_freq_total[word]/total_news)
        plt.bar(words,y)
        plt.title("Term frecuency bar graph")
        plt.xticks(rotation=90)
        
        


