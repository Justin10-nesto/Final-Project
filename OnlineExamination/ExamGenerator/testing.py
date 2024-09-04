from exam_generator import ExamGerator
# path = r'C:\Users\CTS\Downloads\ELearning\static\media\Books\Entrepreneurship3.pdf'
# # path = r'C:\Users\CTS\Downloads\ELearning\static\models\Qns Generation\new.txt'
# hist = ExamGerator('history', [path])
# doc =hist.doc_opening()
# taging = hist.chicking_doc_tags()
# print('essay questions')
# questions, answers= hist.generate_exams('Essay', 10)
# print('fill the blanks')
# questions, answers= hist.generate_exams('fill the blanks', 10)
# print('Short Note')
# questions, answers= hist.generate_exams('fill the blanks', 10)
# print(questions)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
# Sample documents
documents = [
    "This is the first document.",
    "This document is the second document.",
    "And this is the third one.",
    "Is this the first document?"
]

# Preprocess the documents (optional)
# You can use libraries like NLTK or spaCy for tokenization and stemming

# Create vector representations using TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

# Calculate cosine similarity
similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
arr_np = np.array(similarity_matrix)
# Print the similarity matrix
arr_np.mean()
