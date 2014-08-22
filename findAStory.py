import json
import string
from StringIO import StringIO
import urllib2
from UserDict import UserDict
import nltk
import re
import operator
import wolframalpha
from BeautifulSoup import BeautifulSoup
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

import numpy as np
import cv2
#from matplotlib import pyplot as plt

#from hello.models import *

PAGE_HEIGHT= 8.5
PAGE_WIDTH=5.5
styles = getSampleStyleSheet()
Title = "Hello world"
pageinfo = "platypus example"
giantListOfStopWords = []
etsy_api_key = 'iqz5tb9wzxg18xd91e8f8yj1'
etsy_api_secret = '8oexal01qs'


quotes = []


class SourceItem(UserDict):
    def __init__(self,source=None):
        UserDict.__init__(self)
        self['source'] = source
        self['text']
        print 'init complete'
    print 'instructable Class'

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def myFirstPage(canvas, doc):
    print 'myFirstPage'
    canvas.saveState()
    canvas.setFont('Times-Bold',16)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch,"First Page / %s" % pageinfo)
    canvas.restoreState()

def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch,"Page %d %s" % (doc.page, pageinfo))
    canvas.restoreState()

def findParagraphsWithFeaturedWord():
    pass

def orbFeature():
    img = cv2.imread('NASA_child_bubble_exploration.jpg',0)

    # Initiate STAR detector
    orb = cv2.ORB()
    # find the keypoints with ORB
    kp = orb.detect(img,None)
    # compute the descriptors with ORB
    kp, des = orb.compute(img, kp)
    
    # draw only keypoints location,not size and orientation
    img2 = cv2.drawKeypoints(img,kp,img,color=(0,255,0), flags=0)
    # plt.imshow(img2),plt.show()

def scanBook(urlToGet,title):
    doc = SimpleDocTemplate("brothersGrimm.pdf", leftMargin=100,rightMargin=30,topMargin=140,bottomMargin=360 )
    Story = [Spacer(1,2*inch)]
    style = styles["Normal"]
    url = urllib2.urlopen(urlToGet)
    chunk = url.read()
    soup = BeautifulSoup(chunk)
    counts = {}
    allWords = []
    j = 300
    for paragraph in soup.findAll('p'):
        if j < 400:
            para =  paragraph.getText()
            if len(para) > 1:
                bogustext = paragraph.getText()
                p = Paragraph(bogustext, style)
                tokens = nltk.word_tokenize(bogustext)
                tagged = nltk.pos_tag(tokens)
                entities = nltk.chunk.ne_chunk(tagged)
                for element in entities:
                    # print element
                    if not element[0] in counts:
                        counts[element[0]] = 0
                        allWords.append(element)
                    else:
                        counts[element[0]] = counts[element[0]] + 1 
                #Counting Words...
                
                Story.append(p)
                Story.append(Spacer(1,0.2*inch) )
            j += 1
        else:
            break

    #           print 'All words!'
    #for each in allWords:
    #    print each
    # counts is counting the top words. 
    sorted_x = sorted(counts.iteritems(), key=operator.itemgetter(1))
    i = 300;
    print 'most popular NN'
    topElements = []
    while (i > 0):
        #print sorted_x[len(sorted_x)-i][0]
        for each in allWords:
            if each[0] == sorted_x[len(sorted_x)-i][0]:
                topElements.append(each)
        i = i - 1
        
    mostFrequentNN = []
    for each in topElements:
        print each
        try:
            if each[1] == 'NN':
                mostFrequentNN.append( each[0] )
        except:
            if each[0][1] == 'NN':
                mostFrequentNN.append( each[0][0] )
    print 'most frequent NN'
    for each in mostFrequentNN:
        print each
    # Save mostfrequent NN list to csv file...
    myFile = open("mostfrequentNN.txt", 'w')
    print "Opening the file..."
    print "Truncating the file.  Goodbye!"
    myFile.truncate()
    for each in mostFrequentNN:
        myFile.write(each + "\n")
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
    print 'look at the doc.'
    print 'do you see a way to look at each page of text?'
    pageEnds = []
    countPages = 0
    for each in doc.canv._doc.Pages.pages:
        countPages += 1
        rowCount = 0
        listOfLines = []
        for row in each.Contents.content.splitlines():
            listOfLines.append( row )
            rowCount += 1
        print listOfLines[rowCount-4]
        
        i = 1
        endNumPage = listOfLines[rowCount-i].find(') Tj T* ET')
        while ( endNumPage == -1):
            i += 1
            endNumPage = listOfLines[rowCount-i].find(') Tj T* ET')
        pageEnds.append(listOfLines[rowCount-i][endNumPage-14:endNumPage])
            
    if ( len(listOfLines) == rowCount ):
        print 'each page had a row added to list of Lines'
    else: 
        print 'check each page contributes a pageEnd'
    for each in pageEnds:
        print each
    # Save mostfrequent NN list to csv file...
    myFile = open("pageEnds.txt", 'w')
    print "Opening the file..."
    print "Truncating the file.  Goodbye!"
    myFile.truncate()
    for each in pageEnds:
        myFile.write(each + "\n")   
        # How do I find the first few text words...
        
            
            
        
    # print doc.canv._doc.Pages.pages[0].Contents.content
    return mostFrequentNN

def pageMake():
    print 'assembling page design'
    print 'building pages requires all of the other events to be completed'

def findItems(phrase, numberOfResults = 10):
    print 'populating Etsy, Instructables and Thingiverse Fields'
    # Query Etsy, Thingiverse, Instructables
     
    # colorStrings get all phrases about the color from the database
    
    newInstruct = instructablesSearch(phrase,numberOfResults)
    newThingy = searchThingiverse(phrase,10)
    newEtsy = searchEtsy(phrase,10)

def keywordPhrases(quotes,keywordList): # used to be called colorPhrases 
    # making keyword phrases 
    print 'making color phrases'
    ideaList = []
    for each in quotes:
        try:
            words = each['text'].split()
            wordPrior = ''
            wordNext = ''
            counter = 0
            # Look at each quote
            for word in words:
                word = word.replace(".", "")
                word = word.replace(",", "")
                word = word.replace('"', "")
                word = word.replace('!', "")
                word = word.replace('?', "")
                word = word.replace(':', "")
                word = word.replace(';', "")

                if len(word) > 1:
                    for keyword in keywordList:
                        #if word in color:
                        if findWholeWord(word)(keyword) != None:
                            # it's a color word! 
                            # get wordPrior and wordNext
                            inCount = counter
                            while inCount > 0:
                                wordPrior = words[inCount-1]
                                wordPrior = wordPrior.replace(".", "")
                                wordPrior = wordPrior.replace(",", "")
                                wordPrior = wordPrior.replace('"', "")
                                wordPrior = wordPrior.replace('!', "")
                                wordPrior = wordPrior.replace('?', "")
                                wordPrior = wordPrior.replace(':', "")
                                wordPrior = wordPrior.replace(';', "")

                                foundStopWord = False
                                for stopWord in giantListOfStopWords:
                                    if findWholeWord(stopWord)(wordPrior) != None:
                                        inCount = inCount - 1
                                        foundStopWord = True
                                        break
                                if not foundStopWord:
                                    inCount = 0
                            nextCount = counter
                            while nextCount < len(words)-2:
                                wordNext = words[nextCount+1]
                                wordNext = wordNext.replace(".", "")
                                wordNext = wordNext.replace(",", "")
                                wordNext = wordNext.replace('"', "")
                                
                                wordNext = wordNext.replace('!', "")
                                wordNext = wordNext.replace('?', "")
                                wordNext = wordNext.replace(':', "")
                                wordNext = wordNext.replace(';', "")
                                foundStopWord = False
                                giantListOfStopWords.append("the")
                                giantListOfStopWords.append("a")
                                for stopWord in giantListOfStopWords:
                                    if findWholeWord(stopWord)(wordNext) != None:
                                        nextCount += 1
                                        foundStopWord = True
                                        break
                                if not foundStopWord:
                                    nextCount = len(words)
                                giantListOfStopWords.remove("the")
                                giantListOfStopWords.remove("a")
                            try:  
                                newPhrase =  wordPrior +" "+word+" "+wordNext
                                ideaList.append( newPhrase )
                            except Exception as e:
                                print e
                counter = counter + 1
        except Exception as e:
            print e
    print 'phrases'
    myFile = open("ideaList.txt", 'w')
    print "Opening the file..."
    print "Truncating the file."
    myFile.truncate()
    for each in ideaList:
        myFile.write(each + "\n") 
        print each
    return ideaList

def keywordQuote(urlToGet,title,wordList): # used to be called colorQuote
#    print 'making color quotes'
    # colors = [' red ',' green ',' blue ',' yellow ',' purple ',' black ']
    url = urllib2.urlopen(urlToGet)
    chunk = url.read()
    soup = BeautifulSoup(chunk)
    quotes = []
    counter = 1
    for paragraph in soup.findAll('p'):
        for word in wordList:
            # if color in text:
            print word
            print paragraph.getText() 
            if findWholeWord( word )(paragraph.getText()) != None:    
                if len(quotes) > 0:
                    if quotes[len(quotes)-1]['id'] != counter:
                        newQuote = {'title':title,'text':paragraph.getText(), 'id':counter }
                        quotes.append(newQuote)

                else:
                    newQuote = {'title':title,'text':paragraph.getText(), 'id':counter }
                    quotes.append(newQuote)
        counter = counter + 1
    return quotes

def paragraphMake(urlToGet,title): # used to be called searchclient.scanBooks()
    print 'making paragraphs by scanning the book'
    url = urllib2.urlopen(urlToGet)
    chunk = url.read()
    soup = BeautifulSoup(chunk)
    paragraphs = []
    counter = 1
    for paragraph in soup.findAll('p'):
        newPara = {}
        newPara['text'] = paragraph.getText()
        newPara['title'] = title
        newPara['id'] = counter
        if len(newPara['text']) > 1:
            paragraphs.append(newPara['text'])
            counter = counter + 1
    # If I want to do extra validation of paragraphs, here is a good spot.
def searchEtsy(phrase,maxNumber):
    try:
        query = phrase.phrase
        query = '+'.join(query.split()) #replace spaces with '+' for url format
        urlFormatSearch = 'https://openapi.etsy.com/v2/listings/active?keywords=' + query +'&limit=12&includes=Images:1&api_key='+etsy_api_key
        url = urllib2.urlopen(urlFormatSearch)
        chunk = url.read()
        io = StringIO( chunk )
        etsyItems = json.load(io)
        toRet = []
        for item in etsyItems['results']:
            newEtsy = SourceItem('etsy')
            newEtsy.name = item['title']
            newEtsy.image = item['Images'][0]['url_170x135']
            newEtsy.title = phrase.title
            newEtsy.id = phrase.id
            newEtsy.phrase = phrase.phrase
            newEtsy.put()
            toRet.append(newEtsy)
        return toRet
    except Exception as e:
        print e
        return []
def makeInstructable(soup):
    """Given a BeautifulSoup object from an instructables page,
    create and return an instructables object. Return None on error."""

    try:
        instr = SourceItem('instructable')

        meta = soup.findAll('meta')
        meta = [x for x in meta if x.get('property') is not None]
        #print meta
        #print "********************before for loop*************"
        for x in meta:
            #print x.get('property'), x.get('content')
            if "og:title" in x.get('property'):
                instr.name = x.get('content')
            #elif "og:type" in x.get('property'):
            #    otype = x.get('content')
            elif "og:url" in x.get('property'):
                instr.url = x.get('content')
            elif "og:image" in x.get('property'):
                # print "image is %s" % x.get('content')
                instr.image = x.get('content')
            elif "og:description" in x.get('property'):
                instr.description = x.get('content')
        return instr
    except Exception as e:
        print e
        return None
def instructablesSearch(phrase, maxNumber, detailed=False,returnType='dictionary' ):
    """Given a string search query, return a list of Instructables objects.
    The list will contain no more than 'maxNumber' items and can be empty.
    If 'detailed' is set to False, each object has only the title, image, and
    url (no description), but returns quickly. If true, each object also has
    description populated, but requires fetching a new html page for every
    object."""

    try:
        query = phrase
        query = '+'.join(query.split()) #replace spaces with '+' for url format
        soup = BeautifulSoup(urllib2.urlopen("http://www.instructables.com/tag/type-id/featured-true/?sort=none&q=" + query)) # soup object of search results page
        res = soup.find(id="infinite-search-results")
        res = res.findAll('li')
        if (maxNumber < len(res)):
            res = res[:maxNumber]

        toRet = []

        if not detailed:
            for x in res:
                instr = SourceItem('instructable')
                instr.name = x.a.get('title') # ISSUE: this will cut off titles with
                    # quotes. Can use #instr.name = x.div.div.a.get_text() instead,
                    # but this will cut off titles that are longer than the two-line
                    # instructables title space...
                instr.image = x.a.img.get('src')
                instr.url = "http://www.instructables.com" + x.a.get('href')
                #instr.description = None
                #instr.title = phrase.title
                #instr.id = phrase.id
                #instr.phrase = phrase.phrase
                instr.put()
                toRet.append(instr)

        elif detailed:
            for x in res:
                soup = BeautifulSoup(urllib2.urlopen("http://www.instructables.com" + x.a.get('href')))
                toRet.append(makeInstructable(soup))

        toRet = [x for x in toRet if x is not None]
        return toRet

    except Exception as e:
        print e
        return []
def getThingiverse(url):
    """Given a url for a Thingiverse page, extract content and return
    Thingiverse idea. Return None on error."""
    try:
        soup = BeautifulSoup(urllib2.urlopen(url))

        newThing = SourceItem('thingiverse')

        newThing.url = url
        newThing.name = soup.find('h1').string
        newThing.image = soup.find(attrs={"class": "thing-page-image featured"}).img.get('src')
        print newThing.image
        s = soup.find(id="description")
        s = str(s)
        start = string.find(s,">")
        end = string.find(s,"</div>",start)
        s = s[start+1:end]

        while string.find(s,'<') is not -1:
            start = string.find(s,'<')
            end = string.rfind(s,'>')
            s = s.replace(s[start:end+1],"")

        newThing.description = s.strip()

        return newThing

    except Exception as e:
        print e
        return None
def searchThingiverse(phrase, number, detailed=False):
    """Search query on Thingiverse, returning a list of a maximum of number
    Thingiverse objects. The list can be empty. If detailed is False,
    the descriptions will be ommitted from each object, but the search will
    return faster."""

    try:
        query = phrase.phrase
        query = '+'.join(query.split())
        baseurl = "http://www.thingiverse.com/search/prolific/things/page:"
        endurl = "?q="
        allThings = []
    
        try:
            for i in range(1, int(number - 1) / 12 + 2):
                soup = BeautifulSoup(urllib2.urlopen(baseurl + str(i) + endurl + query))
                results = soup.findAll(attrs={"data-thing-id": True})
                if detailed:
                    for x in results:
                        allThings.append(getThingiverse("http://www.thingiverse.com" + x.div.a.get('href')))
    
                elif not detailed:
                    for x in results:
                        newThing = SourceItem('thingiverse')
                        newThing.name = x.get('title')
                        newThing.url = "http://www.thingiverse.com/thing:" + x.get('data-thing-id')
                        newThing.image = x.img.get('src')
                        print newThing.image
#                         newThing.id = phrase.id
#                         newThing.title = phrase.title
#                         newThing.fileName =  newThing.name.replace(" ", "") + ".png"
#                         newThing.phrase = phrase.phrase
#                         newThing.put()
                        allThings.append(newThing)
    
            allThings = [x for x in allThings if x is not None]
            return allThings[:number]
        except:
            return []
    except:
        return []

if __name__ == "__main__":
    print 'here I am'
    client = wolframalpha.Client("WJYTHW-WVLY98YW77")
    res = client.query('define universe')
    resString = next(res.results).text
    print resString
    #orbFeature()
    urlToGet = 'http://swift-door-556.appspot.com/book7/'
    title = 'The Brothers Grimm' 
    keywords = scanBook(urlToGet,title)
#     keywordQuotes = keywordQuote(urlToGet,title,keywords)
#     phraseList = keywordPhrases(keywordQuotes,keywords)
#     for each in phraseList:
#         findItems(each,10)
    # Now there are 2 primary 
print 'all done now'


giantListOfStopWords = ["a's",
"able",
"about",
"above",
"according",
"accordingly",
"across",
"actually",
"after",
"afterwards",
"again",
"against",
"ain't",
"all",
"allow",
"allows",
"almost",
"alone",
"along",
"already",
"also",
"although",
"always",
"am",
"among",
"amongst",
"an",
"and",
"another",
"any",
"anybody",
"anyhow",
"anyone",
"anything",
"anyway",
"anyways",
"anywhere",
"apart",
"appear",
"appreciate",
"appropriate",
"are",
"aren't",
"around",
"as",
"aside",
"ask",
"asking",
"associated",
"at",
"available",
"away",
"awfully",
"b",
"be",
"became",
"because",
"become",
"becomes",
"becoming",
"been",
"before",
"beforehand",
"behind",
"being",
"believe",
"below",
"beside",
"besides",
"best",
"better",
"between",
"beyond",
"both",
"brief",
"but",
"by",
"c",
"c'mon",
"c's",
"came",
"can",
"can't",
"cannot",
"cant",
"cause",
"causes",
"certain",
"certainly",
"changes",
"clearly",
"co",
"com",
"come",
"comes",
"concerning",
"consequently",
"consider",
"considering",
"contain",
"containing",
"contains",
"corresponding",
"could",
"couldn't",
"course",
"currently",
"d",
"definitely",
"described",
"despite",
"did",
"didn't",
"different",
"do",
"does",
"doesn't",
"doing",
"don't",
"done",
"down",
"downwards",
"during",
"e",
"each",
"edu",
"eg",
"eight",
"either",
"else",
"elsewhere",
"enough",
"entirely",
"especially",
"et",
"etc",
"even",
"ever",
"every",
"everybody",
"everyone",
"everything",
"everywhere",
"ex",
"exactly",
"example",
"except",
"f",
"far",
"few",
"fifth",
"first",
"five",
"followed",
"following",
"follows",
"for",
"former",
"formerly",
"forth",
"four",
"from",
"further",
"furthermore",
"g",
"get",
"gets",
"getting",
"given",
"gives",
"go",
"goes",
"going",
"gone",
"got",
"gotten",
"greetings",
"h",
"had",
"hadn't",
"happens",
"hardly",
"has",
"hasn't",
"have",
"haven't",
"having",
"he",
"he's",
"hello",
"help",
"hence",
"her",
"here",
"here's",
"hereafter",
"hereby",
"herein",
"hereupon",
"hers",
"herself",
"hi",
"him",
"himself",
"his",
"hither",
"hopefully",
"how",
"howbeit",
"however",
"i",
"i'd",
"i'll",
"i'm",
"i've",
"ie",
"if",
"ignored",
"immediate",
"in",
"inasmuch",
"inc",
"indeed",
"indicate",
"indicated",
"indicates",
"inner",
"insofar",
"instead",
"into",
"inward",
"is",
"isn't",
"it",
"it'd",
"it'll",
"it's",
"its",
"itself",
"j",
"just",
"k",
"keep",
"keeps",
"kept",
"know",
"knows",
"known",
"l",
"last",
"lately",
"later",
"latter",
"latterly",
"least",
"less",
"lest",
"let",
"let's",
"like",
"liked",
"likely",
"look",
"looking",
"looks",
"ltd",
"m",
"mainly",
"many",
"may",
"maybe",
"me",
"mean",
"meanwhile",
"merely",
"might",
"more",
"moreover",
"most",
"mostly",
"much",
"must",
"my",
"myself",
"n",
"name",
"namely",
"nd",
"near",
"nearly",
"necessary",
"need",
"needs",
"neither",
"never",
"nevertheless",
"new",
"next",
"nine",
"no",
"nobody",
"non",
"none",
"noone",
"nor",
"normally",
"not",
"nothing",
"novel",
"now",
"nowhere",
"o",
"obviously",
"of",
"off",
"often",
"oh",
"ok",
"okay",
"old",
"on",
"once",
"one",
"ones",
"only",
"onto",
"or",
"other",
"others",
"otherwise",
"ought",
"our",
"ours",
"ourselves",
"out",
"outside",
"over",
"overall",
"own",
"p",
"particular",
"particularly",
"per",
"perhaps",
"placed",
"please",
"plus",
"possible",
"presumably",
"probably",
"provides",
"q",
"que",
"quite",
"qv",
"r",
"rather",
"rd",
"re",
"really",
"reasonably",
"regarding",
"regardless",
"regards",
"relatively",
"respectively",
"right",
"s",
"said",
"same",
"saw",
"say",
"saying",
"says",
"second",
"secondly",
"see",
"seeing",
"seem",
"seemed",
"seeming",
"seems",
"seen",
"self",
"selves",
"sensible",
"sent",
"serious",
"seriously",
"seven",
"several",
"shall",
"she",
"should",
"shouldn't",
"since",
"six",
"so",
"some",
"somebody",
"somehow",
"someone",
"something",
"sometime",
"sometimes",
"somewhat",
"somewhere",
"soon",
"sorry",
"specified",
"specify",
"specifying",
"still",
"sub",
"such",
"sup",
"sure",
"t",
"t's",
"take",
"taken",
"tell",
"tends",
"th",
"than",
"thank",
"thanks",
"thanx",
"that",
"that's",
"thats",
"their",
"theirs",
"them",
"themselves",
"then",
"thence",
"there",
"there's",
"thereafter",
"thereby",
"therefore",
"therein",
"theres",
"thereupon",
"these",
"they",
"they'd",
"they'll",
"they're",
"they've",
"think",
"third",
"this",
"thorough",
"thoroughly",
"those",
"though",
"three",
"through",
"throughout",
"thru",
"thus",
"to",
"together",
"too",
"took",
"toward",
"towards",
"tried",
"tries",
"truly",
"try",
"trying",
"twice",
"two",
"u",
"un",
"under",
"unfortunately",
"unless",
"unlikely",
"until",
"unto",
"up",
"upon",
"us",
"use",
"used",
"useful",
"uses",
"using",
"usually",
"uucp",
"v",
"value",
"various",
"very",
"via",
"viz",
"vs",
"w",
"want",
"wants",
"was",
"wasn't",
"way",
"we",
"we'd",
"we'll",
"we're",
"we've",
"welcome",
"well",
"went",
"were",
"weren't",
"what",
"what's",
"whatever",
"when",
"whence",
"whenever",
"where",
"where's",
"whereafter",
"whereas",
"whereby",
"wherein",
"whereupon",
"wherever",
"whether",
"which",
"while",
"whither",
"who",
"who's",
"whoever",
"whole",
"whom",
"whose",
"why",
"will",
"willing",
"wish",
"with",
"within",
"without",
"won't",
"wonder",
"would",
"would",
"wouldn't",
"x",
"y",
"yes",
"yet",
"you",
"you'd",
"you'll",
"you're",
"you've",
"your",
"yours",
"yourself",
"yourselves",
"z",
"zero",]
