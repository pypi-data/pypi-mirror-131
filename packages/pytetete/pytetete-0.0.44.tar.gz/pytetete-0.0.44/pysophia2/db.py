import pandas as pd
import mariadb
import sys
from elasticsearch import Elasticsearch



columns = ['id', 'country', 'media_outlet', 'url', 'title', 'text', 'date', 'year', 'journalist', 'month']

sql_vars={
    "__username__":"",
    "__password__": "",
    "__cursor__":None,
    "__host__": "45.79.130.8",
    "__port__": 14096,
    "__database__":"Sun"

}

elastic_vars = {
    "__ip__" : "45.56.113.162",
    "__port__": 9200,
    "__user__": "elastic",
    "__password__": "uZCxWGE35lD3lhc",
    "__es__": Elasticsearch(
        ["45.56.113.162:9200"],
        http_auth=("elastic",
                   "uZCxWGE35lD3lhc"),
        timeout=60
        )
    
}

############ 0 LOGGING #############
def set_elastic_vars(__ip__=None, __port__=None, __user__= None, __password__= None):
    """Set the variables used for ElasticSearch connection

    Args:
        __ip__ (int, optional): [ElasticSearch host ip]. Defaults to "None".
        __port__ (int, optional): [ElasticSearch port]. Defaults to "None".
        __user__ (str, optional): [ElastichSearch username]. Defaults to "None".
        __password__ (str, optional): [ElasticSearch password]. Defaults to "None".
    """
    arguments=locals()
    has_changed=False
    global elastic_vars
    for a,b in arguments.items():
        if (b is not None):
            elastic_vars[a]=b
            has_changed=True
    if has_changed:
        host= elastic_vars["__ip__"]+":"+str(elastic_vars["__port__"])
        elastic_vars["__es__"] = Elasticsearch([host],
                                               http_auth=(elastic_vars["__user__"],
                                                          elastic_vars["__password__"]))
    return 1

def login(__username__="", __password__="", __host__=None, __port__=None, __database__=None): #45.79.130.8 #45.56.109.120
    """login into Sun database through a mariadb sql adapter.

    Args:
        __username__ (str, optional): [description]. Defaults to "sophia2api".
        __password__ (str, required): [description]. Defaults to "".
        __host__ (str, optional): [description]. Defaults to "45.79.130.8".
        __port__ (int, optional): [description]. Defaults to 14096.
        __database__ (str, optional): [description]. Defaults to "Sun".
    """
    arguments=locals()
    global sql_vars

    for a,b in arguments.items():
        if (b is not None):
            sql_vars[a]=b
    
    return connect_sun()

def connect_sun():
    """connect to sun
    Returns:
        
    """
    global sql_vars
    try:
        conn = mariadb.connect(
            user=sql_vars["__username__"],
            password=sql_vars["__password__"],
            host=sql_vars["__host__"],
            port=sql_vars["__port__"],
            database=sql_vars["__database__"]
        )
        sql_vars["__cursor__"] = conn.cursor()
        return "successful connection"
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return "connection could not be established"

def __connection_validator():
    if sql_vars["__cursor__"] is None: sys.exit("connect to the database first with: db.login(user,password)")

############ 1 INFO #############

def list_countries():
    """provides a list with all the countries that currently have media outlets in Sun.

    Returns:
        [string]: [country_name]
    """
    __connection_validator()
    sql_vars["__cursor__"].execute("SELECT DISTINCT country FROM news")
    return [x[0] for x in sql_vars["__cursor__"].fetchall()]

def list_media_outlets(countries=["all"]): 
    """provides a list with all media outlets that currently have media outlets in Sun.

    Returns:
        [string]: [media_outlet]
    """
    pd.set_option("display.max_rows",None)
    __connection_validator()
    if "all" in countries: countries=list_countries()
    media_outlets=[]
    for country in countries:
        sql_vars["__cursor__"].execute("SELECT DISTINCT media_outlet FROM news WHERE country=?",(country,))
        for media_outlet in sql_vars["__cursor__"].fetchall():
            media_outlets.append((country, media_outlet[0]))
    return pd.DataFrame(media_outlets,columns=["country", "media_outlet_name"])


def stats_countries():
    """Provides a list the countries and it's news quantity in Sun.

    Returns:
        df: country;news_quantity
    """
    __connection_validator()
    sql_vars["__cursor__"].execute("SELECT country, count(id) FROM news GROUP BY country")
    return pd.DataFrame(sql_vars["__cursor__"].fetchall(),columns=["country", "quantity"])
    

def stats_countries_by_date(_from, _to):
    """Provides a list the countries and it's news quantity between a date.
    
     Args:
        __from (string, required): [ElasticSearch host ip]. It must be passed as a string with the following format: YYYY/MM/DD.
        __to (string, required): [ElasticSearch host ip]. It must be passed as a string with the following format: YYYY/MM/DD.
        
    Returns:
        df: country;news_quantity
    """
    __connection_validator()
    sql_vars["__cursor__"].execute("SELECT country, count(id) FROM news WHERE date >= ? AND date <= ? GROUP BY country",(_from,_to))
    return pd.DataFrame(sql_vars["__cursor__"].fetchall(),columns=["country", "quantity"])
    

def stats_media_outlet(country=None):
    """Provides a list the media outlets and it's news quantity in Sun.
        country (string, optional): country name.

    Returns:
        df: media_outlet;news_quantity
    """
    pd.set_option("display.max_rows",None)
    __connection_validator()
    if country is not None:
        sql_vars["__cursor__"].execute("SELECT country, media_outlet, count(id) FROM news WHERE country = ? GROUP BY media_outlet",(country,))
    else:
        sql_vars["__cursor__"].execute("SELECT country, media_outlet, count(id) FROM news GROUP BY media_outlet")
    return pd.DataFrame(sql_vars["__cursor__"].fetchall(),columns=["country", "media_outlet_name", "quantity"])


############ 2 DATASETS #############

def last_n(n=1):
    __connection_validator()
    sql_vars["__cursor__"].execute("SELECT *, month(date) as month FROM news ORDER BY ID DESC LIMIT ?" , (n,))
    return pd.DataFrame(sql_vars["__cursor__"].fetchall(), columns=columns)

def get_dataset(country, from_, to_, keyword=None):
    global elastic_vars
    if keyword==None or keyword=="":
                query = {
            "query": { 
                "bool": {
                    "filter":[
                        {"range":{
                            "date":{
                                "gte": from_,
                                "lt": to_
                                }
                            }
                        },
                        {"term":{
                            "country": country
                            }
                        }
                        ]
                    }
                }
            }
    else:
        query = {
            "query": { 
                "bool": {
                    "must": [{
                        "match": {
                            "text":keyword
                            }
                        }],
                    "filter":[
                        {"range":{
                            "date":{
                                "gte": from_,
                                "lt": to_
                                }
                            }
                        },
                        {"term":{
                            "country": country
                            }
                        }
                        ]
                    }
                }
            }        

    res = elastic_vars["__es__"].search(index="news", body=query, size=10000)
    n_news = res['hits']['total']['value']
    if n_news == 10000:
        print("Se encontraron mas de %d noticias, por favor acotar la fecha de busqueda" % n_news)
    else:
        print("Son %d noticias encontradas..." % n_news)
    
    data = {'id_news':[],'country':[],'media_outlet':[],'url':[],'title':[],'text':[],'date':[],'search':[]}
    df = pd.DataFrame(data)
    
    for hit in res['hits']['hits']:
        id_news = hit['_source']['id_news']
        country = hit['_source']['country']
        media_outlet = hit['_source']['media_outlet']
        url = hit['_source']['url']
        title = hit['_source']['title']
        text = hit['_source']['text']
        date = hit['_source']['date']
        search = keyword
    
        new_row = {'id_news':id_news, 'country':country, 'media_outlet':media_outlet, 'url':url, 'title':title, 'text':text, 'date':date, 'search':search}
    
        df = df.append(new_row, ignore_index=True)
    
    return df
    
def export_to_csv(df, name="default"):
    df.to_csv(name,sep=";")
    print("dataset saved as"+name+".csv")
    
## FUNCIONES CASO DE USO 3

def popularity(sources, _from, _to):
    """provides a list with all media outlets that currently have media outlets in Sun.

    Returns:
        [string]: [media_outlet]
    """
    pd.set_option("display.max_rows",None)
    __connection_validator()
    rows=[]
    for name in sources:
        sql_vars["__cursor__"].execute("SELECT s.source_name, SUM(popularity_en), SUM(popularity_es), SUM(popularity_fr), SUM(popularity_it), SUM(popularity_pt), MONTH(popularity_date), YEAR(popularity_date) FROM has_popularity LEFT JOIN source s ON s.id_source = has_popularity.id_source WHERE s.source_name = ? AND popularity_date >= ? AND popularity_date <= ? GROUP BY MONTH(popularity_date), YEAR(popularity_date) ORDER BY (popularity_date)",(name,_from,_to))
        for row in sql_vars["__cursor__"].fetchall():
            rows.append(row)
    return pd.DataFrame(rows,columns=["source","popularity_en","popularity_es","popularity_fr","popularity_it","popularity_pt", "month", "year"])

def mentions(sources=['Gabriel Boric','José Antonio Kast'],_from="2020-01-01",_to="2021-12-31"):
    media_outlets=[]
    for name in sources:
        sql_vars["__cursor__"].execute("SELECT s.source_name, n.id ,n.country, n.media_outlet, n.url, n.title, n.`text`, n.`date` FROM mention  LEFT JOIN source s ON s.id_source=mention.id_source LEFT JOIN news n ON n.id =mention.id_news WHERE s.source_name = ? AND n.`date` >= ? AND n.`date` <= ?",(name,_from,_to))
        for media_outlet in sql_vars["__cursor__"].fetchall():
            media_outlets.append(media_outlet)
    _df=pd.DataFrame(media_outlets,columns=["source","id_news","country","media_outlet","url","title", "text", "date"])
    _df['date']=_df['date'].astype(str)
    return _df