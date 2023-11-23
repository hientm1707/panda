import PyPDF2
import subprocess



def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

def generate_pdf(latex_content, output_filename):
    # Write the LaTeX content to a file
    with open(f'{output_filename}.tex', 'w') as file:
        file.write(latex_content)

    # Compile the LaTeX file into a PDF
    subprocess.run(['pdflatex', f'{output_filename}.tex'])


def write_to_file(content, output_file_path):
    with open(output_file_path, 'w') as file:
        file.write(content)


def read_old_cv(filename):
    # Open the PDF file in read-binary mode
    pdf_file = open(filename, 'rb')

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Get the number of pages in the PDF file
    num_pages = len(pdf_reader.pages)
    if num_pages > 0:
        # Loop over each page and extract the text
        cnt = 0
        full_text = ""
        for page in range(num_pages):
            # Get the page object
            pdf_page = pdf_reader.pages[page]
            # Extract the text from the page
            full_text += pdf_page.extract_text()
        return full_text
    else:
        return None

def read_old_cv_binary(cv_binary_repr):
    pdf_reader = PyPDF2.PdfReader(cv_binary_repr)

    # Get the number of pages in the PDF file
    num_pages = len(pdf_reader.pages)
    if num_pages > 0:
        # Loop over each page and extract the text
        cnt = 0
        full_text = ""
        for page in range(num_pages):
            # Get the page object
            pdf_page = pdf_reader.pages[page]
            # Extract the text from the page
            full_text += pdf_page.extract_text()
        return full_text
    else:
        return None


