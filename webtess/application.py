#!/usr/bin/env python
# -*- coding: utf-8 -*-
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table
from flask import Flask, url_for, json, request, Response, jsonify, send_from_directory
from flask_httpauth import HTTPBasicAuth
from flask_dynamo import Dynamo
import datetime
import os
import nltk
import pickle
import codecs
import re


application = Flask(__name__, static_url_path="")
app = application
auth = HTTPBasicAuth()

# ----------------Setting environment variables for DynamoDB-----------------------


app.config['DYNAMO_TABLES'] = [
    Table('passages', schema=[HashKey('passage')]),
]

dynamo = Dynamo(app)
# print datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
try:
    with app.app_context():
        dynamo.create_all()
except:
    pass


@auth.get_password
def get_password(username):
    if username == '******':
        return '******'
    return None

@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401


global tagger
global sent_tokenizer
global PennLabels2
PennLabels2= [('1.0','\n'),('2.0','PRP\n'),('3.0','PRP$\n'),('4.0','CC\n'),('5.0','DT\n'),('6.0','IN\n'),
               ('7.0','RP\n'),('8.0','TO\n'),('9.0','CD\n'),('10.0','EX\n'),('11.0','FW\n'),
               ('12.0','MD\n'),('13.0','PDT\n'),('14.0','POS\n'),('15.0','UH\n'),('16.0','WDT\n'),
               ('17.0','WP\n'),('18.0','WP$\n'),('19.0','WRB\n'),('20.0','')]

global PennLabels1
PennLabels1 = [('1.0','\n'),('2.0','NN\n'),('3.0','NNS\n'),('4.0','NNP\n'),('5.0','NNPS\n'),
                ('6.0','VB\n'),('7.0','VBD\n'),('8.0','VBG\n'),('9.0','VBN\n'),
                ('10.0','VBP\n'),('11.0','VBZ\n'),('12.0','JJ\n'),
                ('13.0','JJR\n'),('14.0','JJS\n'),
                ('15.0','RB\n'),('16.0','RBR\n'),('17.0','RBS\n'),('18.0','')]

global database_attributes
database_attributes = ['passage-extra1','passage-extra2','passage-extra3','passage-extra4','passage-extra5']

data = {}
data['descriptive'] = {}
data['readability'] = {}
data['wordfreq'] = {}
data['pos'] = {}
data['phrases'] = {}
data['mrc'] = {}
worddata = {}
sentsim = {}
passsim = {}

pospickle = open('pos_english.pickle','rb')
tagger = pickle.load(pospickle)

sentencepickle = open('sent_english.pickle','rb')
sent_tokenizer = pickle.load(sentencepickle)


@app.route('/')
@auth.login_required
def get_page():
    return send_from_directory('static','index.html')


@app.route('/main', methods = ['POST'])
@auth.login_required
def evaluate_all():
    Descriptive_eval()
    Readability_eval()
    wf_eval()
    POS_eval()
    chunk_eval()
    MRC_eval()
    ans=jsonify(data)
    passtemp = request.form['passage']
    if len(passtemp) > 2000:
        p1 = passtemp[:2000]
        p2 = passtemp[2000:]
        try:
            temp = dynamo.passages.get_item(passage=p1)
        except:
            dynamo.passages.put_item(data={
                'passage': p1,
                'passage-extra': p2,
                'timestamp': datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),
            })
    else:
        try:
            temp = dynamo.passages.get_item(passage=passtemp)
        except:
            dynamo.passages.put_item(data={
                'passage': passtemp,
                'timestamp': datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),
            })
    return ans, 200


@app.route('/word', methods=['POST'])
@auth.login_required
def worddatatry():
    TheWord = request.form['enterword']
    WordGradeLevels = {}
    with open("WordGradeLevels.txt","r") as f:
        WordGradeLevels = dict((x[0],[x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15],x[16],x[17]]) for x in (x.split('\t') for x in f.read().split('\n') if x))
    f.close()
    AoA = {}
#-----------------------------REQUIRED CHANGE IN FILENAME---------------------------
    with open("MRC-AoA.txt","r") as f:
        Ages = dict((x[0],x[1]) for x in (x.split('\t') for x in f.read().split('\n') if x))

    TheAge = Ages.get(TheWord.lower(),'N/A')
    worddata['age'] = TheAge
    worddata['sfivalue'] = WordGradeLevels[TheWord][0]
    worddata['grade1'] = WordGradeLevels[TheWord][4]
    worddata['grade2'] = WordGradeLevels[TheWord][5]
    worddata['grade3'] = WordGradeLevels[TheWord][6]
    worddata['grade4'] = WordGradeLevels[TheWord][7]
    worddata['grade5'] = WordGradeLevels[TheWord][8]
    worddata['grade6'] = WordGradeLevels[TheWord][9]
    worddata['grade7'] = WordGradeLevels[TheWord][10]
    worddata['grade8'] = WordGradeLevels[TheWord][11]
    worddata['grade9'] = WordGradeLevels[TheWord][12]
    worddata['grade10'] = WordGradeLevels[TheWord][13]
    worddata['grade11'] = WordGradeLevels[TheWord][14]
    worddata['grade12'] = WordGradeLevels[TheWord][15]
    worddata['grade13'] = WordGradeLevels[TheWord][16]
    ans2 = jsonify(worddata)
    return ans2, 200

@app.route('/sent', methods = ['POST'])
@auth.login_required
def senteval():
    from requests import get
    type='relation'
    corpus='webbase'     # corpus can be 'webbase' or 'gigawords'
    s1 = request.form['p1sim']
    s2 = request.form['p2sim']
    sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"

    try:
        response = get(sss_url, params={'operation':'api',
                                        'phrase1':s1,'phrase2':s2,
                                        'type':type,'corpus':corpus})
        SimValue = float(response.text.strip())
        if format(SimValue,'.3f') == "-inf":
            sentsim['simval'] = 'Error in getting similarity'
        else:
            sentsim['simval'] = format(SimValue,'.3f')
    except:
        sentsim['simval'] = 'Error in getting similarity'
    ans3 = jsonify(sentsim)
    return ans3, 200


# @app.route('/pass', methods = ['POST'])
# @auth.login_required
# def passeval():
#     import gensim
#     from gensim.models import word2vec
#
#
#
#     mainpass = request.form['passage']
#     # mainpass = mainpass.replace(u'\u2019',"'")
#     temp = num_sentences(mainpass)
#     model=word2vec.Word2Vec.load('wikipedia_300_sample001_neg_10_iter3')  #changed name of model from wikipedia_300_sample001_neg_10_iter3
#     # model = word2vec.Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
#
#     passsim['p1sim'] = sentences[0]
#     print "sentences: " + sentences[0]
#     # Passage2text = u""
#     Passage2text = request.form['simpassage']
#     # Passage2text = Passage2text.replace(u'\u2019',"'") #replaces curly Unicode apostrophe/single quote
#     print Passage2text
#
#     Passage2sentences = sent_tokenizer.tokenize(Passage2text)
#     passsim['p2sim'] = Passage2sentences[0]
#     print "new sentences : " + Passage2sentences[0]
#     tokens1 = [[]]
#     tokens2 = [[]]
#     tokens1[0] = nltk.word_tokenize(sentences[0])
#     tokens2[0] = nltk.word_tokenize(Passage2sentences[0])
#     passsim['simpassage'] = tokens2[0]   #Changed tokens to token2---------toekns is original
#     SimValue = model.most_similar(tokens1[0],tokens2[0])
#     passsim['simval'] = SimValue
#
#     # passsim['simval'] = format(SimValue,'.3f')
#
#     ans4 = jsonify(passsim)
#     return ans4, 200

def num_sentences(thetext):

    global sentences

    sentences = sent_tokenizer.tokenize(thetext)
    return len(sentences)

def Descriptive_eval():
    global StdWC
    global RealWC
    global AvgCharsPerWord
    global pct_lengths_gt_six
    global AvgSyllsPerWord
    global pct_syll_lengths_gt_two
    global AvgWordsPerSent
    global num_sents
    global type_to_token
    global mtld_value_final
    global thetexttokenized
    global filtered
    global ourbigrams
    global sentences
    global thetext

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

#----------DONE---------REQUIRED CHANGE IN WAY DATA IS SENT---------------------
    # thetext = u""                               #Not Sure if this is required
    thetext = request.form['passage']                # may require change based on front end
    # thetext = thetext.replace(u'\u2019',"'")
    # thetext = thetext.replace(u'\u2019',"'")
    #~~~~~~~~~~~~Tokenizing to words~~~~~~~~~~~~~~~~~~~~~
    #    sentences = nltk.sent_tokenize(thetext)

    re.U
    pattern = ur'''(?x)(?u)      # set flag to allow verbose regexps  ----CORRECT-----
        (?:[A-Za-z]\.)+
        | \d+\/\d+          # fractions            ----PROBLEM-----
        | \d+(?:\w+)?\-(?:\w+)?
        | \d+\°.           # number with a degree symbol       ----PROBLEM-----
        | \$?(?:\d+,)+?(?:\d{3})(?:[^,]|$)
        | \$?\d+(?:\.\d+)?%?
        | \d+\.\d+
        | \w+(?:[-'’/](?:\w+)?)*
        | \d+:\d+
        | (?:[+/\-@&*])
        '''

    ##              | \$?\d{1,3}(\,\d{3})*%? # numbers, incl. currency and percentages
    ##              | \$?\d+(\.\d+)?%?
    ##              |(\d+)(\.\d)*%?

    #^\$?(\d{1,3}(\,\d{3})*|(\d+))(\.\d{1,2})?$
    thetexttokenized = nltk.regexp_tokenize(thetext,pattern)
    filtered = thetexttokenized
    #thetexttokenized = thetexttokenized
    # ourbigrams = nltk.bigrams(thetexttokenized)
    # print(ourbigrams)

    ##    #~~~~Word data~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Syllables = {}

    with open('Sylls.txt','r') as f:
        ##SyllList = [for x in (x.split('\t') for x in f.read().split('\n') if x)]
        ##Syllables = dict(SyllList)
        Syllables = dict((x[0],x[1]) for x in (x.split('\t') for x in f.read().split('\n') if x))

    ##    with open("Sylls.txt","r") as f:
    ##        Syllables = dict((x[0],x[1]) for x in (x.split('\t') for x in f.read().split('\n') if x))
    #~~~~~~~~ACT Standard words (=6 chars)~~~~~~~
    StdWC = len(thetext)/6
    data['descriptive']['stdwordcnt'] = StdWC

    #~~~~~~~~Actual words~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~Number act. wds.
    RealWC = len(thetexttokenized)
    data['descriptive']['realwordcnt'] = RealWC

    sum_char_lengths = 0
    sum_char_lengths_gt_six = 0

    count_of_sylls = 0
    sum_syll_lengths = 0
    sum_syll_lengths_gt_two = 0
    data['descriptive']['wordlengths'] = []
    for token in thetexttokenized:

        char_length = len(token)
        syll_length = Syllables.get(token.lower(),"N/A")

        if syll_length == "N/A" and token[0] in {"1","2","3","4","5","6","7","8","9","0","$"}:
            if token[len(token)-1]=="F":                     #Probably indicating a temperature
                syll_length=2
            else:
                syll_length = 1                             #This version catches things like "135" and "75%"

        sum_char_lengths = sum_char_lengths + char_length

        if syll_length != "N/A":
            count_of_sylls = count_of_sylls + 1
            sum_syll_lengths = sum_syll_lengths + int(syll_length)
            if int(syll_length)>2:
                sum_syll_lengths_gt_two = sum_syll_lengths_gt_two + 1

        if char_length>6:
            sum_char_lengths_gt_six = sum_char_lengths_gt_six + 1

        data['descriptive']['wordlengths'].append({"word" : token, "clength" : str(char_length), "slength" : str(syll_length)})

    AvgCharsPerWord = sum_char_lengths/float(RealWC)
    data['descriptive']['avgcharperword'] = format(AvgCharsPerWord,'.2f')
    # Data_Desc.insert('5.end',format(AvgCharsPerWord,'.2f'))

    pct_lengths_gt_six = round(sum_char_lengths_gt_six/float(RealWC),2)
    data['descriptive']['percent_gt_six'] = str(format((100*pct_lengths_gt_six),'.0f'))
    # Data_Desc.insert('6.end',str(format((100*pct_lengths_gt_six),'.0f'))+'%')

    AvgSyllsPerWord = sum_syll_lengths/float(count_of_sylls)
    data['descriptive']['avgsylls'] = format(AvgSyllsPerWord,'.2f')
    # Data_Desc.insert('10.end',format(AvgSyllsPerWord,'.2f'))

    pct_syll_lengths_gt_two = round(sum_syll_lengths_gt_two/float(count_of_sylls),2)
    data['descriptive']['syll_percent_gt_two'] = str(format((100*pct_syll_lengths_gt_two),'.0f'))
    # Data_Desc.insert('11.end',str(format((100*pct_syll_lengths_gt_two),'.0f'))+'%')


    #~~~~Sentence data ~~~~~~~~~~~~~~~~~~~~~~~~~~~

#    num_sents = len(sentences)
    num_sents = num_sentences(thetext)
    data['descriptive']['totalsents'] = num_sents
    # Data_Desc.insert('15.end',num_sents)

    AvgWordsPerSent = RealWC/float(num_sents)
    data['descriptive']['avgwordpersent'] = format(AvgWordsPerSent,'.2f')
    # Data_Desc.insert('16.end',format(AvgWordsPerSent,'.2f'))


    tokens_lowercased_lst = [word.lower() for word in filtered]    # Use a list comprehension to convert all tokens to lowercase

    #~~~~~~~~type to token
    type_to_token = len(set(tokens_lowercased_lst))/float(len(tokens_lowercased_lst))
    data['descriptive']['typetotoken'] = format(type_to_token,'.2f')
    #Data_LexDiv.insert('3.end',format(type_to_token,'.2f'))

    #~~~~~~~~MTLD

    total_sequences = 0
    current_sequence_count = 0
    current_token_count = 0
    current_sequence_start = 0
    mtld_value_forward=0
    mtld_value_backward=0

    logfile = open('MTLDlogfile.txt', 'w')

    for j in range(2):

        for i in range(len(tokens_lowercased_lst)):
            current_token_count = current_token_count + 1
            current_type_count = len(set(tokens_lowercased_lst[current_sequence_start:i+1]))   #number of types is number of tokens in SET of tokens up to word i
            current_ttr = current_type_count / float(current_token_count)
            current_sequence_count = current_sequence_count + 1

            logfile.write(str(i+1)+"\t")
            logfile.write(tokens_lowercased_lst[i].encode('utf-8')+"\t")
            logfile.write(str(current_token_count)+"\t")
            logfile.write(str(current_type_count)+"\t")
            logfile.write(str(current_ttr)+"\t")
            logfile.write(str(current_sequence_count)+"\n")

            if current_ttr < 0.72:
                current_sequence_start = current_sequence_start + current_token_count
                if current_sequence_count > 10:
                    total_sequences = total_sequences + 1
                current_token_count= 0
                current_sequence_count = 0

        remainder = (1-current_ttr)/(1-0.72)
        total_sequences = total_sequences + remainder

        if j==0:
            mtld_value_forward = len(tokens_lowercased_lst)/float(total_sequences)
        else:
            mtld_value_backward = len(tokens_lowercased_lst)/float(total_sequences)

        tokens_lowercased_lst.reverse()
        total_sequences = 0
        current_sequence_count = 0
        current_token_count = 0
        current_sequence_start = 0

    logfile.close()

    mtld_value_final = (mtld_value_forward + mtld_value_backward)/2
    data['descriptive']['mtld'] = str(format(mtld_value_final,'.2f'))
    # Data_LexDiv.insert('4.end',str(format(mtld_value_final,'.2f')))

    # Data_Desc.configure(state='disabled')
    # Data_LexDiv.configure(state='disabled')
    # Unigram_WordList_Desc.configure(state='disabled')
    # Unigram_WordList_Read.configure(state='disabled')

#~~~~~~~~~~~~~~ Functionality: Readability ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def Readability_eval():

    # Data_Read.configure(state='normal')
#    Unigram_WordList_Read(state='normal')

    # Data_Read.delete(1.0,END)

    # for i in range(18):
    #     Data_Read.insert(txtlines[i],'\n')

#Flesch-Kincaid Grade Level
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    FKGLIndex = (0.39 * AvgWordsPerSent)+(11.8 * AvgSyllsPerWord) - 15.59
    data['readability']['fkglindex'] = format(FKGLIndex,'.2f')
    # Data_Read.insert('3.0',format(FKGLIndex,'.2f'))
    FKGL_CCGrade = "N/A"

#Flesch-Kincaid Grade Level conversions to CC Grade:
    if FKGLIndex>14.21:
        FKGL_CCGrade = "13+"
    elif FKGLIndex>13.17:
        FKGL_CCGrade = "12"
    elif FKGLIndex>12.13:
        FKGL_CCGrade = "11"
    elif FKGLIndex>11.24:
        FKGL_CCGrade = "10"
    elif FKGLIndex>10.35:
        FKGL_CCGrade = "9"
    elif FKGLIndex>9.48:
        FKGL_CCGrade = "8"
    elif FKGLIndex>8.61:
        FKGL_CCGrade = "7"
    elif FKGLIndex>7.74:
        FKGL_CCGrade = "6"
    elif FKGLIndex>6.55:
        FKGL_CCGrade = "5"
    elif FKGLIndex>5.35:
        FKGL_CCGrade = "4"
    elif FKGLIndex>3.67:
        FKGL_CCGrade = "3"
    elif FKGLIndex>1.98:
        FKGL_CCGrade = "2"
    elif FKGLIndex>0.0:
        FKGL_CCGrade = "1"
    else:
        FKGL_CCGrade = "<1"

    data['readability']['fkglgrade'] = FKGL_CCGrade
    #Data_Read.insert('4.0',FKGL_CCGrade)

#Flesch Reading Ease
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    FREIndex = 206.835 - (1.015 * AvgWordsPerSent) - (84.6 * AvgSyllsPerWord)
    data['readability']['freindex'] = format(FREIndex,'.2f')
    # Data_Read.insert('9.0',format(FREIndex,'.2f'))
    FREGrade = "N/A"

    if FREIndex<30:
        FREGrade = "16+"
    elif FREIndex<50:
        FREGrade = "13-16"
    elif FREIndex<60:
        FREGrade = "10-12"
    elif FREIndex<70:
        FREGrade = "8-9"
    elif FREIndex<80:
        FREGrade = "7"
    elif FREIndex<90:
        FREGrade = "6"
    elif FREIndex<100:
        FREGrade = "5"
    else:
        FREGrade = "<5"

    # Data_Read.insert('10.0',FREGrade)
    data['readability']['fregrade'] = FREGrade

#Coleman-Liau
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ColemanIndex = (0.0588 * (AvgCharsPerWord*100)) - (0.296 * (100/AvgWordsPerSent)) - 15.8
    data['readability']['colemanindex'] = format(ColemanIndex,'.2f')
    # Data_Read.insert('12.0',format(ColemanIndex,'.2f'))

    ColemanGrade = "N/A"

#Coleman-Liau conversions to grade:
    if ColemanIndex<0.5:
        ColemanGrade = "K"
    elif ColemanIndex<1.5:
        ColemanGrade = "1"
    elif ColemanIndex<2.5:
        ColemanGrade = "2"
    elif ColemanIndex<3.5:
        ColemanGrade = "3"
    elif ColemanIndex<4.5:
        ColemanGrade = "4"
    elif ColemanIndex<5.5:
        ColemanGrade = "5"
    elif ColemanIndex<6.5:
        ColemanGrade = "6"
    elif ColemanIndex<7.5:
        ColemanGrade = "7"
    elif ColemanIndex<8.5:
        ColemanGrade = "8"
    elif ColemanIndex<9.5:
        ColemanGrade = "9"
    elif ColemanIndex<10.5:
        ColemanGrade = "10"
    elif ColemanIndex<11.5:
        ColemanGrade = "11"
    elif ColemanIndex<100:
        ColemanGrade = "12"
    else:
        ColemanGrade = "12+"

    data['readability']['colemangrade'] = ColemanGrade
    # Data_Read.insert('13.0',ColemanGrade)


#~~~Dale-Chall~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    DaleChallFile = open('DClist.txt','r')
    DCwordlist = [line.strip() for line in DaleChallFile]

    DCwords = 0
    NonDCwords = 0

    for word in filtered:
        if word.lower() in DCwordlist:
            DCwords = DCwords + 1
        else:
            NonDCwords = NonDCwords + 1

    PCTDCwords = float(DCwords)/len(filtered)
    PCTNonDCwords = float(NonDCwords)/len(filtered)

    data['readability']['dcwords'] = format(PCTDCwords,'.2f')
    data['readability']['nondcwords'] = format(PCTNonDCwords,'.2f')
    # Data_Read.insert('17.0',format(PCTDCwords,'.2f'))
    # Data_Read.insert('18.0',format(PCTNonDCwords,'.2f'))

    DCIndex = 15.79 * PCTNonDCwords + (0.0496 * AvgWordsPerSent) + 3.6365
    data['readability']['dcindex'] = format(DCIndex,'.2f')
    # Data_Read.insert('15.0',format(DCIndex,'.2f'))

    DCGrade = "N/A"

#Dale-Chall conversions to grade:
    if DCIndex<4.9:
        DCGrade = "K-4"
    elif DCIndex<5.9:
        DCGrade = "5-6"
    elif DCIndex<6.9:
        DCGrade = "7-8"
    elif DCIndex<7.9:
        DCGrade = "9-10"
    elif DCIndex<8.9:
        DCGrade = "11-12"
    elif DCIndex<9.9:
        DCGrade = "13-15"
    elif DCIndex<100:
        DCGrade = "16"

    # Data_Read.insert('16.0',DCGrade)
    data['readability']['dcgrade'] = DCGrade
#~~Degrees of Reading Power~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    DRPIndex = 100 * (1 - (0.886593 - (0.08364 * AvgCharsPerWord) + (0.161911 * (PCTDCwords**3)) - (0.021401 * AvgWordsPerSent) + (0.000577 * (AvgWordsPerSent**2)) - (0.000005 * (AvgWordsPerSent**3))))

    # Data_Read.insert('6.0',format(DRPIndex,'.2f'))
    data['readability']['drpindex'] = format(DRPIndex,'.2f')

    DRPGrade = "N/A"

#DRP conversions to grade:
    if DRPIndex<42:
        DRPGrade = "1"
    elif DRPIndex<47:
        DRPGrade = "2"
    elif DRPIndex<52:
        DRPGrade = "3"
    elif DRPIndex<54.5:
        DRPGrade = "4"
    elif DRPIndex<57:
        DRPGrade = "5"
    elif DRPIndex<58.67:
        DRPGrade = "6"
    elif DRPIndex<60.33:
        DRPGrade = "7"
    elif DRPIndex<62:
        DRPGrade = "8"
    elif DRPIndex<64.5:
        DRPGrade = "9"
    elif DRPIndex<67:
        DRPGrade = "10"
    elif DRPIndex<71:
        DRPGrade = "11"
    elif DRPIndex<75:
        DRPGrade = "12"
    elif DRPIndex<100:
        DRPGrade = "13+"

    data['readability']['drpgrade'] = DRPGrade
    # Data_Read.insert('7.0',DRPGrade)
    #
    # Data_Read.configure(state='disabled')
#    Unigram_WordList_Read(state='disabled')

# ---------------Functionality - Word Frequency-----------

def wf_eval():

#Function for calculating word freq distribution percentiles:
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def percentile(N,P):
        '''
        Find the percentile of a list of values
        N: The list of values. Must be sorted!
        P: The percentile. Float from 0.0 to 1.0.
        Return: The percentile of the values -
           i.e., the list value below which P percent of list values are found.
        '''
        n = int(round(P * len(N) + 0.5))
        return N[n-1]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#     Data_wf.configure(state='normal')
#     WF_WordList.configure(state='normal')
#     LowFreqWords.configure(state='normal')
#
#     Data_wf.delete(1.0,END)
#
#     for i in range(9):
#         Data_wf.insert(txtlines[i],'\n')
#
#     LowFreqWords.delete(1.0,END)
#     LowFreqWords.insert('1.0','Lowest-frequency words\n')
#     for i in range(2,7):
#         LowFreqWords.insert(txtlines[i],'\n')
#
# #    thetext = Passage_text.get(1.0,END).lower()
#     WF_WordList.delete(1.0,END)
#     WF_WordList.insert(END,"Word"+'\t'+'\t'+"SFI"+'\n')   #Column headers

    WordFreqs = {}             #dictionary of words and their lemmas
    BigramFreqs = {}

    with open("WordSFIs.txt", "r") as f:
        WordFreqs = dict((x[0], x[1]) for x in (x.split('\t') for x in f.read().split('\n') if x))

    with open("w2_non-cs.txt","r") as f2:
        BigramFreqs = dict((x[1]+' '+x[2],x[0]) for x in (x.split('\t') for x in f2.read().split('\n') if x))

    count_of_freqs = 0
    sum_of_freqs = 0

    freqlist = [[] for k in range(len(filtered))]
    freqsonly = []

##    print ourbigrams[0]
##    print ourbigrams[0][0] + ' ' + ourbigrams[0][1]
##    print(BigramFreqs.get(ourbigrams[0][0].lower()+' '+ourbigrams[0][1].lower()))


##    for i in range(len(ourbigrams)):
##        textbigram = ourbigrams[i][0]+' '+ourbigrams[i][1]
##        bigramfreq = BigramFreqs.get(textbigram.lower())
##        if bigramfreq == None:
##            bigramfreq = 'N/A'
##        print(textbigram + '\t' + bigramfreq)
    data['wordfreq']['sfiwords'] = []
    for i in range(len(filtered)):
        freqlist[i].append(filtered[i].lower())
        freqlist[i].append(WordFreqs.get(filtered[i].lower(),"N/A"))
        if freqlist[i][1]!='N/A':
            freqlist[i][1]=str(float(freqlist[i][1]))
        data['wordfreq']['sfiwords'].append({"sfword" : freqlist[i][0].lower(), "sfi" : freqlist[i][1]})
        # WF_WordList.insert(END,freqlist[i][0].lower()+'\t'+'\t'+ freqlist[i][1]+'\n')
        if freqlist[i][1]!="N/A":
            freqlist[i][1] = float(freqlist[i][1])

        if freqlist[i][1]!="N/A":
#            tkMessageBox.showinfo(count_of_freqs)
            freqsonly.append(float(freqlist[i][1]))
            count_of_freqs = count_of_freqs + 1
            sum_of_freqs = sum_of_freqs + float(freqlist[i][1])

    mean_freq = sum_of_freqs/float(count_of_freqs)
    data['wordfreq']['meansfi'] = format(mean_freq,'.2f')
    # Data_wf.insert('3.0',format(mean_freq,'.2f'))

    #Sort freqlist on index 1:
    freqlist.sort(key=lambda x: x[1])       #Got this from stackoverflow, 'sorting list of lists by an index'

    freqsonly.sort()

    min_wf = percentile(freqsonly,.00)
    p25_wf = percentile(freqsonly,.25)
    med_wf = percentile(freqsonly,.50)
    p75_wf = percentile(freqsonly,.75)
    max_wf = percentile(freqsonly,.99)

    data['wordfreq']['minsfi'] = format(min_wf,'.2f')
    data['wordfreq']['p25sfi'] = format(p25_wf,'.2f')
    data['wordfreq']['mediansfi'] = format(med_wf,'.2f')
    data['wordfreq']['p75sfi'] = format(p75_wf,'.2f')
    data['wordfreq']['maxsfi'] = format(max_wf,'.2f')

    # Data_wf.insert('5.0',format(min_wf,'.2f'))
    # Data_wf.insert('6.0',format(p25_wf,'.2f'))
    # Data_wf.insert('7.0',format(med_wf,'.2f'))
    # Data_wf.insert('8.0',format(p75_wf,'.2f'))
    # Data_wf.insert('9.0',format(max_wf,'.2f'))


    data['wordfreq']['lowfreqwords'] = []
    data['wordfreq']['lowfreqwords'].append({"lword" : str(freqlist[0][1]), "freq" : freqlist[0][0]})
    data['wordfreq']['lowfreqwords'].append({"lword" : str(freqlist[1][1]), "freq" : freqlist[1][0]})
    data['wordfreq']['lowfreqwords'].append({"lword" : str(freqlist[2][1]), "freq" : freqlist[2][0]})
    data['wordfreq']['lowfreqwords'].append({"lword" : str(freqlist[3][1]), "freq" : freqlist[3][0]})
    data['wordfreq']['lowfreqwords'].append({"lword" : str(freqlist[4][1]), "freq" : freqlist[4][0]})


    # LowFreqWords.insert('3.0',str(freqlist[0][1])+'   \t' + freqlist[0][0])
    # LowFreqWords.insert('4.0',str(freqlist[1][1])+'   \t' + freqlist[1][0])
    # LowFreqWords.insert('5.0',str(freqlist[2][1])+'   \t' + freqlist[2][0])
    # LowFreqWords.insert('6.0',str(freqlist[3][1])+'   \t' + freqlist[3][0])
    # LowFreqWords.insert('7.0',str(freqlist[4][1])+'   \t' + freqlist[4][0])

    # Data_wf.configure(state='disabled')
    # WF_WordList.configure(state='disabled')
    # LowFreqWords.configure(state='disabled')

#~~~~~~~~~~~~~~~ Functionality: Parts of Speech ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def POS_eval():

    global POS_document
    global taggedsentences

    # POS_WordList.configure(state='normal')
    # Data_LexDens.configure(state='normal')
    # Data_PennDefns1.configure(state='normal')
    # Data_PennDefns2.configure(state='normal')

    # POS_WordList.delete(1.0,END)
    # Data_LexDens.delete(1.0,END)
    # Data_PennDefns1.delete(1.0,END)
    # Data_PennDefns2.delete(1.0,END)

##    thetext = Passage_text.get(1.0,END)

    # for i in range(17):
    #     Data_PennDefns1.insert(txtlines[i],'\n')
    # for i in range(19):
    #     Data_PennDefns2.insert(txtlines[i],'\n')

    possentences = sent_tokenizer.tokenize(thetext)

    re.U
    pattern = ur'''(?x)(?u)      # set flag to allow verbose regexps  ----CORRECT-----
        (?:[A-Za-z]\.)+
        | \d+\/\d+          # fractions            ----PROBLEM-----
        | \d+(?:\w+)?\-(?:\w+)?
        | \d+\°.           # number with a degree symbol       ----PROBLEM-----
        | \$?(?:\d+,)+?(?:\d{3})(?:[^,]|$)
        | \$?\d+(?:\.\d+)?%?
        | \d+\.\d+
        | \w+(?:[-'’/](?:\w+)?)*
        | \d+:\d+
        | (?:[+/\-@&*])
        '''

##              | \$?\d{1,3}(\,\d{3})*%? # numbers, incl. currency and percentages
##              | \$?\d+(\.\d+)?%?
##              |(\d+)(\.\d)*%?

#^\$?(\d{1,3}(\,\d{3})*|(\d+))(\.\d{1,2})?$

    possentences = [nltk.regexp_tokenize(sent,pattern) for sent in possentences]

    #See top of code for loading of tagger
    s=''
    taggedsentences = [tagger.tag(sent) for sent in possentences]
    data['pos']['wordparts'] = []
    for sent in taggedsentences:
        for POS_word in sent:
            word, part = POS_word
            data['pos']['wordparts'].append({"pword" : word, "part" : part})
            s += word+'\t'+'\t'+part+'\n'
            # POS_WordList.insert(END, word+'\t'+'\t'+part+'\n')


#-------------POTENTIAL CHANGES-------------------DOUBTS
    POS_WordList_string = s
    # POS_WordList_string = POS_WordList.get(1.0,END)

    thiscount = 0           #the count for the current POS
    totallex = 0            #running total of count for lexical POSs
    totalnonlex = 0         #running total of count for nonlexical POSs
    lexical_density = 0
    postemp1 = ['','nn','nns','nnp','nnps','vb','vbd','vbg','vbn','vbp','vbz','jj','jjr','jjs','rb','rbr','rbs','']
    postemp2 = ['','prp','prp$','cc','dt','in','rp','to','cd','ex','fw','md','pdt','pos','uh','wdt','wp','wp$','wrb','']
    posinfo1 = ['','Noun, Singular or Mass','Noun, Plural','Proper Noun, Singular','Proper Noun, Plural','Verb, Base Form','Verb, Past Tense','Verb, Gerund or Present Participle','Verb, Past Participle','Verb, Non-3rd Person Singular Present','Verb, 3rd Person Singular Present','Adjective','Adjective, Comparative','Adjective, Superlative','Adverb','Adverb, Comparative','Adverb, Superlative','']
    posinfo2 = ['','Personal Pronoun','Possessive Pronoun','Coordinating Conjunction','Determiner','Preposition','Participle','To','Cardinal Number','Existential There','Foreign Word','Modal','Predeterminer','Possessive Ending','Interjection','Wh-Determiner','Wh-Pronoun','Possessive Wh-Pronoun','Wh-Adverb','']
    PennCounts = []
    data['pos']['lex']={}
    data['pos']['nonlex']={}


# ---------------------POTENTIAL DOUBLE CHECK---<RANGE CHANGES> MADE 17 to 18 and 19 to 18, also carried CC from part2 to part1---------------------------
    for i in range(1,17):
        thiscount = POS_WordList_string.count('\t'+PennLabels1[i][1])
        thispct = str(format(100.0*thiscount/RealWC,'.0f'))+'%'
        data['pos']['lex'][postemp1[i]] = {}
        data['pos']['lex'][postemp1[i]]['count'] = str(thiscount)
        data['pos']['lex'][postemp1[i]]['pct'] = thispct
        data['pos']['lex'][postemp1[i]]['info'] = posinfo1[i]
        # Data_PennDefns1.insert(PennLabels1[i][0],str(thiscount)+'\t'+thispct)
        totallex = totallex + thiscount

    thiscount=0

    for i in range(1,19):
        thiscount = POS_WordList_string.count('\t'+PennLabels2[i][1])
        thispct = str(format(100.0*thiscount/RealWC,'.0f'))+'%'
        data['pos']['nonlex'][postemp2[i]] = {}
        data['pos']['nonlex'][postemp2[i]]['count'] = str(thiscount)
        data['pos']['nonlex'][postemp2[i]]['pct'] = thispct
        data['pos']['nonlex'][postemp2[i]]['info'] = posinfo2[i]

        # Data_PennDefns2.insert(PennLabels2[i][0],str(thiscount)+'\t'+thispct)
        totalnonlex = totalnonlex + thiscount

    lexical_density = totallex/float(totallex + totalnonlex)
    data['pos']['lexden'] = format(lexical_density,'.2f')
    # Data_LexDens.insert('1.0', format(lexical_density,'.2f'))

    # POS_WordList.configure(state='disabled')
    # Data_LexDens.configure(state='disabled')
    # Data_PennDefns1.configure(state='disabled')
    # Data_PennDefns2.configure(state='disabled')

##def spell_correct():        #awaiting code
##    pass


#~~~~~~~~~~~~~~~ Functionality: Chunking ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def chunk_eval():

    # Chunk_WordList.configure(state='normal')
    # Data_Chunk.configure(state='normal')
    #
    # Chunk_WordList.delete(1.0,END)
    # Data_Chunk.delete(1.0,END)


#----------------------POTENTIAL DOUBLE CHECK IF REQUIRED----------------------
    # thetext = Passage_text.get(1.0,END)

    #Replace pesky Unicode curly apostrophe/single quote~~~~~~
    # thetext = thetext.replace(u'\u2019',"'")
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # for i in range(6):
    #     Data_Chunk.insert(txtlines[i],'\n')

    chunksentences = sent_tokenizer.tokenize(thetext)

    re.U
    pattern = ur'''(?x)(?u)      # set flag to allow verbose regexps  ----CORRECT-----
        (?:[A-Za-z]\.)+
        | \d+\/\d+          # fractions            ----PROBLEM-----
        | \d+(?:\w+)?\-(?:\w+)?
        | \d+\°.           # number with a degree symbol       ----PROBLEM-----
        | \$?(?:\d+,)+?(?:\d{3})(?:[^,]|$)
        | \$?\d+(?:\.\d+)?%?
        | \d+\.\d+
        | \w+(?:[-'’/](?:\w+)?)*
        | \d+:\d+
        | (?:[+/\-@&*])
        '''

##              | \$?\d{1,3}(\,\d{3})*%? # numbers, incl. currency and percentages
##              | \$?\d+(\.\d+)?%?
##              |(\d+)(\.\d)*%?

#^\$?(\d{1,3}(\,\d{3})*|(\d+))(\.\d{1,2})?$

    chunksentences = [nltk.regexp_tokenize(sent,pattern) for sent in chunksentences]

    #See top of code for loading of tagger
    taggedsentences = [tagger.tag(sent) for sent in chunksentences]
#    sentences = [nltk.pos_tag(sent) for sent in sentences]

    grammar = r"""
      NP: {<DT>?<JJ.*>*<NN.*>+} # Noun phrase pattern
      PP: {<IN><NP>}         # Chunk prepositions followed by NP
      VP: {<MD>?<VB.*><NP|PP|CLAUSE>+}  # Chunk verbs and their arguments
      CLAUSE: {<NP><VP>}    # Chunk NP, VP
      """
#      NP: {<DT|JJ|NN.*>+}    # Chunk sequences of DT, JJ, NN

    cp=nltk.RegexpParser(grammar, loop=2)
    #print(taggedsentences)

#-------------------------POTENTIAL DEBUG----------------------------
    chunk_string=''
    for sent in taggedsentences:
        chunk_tree = cp.parse(sent)
        chunk_string += str(chunk_tree) + '\n'
        # Chunk_WordList.insert(END,chunk_tree)
        # Chunk_WordList.insert(END,'\n')

    data['phrases']['tree'] = chunk_string
    # Chunk_WordList_string = Chunk_WordList.get(1.0,END)
    Chunk_WordList_string = chunk_string
    NPcount = Chunk_WordList_string.count('(NP ')
    VPcount = Chunk_WordList_string.count('(VP ')
    PPcount = Chunk_WordList_string.count('(PP ')

    data['phrases']['npcount'] = NPcount
    data['phrases']['vpcount'] = VPcount
    data['phrases']['ppcount'] = PPcount
    # Data_Chunk.insert('3.0',NPcount)
    # Data_Chunk.insert('4.0',VPcount)
    # Data_Chunk.insert('5.0',PPcount)
    #
    # Chunk_WordList.configure(state='disabled')
    # Data_Chunk.configure(state='disabled')

# ~~~~~~~~~~~~~~~~~~~~~~~~~Functionality MRC~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def MRC_eval():

    # Unigram_WordList_MRC.configure(state='normal')
    # Unigram_WordList_MRC.delete(1.0,END)
    # Data_MRC.configure(state='normal')
    # Data_MRC.delete(1.0,END)
    # for i in range(12):
    #     Data_MRC.insert(txtlines[i],'\n')

    #Create AoA dictionary from file:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Dict_AoA = {}
    count_AoA=0
    sum_AoA=0
    with open("MRC-AoA.txt","r") as f:
        Dict_AoA = dict((x[0],x[1]) for x in (x.split('\t') for x in f.read().split('\n') if x))

    #Create Familiarity dictionary from file:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Dict_Fam = {}
    count_Fam=0
    sum_Fam=0
    with open("MRC-Fam.txt","r") as f:
        Dict_Fam = dict((x[0],x[1]) for x in (x.split('\t') for x in f.read().split('\n') if x))

    #Create Imagability dictionary from file:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Dict_Imag = {}
    count_Imag=0
    sum_Imag=0
    with open("MRC-Imag.txt","r") as f:
        Dict_Imag = dict((x[0],x[1]) for x in (x.split('\t') for x in f.read().split('\n') if x))

    #Create Concreteness dictionary from file:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Dict_Conc = {}
    count_Conc=0
    sum_Conc=0
    with open("MRC-Conc.txt","r") as f:
        Dict_Conc = dict((x[0],x[1]) for x in (x.split('\t') for x in f.read().split('\n') if x))

    #Create Meaningfulness dictionary from file:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Dict_Mean = {}
    count_Mean=0
    sum_Mean=0
    with open("MRC-Mean.txt","r") as f:
        Dict_Mean = dict((x[0],x[1]) for x in (x.split('\t') for x in f.read().split('\n') if x))

    data['mrc']['dictionary'] = []
    for sent in taggedsentences:
        for POS_word in sent:
            word, part = POS_word
            AoA_val = '*'
            Fam_val = '*'
            Imag_val= '*'
            Conc_val = '*'
            Mean_val = '*'
            if (part[0]=='N' or part[0]=='V'):
                AoA_val = Dict_AoA.get(word.lower(),'*')
                Fam_val = Dict_Fam.get(word.lower(),'*')
                Imag_val= Dict_Imag.get(word.lower(),'*')
                Conc_val = Dict_Conc.get(word.lower(),'*')
                Mean_val = Dict_Mean.get(word.lower(),'*')

                data['mrc']['dictionary'].append({"word" : word, "aoa" : AoA_val, "fam" : Fam_val, "imag" : Imag_val, "conc" : Conc_val, "mean" : Mean_val})
                # Unigram_WordList_MRC.insert(END, word+'\t'+'\t'+AoA_val+'\t'+Fam_val+'\t'
                #                             + Imag_val + '\t' + Conc_val + '\t' + Mean_val + '\n')

            if AoA_val <> "*":
                count_AoA = count_AoA + 1
                sum_AoA = sum_AoA + int(AoA_val)
            if Fam_val <> "*":
                count_Fam = count_Fam + 1
                sum_Fam = sum_Fam + int(Fam_val)
            if Imag_val <> "*":
                count_Imag = count_Imag + 1
                sum_Imag = sum_Imag + int(Imag_val)
            if Conc_val <> "*":
                count_Conc = count_Conc + 1
                sum_Conc = sum_Conc + int(Conc_val)
            if Mean_val <> "*":
                count_Mean = count_Mean + 1
                sum_Mean = sum_Mean + int(Mean_val)

    AoA_mean = sum_AoA/float(count_AoA)
    Fam_mean = sum_Fam/float(count_Fam)
    Imag_mean = sum_Imag/float(count_Imag)
    Conc_mean = sum_Conc/float(count_Conc)
    Mean_mean = sum_Mean/float(count_Mean)

    data['mrc']['aoamean'] = format(AoA_mean,'.0f')
    data['mrc']['fammean'] = format(Fam_mean,'.0f')
    data['mrc']['imagmean'] = format(Imag_mean,'.0f')
    data['mrc']['concmean'] = format(Conc_mean,'.0f')
    data['mrc']['meanmean'] = format(Mean_mean,'.0f')
    # Data_MRC.insert('3.end',format(AoA_mean,'.0f'))
    # Data_MRC.insert('5.end',format(Fam_mean,'.0f'))
    # Data_MRC.insert('7.end',format(Imag_mean,'.0f'))
    # Data_MRC.insert('9.end',format(Conc_mean,'.0f'))
    # Data_MRC.insert('11.end',format(Mean_mean,'.0f'))
    #
    # Unigram_WordList_MRC.configure(state='disabled')
    # Data_MRC.configure(state='disabled')







if __name__ == '__main__':
    app.run(host="127.0.0.1",port=int("5000"),debug=True)