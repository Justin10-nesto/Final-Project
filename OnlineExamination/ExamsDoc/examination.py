import markovify

# Sample notes
notes = "Artificial intelligence is the simulation of human intelligence processes by machines. These processes include learning, reasoning, and self-correction. AI technologies are being used in various industries such as healthcare, finance, and transportation."

# Generate exam questions using Markov chains
text_model = markovify.Text(notes)
print(text_model)
num_questions = 3
questions = [text_model.make_sentence() for _ in range(num_questions)]
print(questions)