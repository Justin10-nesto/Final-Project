import nltk
from nltk.tokenize import sent_tokenize
import random
from exam_generator import ExamGerator
path = r'C:/Users/CTS/Documents/DIT/ssmister VIII/project realization/Student_Course_Guidance_Admission_System_Project_Proposal_Book_Allan Thomas.pdf'
# path = r'C:\Users\CTS\Downloads\ELearning\static\models\Qns Generation\new.txt'
hist = ExamGerator('history', [path])
doc =hist.doc_opening()

def generate_true_false_questions(text, num_questions):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Generate True or False questions and their answers
    qa_pairs = []
    for sentence in sentences:
        # Remove leading/trailing whitespaces and convert to lowercase
        sentence = sentence.strip().lower()

        # Generate a True or False question by using the first part of the sentence as the statement
        statement = sentence.split(',')[0].strip()
        question, answer = create_question(statement)
        qa_pairs.append((question, answer))

    # Randomly select the desired number of questions
    random.shuffle(qa_pairs)
    qa_pairs = qa_pairs[:num_questions]

    return qa_pairs

def create_question(statement):
    keywords = ["not", "never", "unlike", "in contrast to", "instead of", "without", "except", "but",
                "also", "furthermore", "moreover", "in addition to", "similarly", "likewise", "additionally", "likewise"]

    # Choose a keyword randomly
    keyword = random.choice(keywords)

    # Create a true or false question using the chosen keyword
    if keyword in ["not", "never", "unlike", "in contrast to", "instead of", "without", "except", "but"]:
        question = f"Does {statement} {keyword}?"
        answer = False
    else:
        question = f"Does {statement} {keyword}?"
        answer = True

    return question, answer

# Example usage
text =doc
num_questions = 5

generated_qa_pairs = generate_true_false_questions(text, num_questions)
for i, (question, answer) in enumerate(generated_qa_pairs):
    print(f"Question {i+1}: {question}")
    print(f"Answer {i+1}: {answer}")
    print()
