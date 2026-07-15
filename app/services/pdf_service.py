import fitz


class PDFService:
    """
    Service responsible for extracting text from PDF files.
    """

    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extract all text from a PDF.

        Args:
            file_path: Path to the PDF file.

        Returns:
            Complete text extracted from the PDF.
        """

        document = fitz.open(file_path)

        text = ""

        try:
            for page in document:
                text += page.get_text()
        finally:
            document.close()

        return text