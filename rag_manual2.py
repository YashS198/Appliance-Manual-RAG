import os
import json
import requests
import pdfplumber

API_URL = "https://models.github.ai/inference/chat/completions"
MODEL = "gpt-4.1"
MAX_COMPLETION_TOKENS = 500

GITHUB_PAT = os.getenv("GITHUB_PAT")

MANUAL_FOLDER = "manuals"


# Extract text from one PDF
def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
            text += "\n"
    return text


# Load all manuals
def load_all_manuals(folder):
    text = ""
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)
            text += extract_text_from_pdf(path)
            text += "\n"
    return text


# Split text into chunks
def split_into_chunks(text, chunk_size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


# Simple keyword retrieval
def retrieve_relevant_chunks(chunks, question, top_k=3):
    results = []

    for chunk in chunks:
        score = 0
        for word in question.lower().split():
            if word in chunk.lower():
                score += 1
        results.append((score, chunk))

    results.sort(reverse=True)

    return [chunk for score, chunk in results[:top_k]]


# Call GitHub model
def call_github_models(system_prompt, user_prompt):
    if not GITHUB_PAT:
        raise RuntimeError("GitHub PAT not configured.")

    headers = {
        "Authorization": f"Bearer {GITHUB_PAT}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": MAX_COMPLETION_TOKENS
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

    if response.status_code != 200:
        raise RuntimeError(f"GitHub Models error {response.status_code}: {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
#question.... 
# What you want to ask the assistant. For example, "What cookware is safe to use in a Samsung smart oven?"
# or question like "How does microwave cooking work in the Samsung smart oven?"
# or "Can I put metal in a microwave?"
    question = "What cookware is safe to use in a Samsung smart oven?"

    print("Loading manuals...")
    manual_text = load_all_manuals(MANUAL_FOLDER)

    print("Splitting into chunks...")
    chunks = split_into_chunks(manual_text)

    print("Retrieving relevant chunks...")
    relevant_chunks = retrieve_relevant_chunks(chunks, question)

    context = "\n\n".join(relevant_chunks)

    system_prompt = (
        "You are an appliance repair assistant. "
        "Use the provided manual context to answer the user's question. "
        "If the answer is not in the manuals, say you don't know."
    )

    user_prompt = f"""
Manual Context:
{context}

Question:
{question}
"""

    result = call_github_models(system_prompt, user_prompt)

    print("\nAssistant Response:\n")
    print(result)