from flask import Flask, request, render_template
import os
import openai
import PyPDF2
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
from markdown import markdown

# Load environment variables from a .env file (if present)
load_dotenv()

# Set up OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key is set
if not openai.api_key:
    print("Error: OpenAI API key is missing. Please set it in the environment variables.")
    exit()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, '../claimSenseAI_web/templates'),
    static_folder=os.path.join(BASE_DIR, '../claimSenseAI_web/static')
)
def extract_text_from_pdf(pdf_path_1, pdf_path_2):
    """
    Extracts text from 2 PDF files.
    Args:
        pdf_path_1 (str): The file path of the PDF document.
        pdf_path_2 (str): the file of the PDF document

    Returns:
        str: Extracted text from the combined PDF's.
    """
    try:
        text = ""
        with open(pdf_path_1,  "rb") as file:
            reader1 = PyPDF2.PdfReader(file)
            # Extract text from each page and join them with newline
            text += "\n".join([page.extract_text() for page in reader1.pages if page.extract_text()])

        with open(pdf_path_2, "rb") as file:
            reader2 = PyPDF2.PdfReader(file)
            # extract text from each page and join them with newline
            text += "\n".join([page.extract_text() for page in reader2.pages if page.extract_text()])

        return text.strip() if text else None # ensures that None is returned if there is no text
    except Exception as e:
        print(f"Error while reading PDF: {e}")
        return None


def analyze_claim(text, user_prompt):
    """
    Uses GPT-4-Turbo to review the insurance claim.

    Args:
        text (str): Extracted text from the insurance claim PDF.

    Returns:
        str: AI-generated summary, key details, and red flags (if any).
        :param text:
        :param user_prompt:
    """
    try:
        # Initialize the OpenAI language model with GPT-4-Turbo
        llm = ChatOpenAI(model_name="gpt-4-turbo", openai_api_key=openai.api_key)

        # Define system and user messages for context
        messages = [
            SystemMessage(
                content="You are an AI assistant that reviews insurance claims for accuracy, fraud detection, and compliance."),
            HumanMessage(
                content=f"Here is an insurance claim and policy document:\n{text}\n\n" + user_prompt)
            # Review these document's and provide a summary, key details, and any potential red flags.
        ]

        # Use the invoke method to get AI response
        response = llm.invoke(messages)

        return response.content
    except Exception as e:
        print(f"Error while analyzing claim: {e}")
        return None

@app.route('/')
def home():
    return render_template("Auth.html")

@app.route('/process', methods=['POST'])
def process_login(): #process_files():

    password_actual = "password"
    username_actual = "samuel"

    username = request.form["username"]
    password = request.form["password"]

    print(username)
    print(password)

    if password_actual == password:
        if username_actual == username:
            return render_template("index.html")

    return render_template("login_failed.html")


@app.route('/upload', methods=['POST'])
def process_files():
    claim_pdf = request.files['claim_pdf']
    policy_pdf = request.files['policy_pdf']

    user_prompt = request.form['prompt']

    claim_pdf_path = os.path.join('uploads', claim_pdf.filename)
    policy_pdf_path = os.path.join('uploads', policy_pdf.filename)

    claim_pdf.save(claim_pdf_path)
    policy_pdf.save(policy_pdf_path)

    extracted_text = extract_text_from_pdf(claim_pdf_path, policy_pdf_path)


    review_output = analyze_claim(extracted_text, user_prompt)
    markdown_as_html = markdown(review_output)

    return render_template('response_page.html', review_output=markdown_as_html )

# Run the main function when the script is executed
if __name__ == "__main__":
    app.run(debug=True)
