"""
Given a PDF file, return sections that are suitable for further processing
"""
import os
import fitz  # PyMuPDF


# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    pages = []
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        page_text = page.get_text()
        pages.append(page_text)
        text += page_text
    return {
        "text": text,
        "pages": pages,
    }


def load_pdf(pdf_filename):
    """
    Given a pdf file name, load its contents
    :param pdf_filename: file name
    :return: text of PDF contents
    """
    content = extract_text_from_pdf(pdf_filename)
    return content


if __name__ == '__main__':
    input_folder = r"C:\home\ananth\trainings\adobe\genai_2025\batch2_may_june"

    pdf_name = "Session_1_overview_12may2025.pdf"
    # pdf_name = "Session_2_dl_transformers_15may2025.pdf"

    pdf_file = os.path.join(input_folder, pdf_name)  # Replace with your PDF file path
    results = extract_text_from_pdf(pdf_file)
    print(len(results["pages"]))

    print(results["text"])



