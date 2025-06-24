import streamlit as st
import PyPDF2
import gzip
from io import BytesIO

def extract_structured_text(file, filename):
    pdf_reader = PyPDF2.PdfReader(file)
    structured_text = [f"\n===== File: {filename} =====\n"]
    for i, page in enumerate(pdf_reader.pages, 1):
        text = page.extract_text() or ""
        structured_text.append(f"\n--- Page {i} ---\n{text.strip()}\n")
    return "".join(structured_text)

def compress_text(text):
    buffer = BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode='wb') as gz_file:
        gz_file.write(text.encode('utf-8'))
    buffer.seek(0)
    return buffer

def main():
    st.title("PDF to Structured Text (with Compression)")

    st.write(
        """
        Upload multiple PDFs. The app will extract structured text while preserving file and page boundaries, 
        and you can download the result as a compressed text file (.txt.gz) for easy sharing and storage.
        """
    )

    uploaded_files = st.file_uploader(
        "Choose PDF files", 
        type=["pdf"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        all_structured_text = []
        for uploaded_file in uploaded_files:
            with st.spinner(f"Extracting: {uploaded_file.name}"):
                structured = extract_structured_text(uploaded_file, uploaded_file.name)
                all_structured_text.append(structured)
        complete_text = "\n".join(all_structured_text)
        
        st.subheader("Preview of Structured Text")
        st.text_area(
            "Preview (first 5000 characters)", 
            complete_text[:5000], 
            height=250
        )

        compressed_buffer = compress_text(complete_text)
        st.download_button(
            "Download Compressed Structured Text (.txt.gz)",
            data=compressed_buffer,
            file_name="combined_pdfs_structured.txt.gz",
            mime="application/gzip"
        )

if __name__ == "__main__":
    main()
