from bs4 import BeautifulSoup as bs
import urllib
import re
import nltk


def run():
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
            if summary:
                for i in word1:
                    print('disaster tyrpe:',i)
                print('country:',a.text)
                print('source:aljazeera')
                print('summary:\n',summary.text)
                print('========================================================')
                        

if __name__ == '__main__':       
    run()
                                                 
