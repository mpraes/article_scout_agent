import os
import sys

def extract_text_from_pdf(pdf_path: str, max_tokens: int = 20000) -> str:
    """
    Extrai texto de um arquivo PDF usando múltiplos métodos.
    
    Args:
        pdf_path (str): Caminho para o arquivo PDF
        max_tokens (int): Número máximo de tokens (aproximadamente 4 caracteres por token)
    
    Returns:
        str: Texto extraído do PDF, truncado se necessário
    """
    if not os.path.exists(pdf_path):
        print(f"Erro: Arquivo não encontrado: {pdf_path}")
        return ""
    
    print(f"Tentando extrair texto de: {pdf_path}")
    
    # Método 1: PyPDF2
    text = try_pypdf2(pdf_path)
    if text.strip():
        print(f"PyPDF2 extraiu {len(text)} caracteres")
        return truncate_text(text, max_tokens)
    
    # Método 2: pdfminer.six
    text = try_pdfminer(pdf_path)
    if text.strip():
        print(f"pdfminer extraiu {len(text)} caracteres")
        return truncate_text(text, max_tokens)
    
    # Método 3: pymupdf (fitz)
    text = try_pymupdf(pdf_path)
    if text.strip():
        print(f"PyMuPDF extraiu {len(text)} caracteres")
        return truncate_text(text, max_tokens)
    
    print("Nenhum método conseguiu extrair texto do PDF")
    return ""

def try_pypdf2(pdf_path: str) -> str:
    """Tenta extrair texto usando PyPDF2"""
    try:
        import PyPDF2
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text += page_text
        return text
    except Exception as e:
        print(f"PyPDF2 falhou: {e}")
        return ""

def try_pdfminer(pdf_path: str) -> str:
    """Tenta extrair texto usando pdfminer.six"""
    try:
        from pdfminer.high_level import extract_text
        text = extract_text(pdf_path)
        return text
    except ImportError:
        print("pdfminer.six não está instalado")
        return ""
    except Exception as e:
        print(f"pdfminer falhou: {e}")
        return ""

def try_pymupdf(pdf_path: str) -> str:
    """Tenta extrair texto usando PyMuPDF (fitz)"""
    try:
        import fitz  # PyMuPDF
        text = ""
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except ImportError:
        print("PyMuPDF não está instalado")
        return ""
    except Exception as e:
        print(f"PyMuPDF falhou: {e}")
        return ""

def truncate_text(text: str, max_tokens: int) -> str:
    """Trunca o texto para caber no limite de tokens da API"""
    max_chars = max_tokens * 4  # Aproximadamente 4 caracteres por token
    if len(text) > max_chars:
        truncated = text[:max_chars]
        print(f"Texto truncado para {max_tokens} tokens ({len(truncated)} caracteres)")
        return truncated
    return text

if __name__ == "__main__":
    # Teste direto
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
        text = extract_text_from_pdf(pdf_file)
        if text:
            print(f"\nPrimeiros 500 caracteres extraídos:")
            print(text[:500])
        else:
            print("Nenhum texto foi extraído")
    else:
        print("Uso: python pdf_extractor.py <caminho_do_pdf>") 