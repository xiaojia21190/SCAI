import requests
from pathlib import Path
import PyPDF2
from typing import Optional
import tempfile

class PaperRetrieval:
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or Path(tempfile.gettempdir()) / "scai_papers"
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_full_text(self, paper_id: str) -> str:
        # Check cache first
        cache_file = self.cache_dir / f"{paper_id}.txt"
        if cache_file.exists():
            return cache_file.read_text()
        
        # Download PDF
        pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
        response = requests.get(pdf_url)
        
        if response.status_code != 200:
            raise Exception(f"Failed to download paper {paper_id}")
        
        # Save PDF temporarily
        pdf_path = self.cache_dir / f"{paper_id}.pdf"
        pdf_path.write_bytes(response.content)
        
        # Extract text
        text = self._extract_text_from_pdf(pdf_path)
        
        # Cache the text
        cache_file.write_text(text)
        
        # Clean up PDF
        pdf_path.unlink()
        
        return text
    
    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text