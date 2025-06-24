import streamlit as st
import PyPDF2
import tempfile
from io import StringIO

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def main():
    st.title("PDF Merger & Text Extractor")

    st.write(
        """
        Upload multiple PDF files and this app will extract all the text, 
        preserving the order, and allow you to download a single structured text file.
        """
    )

    uploaded_files = st.file_uploader(
        "Choose PDF files", 
        type=["pdf"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        pdf_texts = []
        for idx, uploaded_file in enumerate(uploaded_files, 1):
            with st.spinner(f"Extracting PDF {idx}: {uploaded_file.name}"):
                pdf_text = extract_text_from_pdf(uploaded_file)
                # Add basic structure: filename and separator
                structured_text = f"\n---\nFile: {uploaded_file.name}\n---\n{pdf_text.strip()}\n"
                pdf_texts.append(structured_text)

        final_text = "\n".join(pdf_texts)
        
        st.subheader("Preview of Extracted Text")
        st.text_area("Combined Text", final_text[:5000], height=200)

        # Download the combined text file
        st.download_button(
            "Download Structured Text File",
            data=final_text,
            file_name="combined_pdfs.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
