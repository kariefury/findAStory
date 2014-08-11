import urllib2
import csv
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
    doc = SimpleDocTemplate("phello.pdf")
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
    myFile = open("mostfrequentNN.csv", 'w')
    print "Opening the file..."
    print "Truncating the file.  Goodbye!"
    myFile.truncate()
    for each in mostFrequentNN:
        myFile.write(each + "\n")
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
    print 'look at the doc.'
    print 'do you see a way to look at each page of text?'

if __name__ == "__main__":
    print 'here I am'
    client = wolframalpha.Client("WJYTHW-WVLY98YW77")
    res = client.query('define universe')
    resString = next(res.results).text
    print resString
    #orbFeature()
    scanBook('http://swift-door-556.appspot.com/book7/','Alice In Wonderland')

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
