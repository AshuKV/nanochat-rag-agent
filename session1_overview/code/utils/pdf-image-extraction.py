import fitz  # PyMuPDF
import os
import io
from PIL import Image


def extract_images_from_pdf(pdf_path, output_dir):
    """
    Extract all images from a PDF file and save them as PNG files.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save the extracted images
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Initialize image counter
    image_count = 0
    
    # Iterate through each page of the PDF
    for page_num, page in enumerate(pdf_document):
        # Get image list
        image_list = page.get_images(full=True)
        
        # Print information for debugging
        print(f"Found {len(image_list)} images on page {page_num + 1}")
        
        # Iterate through images on the page
        for img_index, img in enumerate(image_list):
            # Get the XREF of the image
            xref = img[0]
            
            # Extract the image bytes
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Get the image extension
            image_ext = base_image["ext"]
            
            # Load image and convert it to a PIL Image object
            image = Image.open(io.BytesIO(image_bytes))
            
            # Save the image as PNG
            image_filename = f"{output_dir}/page{page_num + 1}_image{img_index + 1}.png"
            image.save(image_filename, "PNG")
            
            print(f"Saved image as {image_filename}")
            image_count += 1
    
    # Close the PDF
    pdf_document.close()
    
    print(f"Total of {image_count} images extracted from {pdf_path}")


# Example usage
if __name__ == "__main__":
    input_folder = r"C:\home\ananth\trainings\adobe\genai_2025\batch2_may_june"
    pdf_name = "Session_1_overview_12may2025.pdf"

    pdf_file = os.path.join(input_folder, pdf_name)  # Replace with your PDF file path
    output_folder = r"C:\home\ananth\research\my_projects\2025_batch2_may_june\core\images_from_pdf"  # to save images
    extract_images_from_pdf(pdf_file, output_folder)
