import os
import numpy as np
from scipy.spatial.distance import cosine
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, make_response
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from langchain.docstore.document import Document
import docx
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import UnstructuredPDFLoader
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
llm = OpenAI(openai_api_key=openai_api_key)
app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if request.method == 'POST':
            file = request.files['document']
            if file:
                filename = secure_filename(file.filename)
                app.logger.info(f"Uploaded file name: {filename}")  # Log the uploaded file name
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                if filename.endswith('.pdf'):
                    text_content = extract_text_from_pdf(file_path)
                    content = f'<pre>{text_content}</pre>'
                elif filename.endswith('.txt'):
                    with open(file_path, 'r') as file:
                        content = f'<pre>{file.read()}</pre>'
                elif filename.endswith('.docx'):
                    try:
                        doc = docx.Document(file_path)
                        full_text = [paragraph.text for paragraph in doc.paragraphs]
                        content = '<pre>' + '\n'.join(full_text) + '</pre>'
                    except Exception as e:
                        app.logger.error(f'Error reading .docx file: {str(e)}')
                        content = f'<p>Error reading .docx file: {str(e)}</p>'
                else:
                    app.logger.error(f'Unsupported file format: {filename}')
                    content = '<p>Unsupported file format.</p>'

                response = make_response(
                    jsonify({'success': True, 'content': content}))
                response.headers['Content-Type'] = 'application/json'
                return response

        response = make_response(
            jsonify({'success': False, 'message': 'No file was uploaded.'}))
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        app.logger.error(f'Error during file upload: {str(e)}')
        response = make_response(
            jsonify({'success': False, 'message': 'An error occurred during file upload.'}))
        response.headers['Content-Type'] = 'application/json'
        return response, 500


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page_text = reader.pages[page_num].extract_text()
            text += f"Page {page_num + 1}:\n{page_text}\n\n"
    return text

@app.route('/document/<filename>')
def display_document(filename):
    if filename.endswith('.txt') or filename.endswith('.pdf'):
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as file:
            content = file.read()
        return render_template('document.html', filename=filename, content=content)
    return render_template('document.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/search', methods=['POST'])
def search_document():
    try:
        data = request.get_json()
        query = data.get('query')
        filename = data.get('filename')
        app.logger.info(f"Search file name: {filename}")  # Log the search file name
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Load the uploaded .docx file and extract the text
        loader = Docx2txtLoader(file_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        # Create a vector store index
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_documents(texts, embeddings)

        # Create a question-answering chain
        qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever())

        # Perform the search and get the relevant text
        relevant_text = qa.invoke(query)
        app.logger.info(f"Relevant text: {relevant_text}")  # Log the relevant text

        # Collect information for attribution
        attribution_info = []
        for doc in qa.retriever.get_relevant_documents(query):
            attribution_info.append({
                'page_number': doc.metadata.get('page', 'N/A'),
                'text': doc.page_content
            })
        app.logger.info(f"Attribution info: {attribution_info}")  # Log the attribution info

        # Prepare the response
        response_data = {
            'success': True,
            'content': relevant_text,
            'attribution': attribution_info
        }
        app.logger.info(f"Response data: {response_data}")  # Log the response data

        response = make_response(jsonify(response_data))
        response.headers['Content-Type'] = 'application/json'
        return response

    except Exception as e:
        app.logger.error(f"Error during search: {str(e)}")
        response = make_response(
            jsonify({'success': False, 'message': str(e)}))
        response.headers['Content-Type'] = 'application/json'
        return response, 404


def cosine_similarity(vec1, vec2):
    # Calculate cosine similarity as 1 minus the cosine distance
    return 1 - cosine(vec1, vec2)


if __name__ == '__main__':
    app.run()