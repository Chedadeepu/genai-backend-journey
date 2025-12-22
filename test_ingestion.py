from genai.pdf_reader import extract_text_from_pdf
from genai.embeddings import create_embeddings_from_text

text = extract_text_from_pdf("uploads/KarmaQuest_IEEE_Paper.pdf")
count = create_embeddings_from_text(text)

print(f"Embedded {count} chunks")
