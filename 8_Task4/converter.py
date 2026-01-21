from docling.document_converter import DocumentConverter

def read_resume(file_path: str) -> str:
    converter = DocumentConverter()
    result = converter.convert(file_path)
    return result.document.export_to_text()
