from bs4 import BeautifulSoup as bs
import requests
import urllib
import re
import nltk


def down:
    #https://www.downtoearth.org.in/category/natural-disasters/news?page=1&per-page=25
    page = requests.get('https://www.downtoearth.org.in/category/natural-disasters/news?page=1&per-page=25')
    disaster = ['flood','storm', 'cyclone','earthquake', 'volcanic', 'tsunami', 'volcanic', 'cyclones', 'tornado', 'storms', 'landslides', 'waves', 'wildfire', 'drought', 'blizzard', 'avalanche', 'heatwave','thunderstorms']

    soup = bs(page.text, 'lxml')

                                                 
    div=soup.find_all('div',{'class':"col-lg-4 col-md-4 col-sm-5 col-xs-12 pl-0 pr-5"})
    for i in div:
        a = i.findChild('a')
        p = i.find_all('a',{'class':'topics-sec-item-labe'})
        page = urllib.request.urlopen(a['href']).read()
        spage = bs(page,'lxml')
        paragraphs=spage.find_all('p')
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
                for i in word1:
                    print(i)
                print(summary)
                        
                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

if __name__ == '__main__':       
    run()
        
        


