from bs4 import BeautifulSoup as bs
import urllib
import re
import nltk
from elasticsearch import Elasticsearch


es1 = Elasticsearch(['http://167.86.104.221:9200'], timeout=30)
def get_lat_long(q):
    print(q)
    res = es1.search(index='location_latlong', doc_type='loc-type',
                    body={"query": {"dis_max": { "queries": {"match": {"Address": q}}}}}, request_timeout=60)
    return res

def run():
    

    es=Elasticsearch([{'host':'localhost','port':9200}])
    j1 = 1
    page = urllib.request.urlopen('https://www.aljazeera.com/topics/subjects/natural-disasters.html').read()
    disaster = ['flood','storm', 'cyclone','earthquake', 'volcanic', 'tsunami', 'volcanic', 'cyclones', 'tornado', 'storms', 'landslides', 'waves', 'wildfire', 'drought', 'blizzard', 'avalanche', 'heatwave','thunderstorms']

    soup = bs(page, 'lxml')
    div = soup.find_all('div',{'class':'col-sm-7 topics-sec-item-cont'})
    for i in div:
        a = i.findChild('a',{'class':'topics-sec-item-label'})
        a1 = i.findChildren('a')
        summary =  i.findChild('p',{'class':'topics-sec-item-p'})
        l = []
        for j in a1:
            l.append(j['href'])
        spage = urllib.request.urlopen('https://www.aljazeera.com'+l[1]).read()
        soup = bs(spage,'lxml')
        paragraphs=soup.find_all('p')
        article_text=""
        

        for p in paragraphs:
            article_text+=p.text
        article_text.lower()
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)  
        article_text = re.sub(r'\s+', ' ', article_text)

        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )  
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

        sentence_list = nltk.sent_tokenize(article_text)

        stopwords = nltk.corpus.stopwords.words('english')

        word_frequencies = {}  
        for word in nltk.word_tokenize(formatted_article_text):  
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
        score = {}
        for i in disaster:
            if i in word_frequencies.keys():
                score[i] = word_frequencies[i]

        import heapq
        word1 = heapq.nlargest(1,score,key=score.get)
        count = 0
        for j in word1:
            count = score[j]
                
                
                
       
        if not len(score) is 0 and  count>2:
            dt = ''
            if summary:
                for i in word1:
                    dt = i
                    print('disaster tyrpe:',i)
                print('country:',a.text)
                print('source:aljazeera')
                print('summary:\n',summary.text)
                try:
                    p = get_lat_long(a.text.lower())
                    sample = p['hits']['hits'][0]
                    latitude = (sample['_source']['geolocation']['lat'])
                    longitude = (sample['_source']['geolocation']['lon'])
                except Exception as e:
                    latitude = 0
                    longitude = 0
                    print(e)
                print("Longitude", longitude)
                print("Latitude", latitude)
                e1 = {
                                'disaster_type': dt[0],
                                'country':a.text,
                                'source':'aljazeera',
                                'summary':summary.text,
                                'geoPoint': {
                                    'lat':longitude,
                                    'lon':longitude
                                    }
                                
                                
                            }
                
                res = es.index(index='anews',doc_type='dnews',id=j1,body=e1)
                
                        

if __name__ == '__main__':       
    run()
                                                 
