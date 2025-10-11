from pypdf import PdfReader


def parse_page_numbers(text):
    """Parse page numbers from text input (e.g., '1,3,5-7' -> [0,2,4,5,6])."""
    pages = set()
    try:
        text = text.strip()
        while ',,' in text:
            text = text.replace(',,', ',')
        text = text.strip(',')
        
        if not text:
            return None
        
        for part in text.split(','):
            part = part.strip()
            if not part:
                continue
                
            if '-' in part:
                range_parts = part.split('-')
                if len(range_parts) != 2:
                    return None
                start, end = range_parts[0].strip(), range_parts[1].strip()
                if not start or not end:
                    return None
                start, end = int(start), int(end)
                if start < 1 or end < 1 or start > end:
                    return None
                pages.update(range(start - 1, end))
            else:
                page_num = int(part)
                if page_num < 1:
                    return None
                pages.add(page_num - 1)
        
        return sorted(pages) if pages else None
    except (ValueError, AttributeError):
        return None


def get_pdf_info(file_path):
    """Get PDF file information (total pages).
    
    Returns:
        dict with 'total_pages' key, or raises exception on error
    """
    reader = PdfReader(file_path, strict=False)
    total_pages = len(reader.pages)
    return {'total_pages': total_pages}
