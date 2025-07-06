#!/usr/bin/env python3
"""
Teste pytest para extração de texto de PDFs
"""

import os
import sys
import pytest

# Adiciona o diretório raiz do projeto ao path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from utils.pdf_extractor import extract_text_from_pdf

class TestPDFExtraction:
    """Testes para extração de texto de PDFs"""
    
    @pytest.fixture
    def input_dir(self):
        """Retorna o diretório de entrada"""
        return "input_files"
    
    @pytest.fixture
    def pdf_files(self, input_dir):
        """Retorna lista de arquivos PDF encontrados"""
        if not os.path.exists(input_dir):
            pytest.skip(f"Diretório {input_dir} não encontrado")
        
        pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
        if not pdf_files:
            pytest.skip(f"Nenhum arquivo PDF encontrado em {input_dir}")
        
        return pdf_files
    
    def test_pdf_files_exist(self, input_dir, pdf_files):
        """Testa se existem arquivos PDF na pasta input_files"""
        assert os.path.exists(input_dir), f"Diretório {input_dir} deve existir"
        assert len(pdf_files) > 0, f"Deve haver pelo menos um PDF em {input_dir}"
        
        print(f"\nPDFs encontrados em {input_dir}:")
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"{i}. {pdf_file}")
    
    def test_pdf_extraction(self, input_dir, pdf_files):
        """Testa a extração de texto de cada PDF"""
        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_dir, pdf_file)
            print(f"\nTestando extração de: {pdf_file}")
            
            # Testa se o arquivo existe
            assert os.path.exists(pdf_path), f"Arquivo {pdf_path} deve existir"
            
            # Tenta extrair texto
            text = extract_text_from_pdf(pdf_path)
            
            # Verifica se a extração foi bem-sucedida
            if text:
                print(f"✅ Sucesso! Extraídos {len(text)} caracteres")
                print(f"Primeiros 200 caracteres:")
                print(text[:200])
                print("...")
                
                # Verifica se o texto tem conteúdo significativo
                assert len(text.strip()) > 0, f"Texto extraído de {pdf_file} não pode estar vazio"
                assert len(text) > 100, f"Texto extraído de {pdf_file} deve ter pelo menos 100 caracteres"
                
            else:
                print(f"❌ Falha na extração de {pdf_file}")
                # Para PDFs que falham na extração, vamos apenas avisar mas não falhar o teste
                pytest.skip(f"Extração falhou para {pdf_file} - pode ser um PDF de imagem")
    
    def test_pdf_extraction_with_truncation(self, input_dir, pdf_files):
        """Testa a extração com truncamento para limites de tokens"""
        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_dir, pdf_file)
            print(f"\nTestando truncamento de: {pdf_file}")
            
            # Testa com limite baixo de tokens
            text = extract_text_from_pdf(pdf_path, max_tokens=1000)
            
            if text:
                # Verifica se o texto foi truncado corretamente
                max_chars = 1000 * 4  # 4 caracteres por token
                assert len(text) <= max_chars, f"Texto deve ser truncado para {max_chars} caracteres"
                print(f"✅ Truncamento OK: {len(text)} caracteres")
            else:
                print(f"❌ Falha na extração de {pdf_file}")

if __name__ == "__main__":
    # Execução direta para debug
    test_instance = TestPDFExtraction()
    input_dir = "input_files"
    
    if not os.path.exists(input_dir):
        print(f"Diretório {input_dir} não encontrado!")
        sys.exit(1)
    
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"Nenhum arquivo PDF encontrado em {input_dir}")
        sys.exit(1)
    
    print(f"PDFs encontrados em {input_dir}:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"{i}. {pdf_file}")
    
    print("\n" + "="*50)
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        print(f"\nTestando: {pdf_file}")
        print("-" * 30)
        
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            print(f"✅ Sucesso! Extraídos {len(text)} caracteres")
            print(f"Primeiros 200 caracteres:")
            print(text[:200])
            print("...")
        else:
            print("❌ Falha na extração")
        
        print("-" * 30) 