from bs4 import BeautifulSoup as bs
import requests
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
    #https://www.downtoearth.org.in/category/natural-disasters/news?page=1&per-page=25
    page = requests.get('https://www.downtoearth.org.in/category/natural-disasters/news?page=1&per-page=25')
    disaster = ['flood','storm', 'cyclone','earthquake', 'volcanic', 'tsunami', 'volcanic', 'cyclones', 'tornado', 'storms', 'landslides', 'waves', 'wildfire', 'drought', 'blizzard', 'avalanche', 'heatwave','thunderstorms']
    f = open('country.txt','r')
    contents = f.read().lower()
    contents = nltk.word_tokenize(contents)
    soup = bs(page.text, 'lxml')

                                                 
    div=soup.find_all('div',{'class':"col-lg-4 col-md-4 col-sm-5 col-xs-12 pl-0 pr-5"})
    for i in div:
        a = i.findChild('a')
        p = i.find_all('a',{'class':'topics-sec-item-labe'})
        page = urllib.request.urlopen(a['href']).read()
        spage = bs(page,'lxml')
        paragraphs=spage.find_all('p')
        article_text=""
        tags = spage.find('div',{'class':'author-categories-tags'})
        country = tags.find_all('a')
        con = ''
        for i in country:
            if i.text.lower() in contents:
                con = i.text.lower()

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
            maximum_frequncy = max(word_frequencies.values())
                    
            for word in word_frequencies.keys():  
                word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

            sentence_scores = {}  
            for sent in sentence_list:  
                for word in nltk.word_tokenize(sent.lower()):
                    if word in word_frequencies.keys():
                       if len(sent.split(' ')) < 30:
                           if sent not in sentence_scores.keys():
                               sentence_scores[sent] = word_frequencies[word]
                           else:
                               sentence_scores[sent] += word_frequencies[word]


            import heapq  
            summary_sentences = heapq.nlargest(2, sentence_scores, key=sentence_scores.get)

            summary = ' '.join(summary_sentences)
            if summary:
                try:
                            p = get_lat_long(con)
                            sample = p['hits']['hits'][0]
                            latitude = (sample['_source']['geolocation']['lat'])
                            longitude = (sample['_source']['geolocation']['lon'])
                except Exception as e:
                            latitude = 0
                            longitude = 0
                            print(e)
                dt = ''
                for i in word1:
                    dt = i
                print(summary)
                e = {
                                'disaster_type': dt,
                                'source':'down to earth',
                                'summary':summary,
                                'geoPoint': {
                                        'lat':longitude,
                                       'lon':longitude
                                    }
                           }
                res = es.index(index='news',doc_type='enews',id=j,body=e)
                j += 1
               

if __name__ == '__main__':       
    run()
        
        


