from flask import Flask, request, render_template
import os
import openai
import PyPDF2
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
from markdown import markdown
from DBAccess.dbAccess import db_access
import bcrypt


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

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from two lists of PDF files.
    Args:
        pdf_path : a document taken from the user

    Returns:
        str: Extracted text from the pdf
    """
    try:
        text = ""

        # Process the first list of PDFs (pdf_paths_1)
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text += "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            return text.strip() if text else None  # Return None if no text is extracted

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

    # grabbing the credentials from the form
    username = request.form["username"]
    password = request.form["password"].encode('utf-8')

    print(username)
    print(password)


    # accessing the connection and cursor from the db access file
    conn, cur = db_access()

    # selecting the user from the database
    query = "SELECT * FROM users WHERE username = %s"

    # executing the query
    print("\n getting user credentials from database")
    try:
        cur.execute(query, (username,))  # Pass username as a tuple
        conn.commit()

    except Exception as e:
        print(f"Database error: {e}")
        return render_template("login_failed.html")

    # using the results to check the password
    result = cur.fetchone()

    print("\nchecking the inputted credentials against stored credentials")
    if result:
        stored_password = result[1]  # Ensure stored password is in bytes

        if isinstance(stored_password, str):
            stored_password = stored_password.encode('utf-8')

        # Check if entered password matches stored password
        if bcrypt.checkpw(password, stored_password):
            return render_template("index.html")  # Redirect to the main page

    return render_template("login_failed.html")  # If login fails, show error page


@app.route('/upload', methods=['POST'])
def process_files():
    extracted_text = ""

    claims  = request.files.getlist('claim_pdf')
    policies = request.files.getlist('policy_pdf')

    user_prompt = request.form['prompt']

    for claim in claims:
        claim_pdf_path = os.path.join('uploads', claim.filename)
        claim.save(claim_pdf_path)

        claim_text = extract_text_from_pdf(claim_pdf_path)

        if claim_text:
            extracted_text += "This is a new claim:\n" + claim_text + "\n\n"

    for policy in policies:
        policy_pdf_path = os.path.join('uploads', policy.filename)
        policy.save(policy_pdf_path)

        policy_text = extract_text_from_pdf(policy_pdf_path)

        if policy_text:
            extracted_text += "This is a new policy:\n" + policy_text + "\n\n"



    review_output = analyze_claim(extracted_text, user_prompt)
    markdown_as_html = markdown(review_output)

    print(extracted_text)

    return render_template('response_page.html', review_output=markdown_as_html )

# Run the main function when the script is executed
if __name__ == "__main__":
    app.run(debug=True)
