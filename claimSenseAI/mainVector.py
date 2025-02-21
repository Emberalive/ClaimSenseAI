import os
import PyPDF2
from dotenv import load_dotenv
from langchain.schema import SystemMessage, HumanMessage
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatDeepSeek

load_dotenv()

# Set up DeepSeek API key (Replace with your key)
deepseek_api_key = "OPENAI_API_KEY"

# Initialize FAISS Vector Store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.load_local("claims_db", embeddings)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

def retrieve_similar_claims(text):
    """Retrieves similar past claims from the vector database."""
    similar_claims = vectorstore.similarity_search(text, k=3)
    return "\n\n".join([claim.page_content for claim in similar_claims])

def analyze_claim(text):
    """Uses DeepSeek to review the insurance claim with retrieved similar cases."""
    similar_cases = retrieve_similar_claims(text)
    llm = ChatDeepSeek(model_name="deepseek-chat", api_key=deepseek_api_key)
    messages = [
        SystemMessage(
            content="You are an AI assistant that reviews insurance claims for accuracy, fraud detection, and compliance."),
        HumanMessage(
            content=f"Here is an insurance claim document:\n{text}\n\nHere are similar past cases for reference:\n{similar_cases}\n\nReview this document and provide a summary, key details, and any potential red flags.")
    ]
    response = llm(messages)
    return response.content

def main():
    print("Welcome to the Insurance Claim AI Reviewer!")
    pdf_path = input("Enter the path to the insurance claim PDF: ").strip()
    if not os.path.exists(pdf_path):
        print("File not found. Please enter a valid path.")
        return

    print("Processing the document...\n")
    claim_text = extract_text_from_pdf(pdf_path)
    if not claim_text:
        print("No text found in the document. Please check the file.")
        return

    review_output = analyze_claim(claim_text)
    print("\n--- AI Claim Review ---\n")
    print(review_output)

if __name__ == "__main__":
    main()
