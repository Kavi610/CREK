from googleapiclient.discovery import build
from google.oauth2 import service_account
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/documents']
SERVICE_ACCOUNT_FILE = SERVICE_ACCOUNT_FILE = r"D:\internship program\CREK\Project\mysite\myapp\service-account.json"
  # Secure this file

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
docs_service = build('docs', 'v1', credentials=credentials)

def convert_html_to_google_docs(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    requests = []
    index = 1
    
    for tag in soup.recursiveChildGenerator():
        if tag.name == 'h1':
            requests.append({
                "insertText": {"location": {"index": index}, "text": tag.get_text() + "\\n"}
            })
            requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": index, "endIndex": index + len(tag.get_text())},
                    "textStyle": {"bold": True, "fontSize": {"magnitude": 18, "unit": "PT"}},
                    "fields": "bold,fontSize"
                }
            })
        elif tag.name == 'p':
            requests.append({
                "insertText": {"location": {"index": index}, "text": tag.get_text() + "\\n"}
            })
        index += len(tag.get_text()) + 1
    
    return requests

def create_google_doc(content):
    doc = docs_service.documents().create(body={}).execute()
    document_id = doc.get('documentId')
    requests = convert_html_to_google_docs(content)
    docs_service.documents().batchUpdate(
        documentId=document_id, body={"requests": requests}
    ).execute()
    return f"https://docs.google.com/document/d/{document_id}"
