import pandas as pd
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re
import random
import string
import warnings
warnings.simplefilter("ignore")
from textblob import TextBlob
from PyPDF2 import PdfReader
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from multiprocessing import pool

class ExamGerator():
    def __init__(self, path):
        self.path = path
        self.status = False
        self.notes = ''
        self.topic = ''
        self.procesed_doc= ''
        self.raw_doc1 = ''
        self.final_doc = ''
        self.notes_full ={'topic':[], 'notes':[]}
        self.procesed_sent= []
        self.final_sent_token = []
        self.sent_tokens =[]
        self.word_tokens = []

    def doc_opening(self):
        for pth in self.path:
            _, extenstion = pth.split('.')
            print('doc openiing')

            if extenstion == 'txt':
                with open(pth,'rb') as f:
                    for line in f:
                        line = str(line)[1:]
                        self.raw_doc1 +=line
                        # extracting chapter pages

                        for word in line.split(' '):
                            if word == 'chapter':
                                self.notes_full['topic'].append(self.topic)
                                self.notes_full['notes'].append(self.notes)
                                self.topic = line
                                self.notes = ''
                                self.status = True
                        if self.status:
                            self.notes +=line

            elif extenstion == 'pdf':
                pdf = PdfReader(pth)
                for index, page in enumerate(pdf.pages):
                    page = pdf.pages[index]
                    self.raw_doc1 += page.extract_text()
            else:
                self.raw_doc1 = ''
        return self.raw_doc1


    def doc_cleaning(self):
        print('doc cleaning')

        for initial in str(self.raw_doc1):
            data_given = ""
            if initial == string.punctuation[23]:
                data_given = " "
            else:
                data_given = initial
            self.procesed_doc +=data_given
            self.procesed_doc = self.procesed_doc.replace('r n', '')
            self.procesed_doc = self.procesed_doc.replace("''", '')
            self.sent_tokens = nltk.sent_tokenize(self.procesed_doc.lower())
        self.word_tokens = nltk.word_tokenize(self.procesed_doc.lower())
        # nltk.download('stopwords')
        stop_words = set(stopwords.words('english'))
        filtered_token = [token for token in self.word_tokens if token not in stop_words]
        raw_doc =self.final_doc
        return self.procesed_doc

    # Find synonyms
    def similar_words(self,word):
        synonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.name() != word:
                    synonyms.append(lemma.name())
        return set(synonyms)

    # Find antonyms
    def opposite_words(self, word):
        antonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                for antonym in lemma.antonyms():
                    antonyms.append(antonym.name())
        return set(antonyms)

    def response(self, user_response):
        robol_response = ''
        tifidvec = TfidfVectorizer(tokenizer=LemNormalizer, stop_words='english')
        tfid = tifidvec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfid[-1], tfid)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tif = flat[-2]
        if (req_tif == 0):
            robol_response = robol_response + "I am sorry, i can't understand you"
            return robol_response
        else:
            robol_response = robol_response + self.sent_tokens[idx]
            self.sent_tokens.remove(self.sent_tokens[idx])
            return robol_response

    def chicking_doc_tags(self):
        print('checking tags')
        text = TextBlob(self.procesed_doc)
        tags = text.tags
        no_words = len(tags)
        words_dict = {'word':[], 'tag':[]}
        previous_word, previous_tag = 'ml', 'NN'
        sentence_words = ''
        for i in range(no_words+1):
            status = False
            try:
                tag_word = tags[i][1]
            #         print(tags[i],tags[i+1]
                if tag_word == tags[i-1][1]:
                    sentence_words += tags[i-1][0]+' '
                else:
                    sentence_words+=tags[i-1][0]
                    status =True

                if status:
                    words_dict['word'].append(sentence_words)
                    words_dict['tag'].append(tags[i-1][1])
                    sentence_words = ''

            except:
                pass
        data_word = pd.DataFrame(words_dict)
        data_word.drop_duplicates(inplace= True)
        return data_word

    def serching_keywords(self, sentence, key_words, nn_number = 4, qn_index = 1, ans_index =0):
        print('searching keywords')
        qn = []
        ans = []
        for idx,row_sent in enumerate(sentence):
            previous_text = ''
            status = True
            for row in row_sent.split(' '):
                words_complit = ''
                value = 0
                for key_word in key_words:
                    if key_word == row:
                        words_complit +=key_word + " "
                        text = TextBlob(row_sent.split(key_word)[qn_index])
                        tqns_tags = text.tags
                        tag_arry = [tag[1] for tag in tqns_tags]
                        for  index, tag_qn in enumerate(tag_arry):
                            if tag_arry[index] == 'NN' or tag_arry[index] == 'NNS':
                                value +=1

                            extracted_symbol = ['.', ':', ";", ',']
                            symbols = [symbol for symbol in  extracted_symbol for tex in tqns_tags[index][0] if symbol == tex]
                            if value >nn_number or len(symbols)>0:
                                status = False
                            if status:
                                words_complit +=tqns_tags[index][0] + ' '
                        ans.append(row_sent.split(key_word)[ans_index])
                        qn.append(words_complit)
        # qn = list(set(qn))
        # ans= list(set(ans))
        return qn, ans

    def generate_exams(self, type_exam, no_questions = 50):
        flag = True
        Qn_generated= ''
        ans = ''
        definitions =  ['refers to', 'is defined as', 'process', 'is called', 'known as', 'what is' ]
        definitions_modified = []
        ended_qns_dfns = ['called', 'known as', 'reffered to']
        questions = []
        answers = []
        qn_combined = []
        ans_combined = []
        filling_blank = ['NN', 'NNS']
        short_notes = ['NN', 'NNS']
        no_questions_generated =0
        Qn_generated = ''
        ans_generated = ''
        selection = 0
        cleaned = self.doc_cleaning()
        data_word = self.chicking_doc_tags()
        for dtn in definitions:
            similar = self.similar_words(dtn)
        for sim in similar:
            definitions_modified.append(sim)
        while flag:
            if no_questions_generated == no_questions:
                flag = False
            if type_exam == 'multiple_coice':
                print('ok')
            elif type_exam == 'Match item':
                print('ok')
            elif type_exam == 'True':
                print('ok')
            elif type_exam == 'fill the blanks':
                text = ""
                solution = ""
                status = False
                sentence = random.choice(self.sent_tokens)
                index_sentece = self.sent_tokens.index(sentence)
                text += self.sent_tokens[index_sentece-1] +' '
                text_with_tag = TextBlob(sentence).tags
                tag_selection = random.choice(filling_blank)

                for tx in text_with_tag:
                    if tx[1] == tag_selection:
                        status = True
                    if status:
                        solution = tx[0]
                        tx = '......'
                    text +=tx[0] + ' '
                if not status:
                    print('empty')
                else:
                    questions.append(text)
                    answers.append(solution)

            elif type_exam == 'Short Note':

                if selection<=no_questions_generated/3:
                    type_word_selected = random.choice(short_notes)
                    words_df_len = data_word[data_word['tag']== type_word_selected]['word'].shape[0]
                    index_choosen = random.randint(0, words_df_len-1)
                    Qn_generated= data_word[data_word['tag']== type_word_selected]['word'].iloc[index_choosen]
                elif selection >(no_questions_generated/3) and selection<(no_questions_generated*2)/3:

                    # Define a regular expression pattern to match revision questions
                    pattern = r'^[Ww]hat |^[Ww]hy |^[Hh]ow |^[Dd]escribe |^[Ee]xplain '

                    # Create an empty list to store the revision questions
                    revision_questions = []

                    # Loop through each sentence and check if it matches the pattern
                    for sentence in self.sent_tokens:
                        if re.match(pattern, sentence):
                            revision_questions.append(sentence)
                    Qn_generated = random.choice(revision_questions)
                else:
                    qn1, ans1 = self.serching_keywords(sentence= self.sent_tokens, key_words= ended_qns_dfns, nn_number = 10, qn_index = 0, ans_index =1)
                    qn2, ans2 = self.serching_keywords(self.sent_tokens,definitions_modified, 2)
                    qn_combined = [qn1, qn2]
                    ans_combined = [ans1, ans2]
                    random_index = random.randint(0,2)
                    if random_index ==1:
                        try:
                            Qn_generated = random.choice(qn1)
                        except:
                            pass
                        try:
                            ans_generated = random.choice(ans1)
                        except:
                            pass
                    else:
                        try:
                            Qn_generated = random.choice(qn2)
                        except:
                            pass
                        try:
                            ans_generated = random.choice(ans2)
                        except:
                            pass
                try:
                    qn = random.choice(qn_combined)
                    Qn_generated = random.choice(qn)
                except:
                    pass
                try:
                    ans = random.choice(ans_combined)
                    ans_generated = random.choice(ans)
                except:
                    pass

                if Qn_generated == "" or ans_generated == '':
                    print('empty')
                else:
                    questions.append(Qn_generated)
                    answers.append(ans_generated)
                selection +=1
                if selection ==no_questions_generated:
                    selection = 0

            elif type_exam =='Questions found':

                    # Define a regular expression pattern to match revision questions
                    pattern = r'^[Ww]hat |^[Ww]hy |^[Hh]ow |^[Dd]escribe |^[Ee]xplain '

                    # Create an empty list to store the revision questions
                    revision_questions = []
                    revision_answers = []

                    # Loop through each sentence and check if it matches the pattern
                    for index, sentence in enumerate(self.sent_tokens):
                        if re.match(pattern, sentence):
                            revision_questions.append(sentence)
                            revision_answers.append(self.sent_tokens[index+1])
                    if revision_questions:
                        Qn_generated = random.choice(revision_questions)
                        ans_generated = random.choice(revision_answers)
                        questions.append(Qn_generated)
                        answers.append(ans_generated)

            elif type_exam =='Essay':
                # points_kewords =['called', 'known as', 'termed as']
                points_kewords = ['purposes', 'aims', 'objectives', 'types', 'characters', 'advantages', 'benefits', 'merits', 'factors', 'causes', 'advantages']
                qn, ans = self.serching_keywords(self.sent_tokens,points_kewords)
                try:
                    Qn_generated =random.choice(qn)
                except:
                    pass
                if Qn_generated == "":
                    print('empty')
                else:
                    questions.append(Qn_generated)
                    answers.append(ans_generated)
            elif type_exam == 'extracting content':
                user_input = 'how'
                user_input = user_input.lower()
                self.sent_tokens.append(user_input)
                word_token = self.word_tokens +nltk.word_tokenize(user_input)
                final_words = list(set(word_token))
                result = self.response(user_input)
                self.sent_tokens.remove(user_input)
                questions.append(result)
            else:
                print('ok')
            no_questions_generated +=1
            ans = ''
            
        print('Question generated with results')
        return questions, answers