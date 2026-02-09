import PyPDF2
import os
from docx import Document

def pdf_to_md(filepath: str):
    """read pdf file and return markdown texts"""
    md_output = f"## Document: {os.path.basename(filepath)}\n\n"
    try:
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    md_output += f"### Page {i+1}\n{page_text}\n\n"
    except Exception as e:
        return (f"got error: {e}")

def docx_to_md(filepath: str):
    """read pdf file and return markdown texts"""
    md_output = f"## Document: {os.path.basename(filepath)}\n\n"
    try:
        doc = Document(filepath) ## Document handles opening of file
        for para in doc.paragraphs:
            if para.text.strip():
                md_output += f"{para.text}\n\n"

    except Exception as e:
        return (f"got error: {e}")
        
##process Resumes##
def process_resumes(input_folder: str) -> list:

    #each element is the md content of pdf/doc
    extracted_docs = [] 

    #to list content of any directory or folder we use
    dirlist =  os.listdir(input_folder)

    for filename in dirlist:
        #create filepath to read
        filepath = os.path.join(input_folder, filename)

        #step 2
        ext = filename.lower().split('.')[-1]

        if ext == "pdf":
            content = pdf_to_md(filepath)
            extracted_docs.append(content)
        elif ext in ["doc", "docx"]:
            content = docx_to_md(filepath)
            extracted_docs.append(content)
            
    return extracted_docs

#input and output file
input_folder = './resumes'
output_file = "resume_data.json"

# whether input folder path exist
if not os.path.exists(input_folder):
    print("File or Folder does not exist")
else :
    markdown_resumes = process_resumes(input_folder)

    if markdown_resumes:
        print("------Sample output-----")
        print(markdown_resumes[0])