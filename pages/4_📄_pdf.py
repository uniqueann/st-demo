# Import necessary libraries
import os
import PyPDF2
import streamlit as st

# Define function to merge pdf files
def merge_pdf_files(pdf_files):
    # Create a PdfFileMerger object
    merger = PyPDF2.PdfMerger()
    # Loop through each pdf file and append it to the merger object
    for file in pdf_files:
        merger.append(file)
    # Create a temporary file to write the merged pdf to
    with open("merged_pdf.pdf", "wb") as output:
        # Write the merged pdf to the temporary file
        merger.write(output)
    # Return the name of the merged pdf file
    return "merged_pdf.pdf"

# Define the Streamlit app
def app():
    # Set the title of the app
    st.title("PDF Merger")
    # Create a file uploader to allow the user to upload multiple pdf files
    pdf_files = st.file_uploader("请上传多个 PDF 文件", accept_multiple_files=True, type="pdf")
    # Create a button to merge the pdf files
    if st.button("Merge PDF files"):
        # Check if any pdf files were uploaded
        if pdf_files:
            # Create a progress bar to display the merge process
            progress_bar = st.progress(0)
            # Merge the pdf files
            merged_pdf = merge_pdf_files(pdf_files)
            # Update the progress bar to 100% to indicate that the merge is complete
            progress_bar.progress(100)
            # Create a download link for the merged pdf file
            st.download_button("Download merged PDF", data=open(merged_pdf, "rb").read(), file_name="merged_pdf.pdf")
        else:
            # Display an error message if no pdf files were uploaded
            st.error("Please upload at least one PDF file.")

app()