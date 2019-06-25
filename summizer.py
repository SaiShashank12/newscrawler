import bs4 as bs
import urllib.request
import nltk
import re

def run():
    source = urllib.request.urlopen('https://www.newsnow.co.uk/h/World+News/Natural+Disasters').read()

    soup = bs.BeautifulSoup(source, 'lxml')
    cc = {	"va": "vatican city",
		"ch": "switzerland",
		"ad": "andorra",
		"ee": "estonia",
		"is": "iceland",
		"am": "armenia",
		"al": "albania",
		"cz": "czech republic",
		"ge": "georgia",
		"at": "austria",
		"ie": "ireland",
		"gi": "gibraltar",
		"gr": "greece",
		"nl": "netherlands",
		"pt": "portugal",
		"no": "norway",
		"lv": "latvia",
		"lt": "lithuania",
		"lu": "luxembourg",
		"es": "spain",
		"it": "italy",
		"ro": "romania",
		"pl": "poland",
		"be": "belgium",
		"fr": "france",
		"bg": "bulgaria",
		"dk": "denmark",
		"hr": "croatia",
		"de": "germany",
		"hu": "hungary",
		"ba": "bosnia/herzegovina",
		"fi": "finland",
		"by": "belarus",
		"fo": "faeroe islands",
		"mc": "monaco",
		"cy": "cyprus",
		"mk": "macedonia",
		"sk": "slovakia",
		"mt": "malta",
		"si": "slovenia",
		"sm": "san marino",
		"se": "sweden",
		"gb": "united kingdom",
		"ck": "cook islands",
		"pw": "palau",
		"tv": "tuvalu",
		"na": "nauru",
		"ki": "kiribati",
		"mh": "marshall islands",
		"nu": "niue",
		"to": "tonga",
		"nz": "new zealand",
		"au": "australia",
		"vu": "vanuatu",
		"sb": "solomon islands",
		"ws": "samoa",
		"fj": "fiji",
		"fm": "micronesia",
		"gw": "guinea-bissau",
		"zm": "zambia",
		"ci": "ivory coast",
		"eh": "western sahara",
		"gq": "equatorial guinea",
		"eg": "egypt",
		"cg": "congo",
		"cf": "central african republic",
		"ao": "angola",
		"ga": "gabon",
		"et": "ethiopia",
		"gn": "guinea",
		"gm": "gambia",
		"zw": "zimbabwe",
		"cv": "cape verde",
		"gh": "ghana",
		"rw": "rwanda",
		"tz": "tanzania",
		"cm": "cameroon",
		"na": "namibia",
		"ne": "niger",
		"ng": "nigeria",
		"tn": "tunisia",
		"lr": "liberia",
		"ls": "lesotho",
		"tg": "togo",
		"td": "chad",
		"er": "eritrea",
		"ly": "libya",
		"bf": "burkina faso",
		"dj": "djibouti",
		"sl": "sierra leone",
		"bi": "burundi",
		"bj": "benin",
		"za": "south africa",
		"bw": "botswana",
		"dz": "algeria",
		"sz": "swaziland",
		"mg": "madagascar",
		"ma": "morocco",
		"ke": "kenya",
		"ml": "mali",
		"km": "comoros",
		"st": "sao tome and principe",
		"mu": "mauritius",
		"mw": "malawi",
		"so": "somalia",
		"sn": "senegal",
		"mr": "mauritania",
		"sc": "seychelles",
		"ug": "uganda",
		"sd": "sudan",
		"mz": "mozambique",
	
		"mn": "mongolia",
		"cn": "china",
		"af": "afghanistan",
		"am": "armenia",
		"vn": "vietnam",
		"ge": "georgia",
		"in": "india",
		"az": "azerbaijan",
		"id": "indonesia",
		"ru": "russia",
		"la": "laos",
		"tw": "taiwan",
		"tr": "turkey",
		"lk": "sri lanka",
		"tm": "turkmenistan",
		"tj": "tajikistan",
		"pg": "papua new guinea",
		"th": "thailand",
		"np": "nepal",
		"pk": "pakistan",
		"ph": "philippines",
		"bd": "bangladesh",
		"ua": "ukraine",
		"bn": "brunei",
		"jp": "japan",
		"bt": "bhutan",
		"hk": "hong kong",
		"kg": "kyrgyzstan",
		"uz": "uzbekistan",
		"mm": "burma (myanmar)",
		"sg": "singapore",
		"mo": "macau",
		"kh": "cambodia",
		"kr": "korea",
		"mv": "maldives",
		"kz": "kazakhstan",
		"gt": "guatemala",
		"ag": "antigua and barbuda",
		"vg": "british virgin islands (uk)",
		"ai": "anguilla (uk)",
		"vi": "virgin island",
		"ca": "canada",
		"gd": "grenada",
		"aw": "aruba (netherlands)",
		"cr": "costa rica",
		"cu": "cuba",
		"pr": "puerto rico (us)",
		"ni": "nicaragua",
		"tt": "trinidad and tobago",
		"gp": "guadeloupe (france)",
		"pa": "panama",
		"do": "dominican republic",
		"dm": "dominica",
		"bb": "barbados",
		"ht": "haiti",
		"jm": "jamaica",
		"hn": "honduras",
		"bs": "bahamas, the",
		"bz": "belize",
		"sx": "saint kitts and nevis",
		"sv": "el salvador",
		"us": "united states",
		"mq": "martinique (france)",
		"ms": "monsterrat (uk)",
		"ky": "cayman islands (uk)",
		"mx": "mexico",
		"gd": "south georgia",
		"py": "paraguay",
		"co": "colombia",
		"ve": "venezuela",
		"cl": "chile",
		"sr": "suriname",
		"bo": "bolivia",
		"ec": "ecuador",
		"gf": "french guiana",
		"ar": "argentina",
		"gy": "guyana",
		"br": "brazil",
		"pe": "peru",
		"uy": "uruguay",
		"fk": "falkland islands",
		"om": "oman",
		"lb": "lebanon",
		"iq": "iraq",
		"ye": "yemen",
		"ir": "iran",
		"bh": "bahrain",
		"sy": "syria",
		"qa": "qatar",
		"jo": "jordan",
		"kw": "kuwait",
		"il": "israel",
		"ae": "united arab emirates",
		"sa": "saudi arabia"
}
    disaster = ['flood','storm', 'cyclone','earthquake', 'volcanic', 'tsunami', 'volcanic', 'cyclones', 'tornado', 'storms', 'landslides', 'waves', 'wildfire', 'drought', 'blizzard', 'avalanche', 'heatwave','thunderstorms']
    div = soup.find_all('div', {'class': 'hl'})
    
    data = {}
    classifier = []
    j1 = 1
    for i in div:
        a = i.findChild('a')
        span = i.findChild('span')
        source = i.findChild('span',{'class':'src-part'}).text
        art = urllib.request.urlopen(a['href']).read()
        dog = bs.BeautifulSoup(art,'lxml')
        
        for anchor in dog.findAll('a', href=True):
            try:
                get = urllib.request.urlopen(anchor['href']).read()
                parsed_article=bs.BeautifulSoup(get,'lxml')
                paragraphs=parsed_article.find_all('p')
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
                            print('disaster type:',i)
                        print('country:',cc[span['c'].lower()])
                        print('source:',source)
                        print('summary:\n',summary)
                        
                        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            except Exception as e:
               f=e

if __name__ == '__main__':       
    run()
        

        





