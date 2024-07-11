from pathlib import Path
from PyPDF2 import PdfReader


from .exceptions import ImageExtractionError


def get_document(document_path: Path | str):
    """
    Retrieve a document from the specified path.

    This function accepts a file path as either a string or a `Path` object. It checks
    if the file exists at the given path and returns the path as a `Path` object. If 
    the file does not exist, it raises a `FileNotFoundError`.

    Parameters:
    -----------
    document_path : Path or str
        The path to the document. It can be provided as a string or a `Path` object.

    Returns:
    --------
    Path
        A `Path` object pointing to the document.

    Raises:
    -------
    FileNotFoundError
        If the file does not exist at the specified path.

    Examples:
    ---------
    >>> get_document("example.txt")
    PosixPath('example.txt')

    >>> get_document(Path("example.txt"))
    PosixPath('example.txt')

    >>> get_document("nonexistent.txt")
    Traceback (most recent call last):
    ...
    FileNotFoundError: File nonexistent.txt not found
    """
    if isinstance(document_path, str):
        document_path = Path(document_path)
    if not document_path.exists():
        raise FileNotFoundError(f"File {document_path} not found")
    return document_path




def read_document(document_path: Path) -> PdfReader:
    """
    Read a PDF document from the specified path.

    This function uses the `get_document` function to ensure the document path exists.
    It then attempts to read the PDF document using `PdfReader`. If an error occurs 
    during reading, it prints an error message and returns `None`.

    Parameters:
    -----------
    document_path : Path
        The path to the document as a `Path` object.

    Returns:
    --------
    PdfReader or None
        A `PdfReader` object if the document is successfully read, otherwise `None`.

    Raises:
    -------
    FileNotFoundError
        If the file does not exist at the specified path.

    Examples:
    ---------
    >>> read_document(Path("example.pdf"))
    <PdfReader object>

    >>> read_document(Path("nonexistent.pdf"))
    Error reading document: [Error message]
    None
    """
    document_path = get_document(document_path)
    try:
        reader = PdfReader(document_path)   
    except Exception as e:
        print(f"Error reading document: {e}")
        return None
    return reader



def get_document_meta_data(document: Path | PdfReader) -> dict:
    """
    Retrieve metadata from a PDF document.

    This function accepts a PDF document as either a `Path` object or a `PdfReader` object.
    If a `Path` object is provided, it uses the `get_document` and `read_document` functions
    to ensure the document exists and to read the document. It then extracts and returns 
    metadata from the PDF document.

    Parameters:
    -----------
    document : Path or PdfReader
        The path to the document as a `Path` object or a `PdfReader` object.

    Returns:
    --------
    dict
        A dictionary containing the document's metadata, including the number of pages, title,
        author, subject, producer, and creator. If the document cannot be read, returns `None`.

    Examples:
    ---------
    >>> get_document_meta_data(Path("example.pdf"))
    {
        'num_pages': 10,
        'title': 'Example Title',
        'author': 'Author Name',a
        'subject': 'Example Subject',
        'producer': 'PDF Producer',
        'creator': 'PDF Creator'
    }

    >>> get_document_meta_data(reader)
    {
        'num_pages': 10,
        'title': 'Example Title',
        'author': 'Author Name',
        'subject': 'Example Subject',
        'producer': 'PDF Producer',
        'creator': 'PDF Creator'
    }
    """
    if isinstance(document, Path):
        document = get_document(document)
        reader = read_document(document)
    else:
        reader = document

    if reader is None:
        return None

    meta_data = {}
    data = reader.metadata

    meta_data['num_pages'] = len(reader.pages)
    meta_data['title'] = data.title
    meta_data['author'] = data.author
    meta_data['subject'] = data.subject
    meta_data['producer'] = data.producer
    meta_data['creator'] = data.creator

    return meta_data



def extract_data_from_page(reader: PdfReader | Path, page_number: int, storage_path: Path =  Path('./images')):
    """
    Extract text and images from a specified page of a PDF document.

    This function takes a `PdfReader` object and a page number, and extracts the text and 
    images from the specified page. It also retrieves the document metadata and includes 
    the page number in the metadata. If the page number is less than 1, it raises a 
    `ValueError`. If the `PdfReader` object is `None`, it returns `None`.

    Parameters:
    -----------
    reader : PdfReader
        The `PdfReader` object representing the PDF document.
    page_number : int
        The page number to extract text and images from (1-based index).
    storage_path: Path
        the path to where to where the images will be store

    Returns:
    --------
    tuple
        A tuple containing:
        - text (str): The extracted text from the specified page.
        - images (list): A list of extracted images from the specified page.
        - meta_data (dict): A dictionary containing the document's metadata, including the page number.

    Raises:
    -------
    ValueError
        If the page number is less than 1.

    Examples:
    ---------
    >>> reader = PdfReader("example.pdf")
    >>> extract_text_from_page(reader, 1)
    (
        'Extracted text from page 1',
        ['image1.png', 'image2.png'],
        {
            'num_pages': 10,
            'title': 'Example Title',
            'author': 'Author Name',
            'subject': 'Example Subject',
            'producer': 'PDF Producer',
            'creator': 'PDF Creator',
            'page': 0
        }
    )
    """
    page_number -= 1  # Convert to 0-based index

    if page_number < 0:
        raise ValueError("Page number should be greater than 0")
    if reader is None:
        return None
    
    if isinstance(reader, Path):
        reader = read_document(reader)

    meta_data = get_document_meta_data(reader)
    meta_data['page'] = page_number + 1
    try:
        page = reader.pages[page_number]
        text = page.extract_text()
        images = extract_image(page, storage_path)
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None
    
    return text, images, meta_data




def extract_image(page, storage_path: Path = Path(__file__).parent):
    """
    Extract images from a PDF page and save them to a specified storage path.

    This function takes a PDF page object and extracts all images from the page, saving
    them to the specified storage path. Each image is saved with a unique filename 
    generated using a counter. If an error occurs during the extraction, it raises an 
    `ImageExtractionError`.

    Parameters:
    -----------
    page : PdfPage
        The PDF page object from which images will be extracted.
    storage_path : Path, optional
        The directory where extracted images will be saved. Defaults to the directory 
        of the current script.

    Returns:
    --------
    list
        A list of `Path` objects representing the paths to the saved images.

    Raises:
    -------
    ImageExtractionError
        If an error occurs while extracting and saving an image.

    Examples:
    ---------
    >>> page = reader.pages[0]
    >>> extract_image(page, Path('./images'))
    [PosixPath('images/0image1.png'), PosixPath('images/1image2.png')]
    """
    count = 0
    images = []
    for image_file_object in page.images:
        image_path = storage_path / f"{count}_{image_file_object.name}"

        try:
            with open(image_path, "wb") as fp:
                fp.write(image_file_object.data)
                images.append(image_path)
                count += 1
        except Exception as e:
            raise ImageExtractionError(f"Error extracting image: {e}")

    return images




