import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline

# -------------------------
# FILE PATH
# -------------------------
file_path = r"C:\Users\Praveen Roy\it-helpdesk-ai\data\knowledge_base\password_reset.txt"

if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

# -------------------------
# LOAD DOCUMENT
# -------------------------
loader = TextLoader(file_path)
docs = loader.load()

# -------------------------
# EMBEDDING MODEL
# -------------------------
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -------------------------
# VECTOR DATABASE (FAISS)
# -------------------------
vector_db = FAISS.from_documents(docs, embedding_model)

# -------------------------
# LLM (GPT2 - CONTROLLED)
# -------------------------
llm = pipeline(
    "text-generation",
    model="gpt2",
)

# -------------------------
# QUERY FUNCTION (FINAL CLEAN)
# -------------------------
def query_rag(query: str):

    # Step 1: Retrieve
    results = vector_db.similarity_search(query, k=1)

    if not results:
        return "No relevant information found."

    context = results[0].page_content

    # Step 2: Prompt
    prompt = f"""
Answer using ONLY the context.

Context:
{context}

Question:
{query}

Give only 4 clear steps:
"""

    # Step 3: Generate
    response = llm(
        prompt,
        max_new_tokens=80,
        do_sample=False,
    )

    raw_output = response[0]["generated_text"]

    # -------------------------
    # CLEAN OUTPUT
    # -------------------------
    cleaned = raw_output.replace(prompt, "").strip()

    lines = cleaned.split("\n")

    final_lines = []
    for line in lines:
        line = line.strip()

        if not line:
            continue

        # stop unwanted repetition
        if "Question" in line or "Context" in line:
            break

        final_lines.append(line)

        if len(final_lines) >= 4:
            break

    return "\n".join(final_lines)