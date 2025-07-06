#!/usr/bin/env python3
"""
Teste de integração: Extração de PDF + Avaliação com Article Scout Agent
"""

import os
import sys
import pytest
import pprint

# Adiciona o diretório raiz do projeto ao path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from utils.pdf_extractor import extract_text_from_pdf
from article_scout_agent import evaluate_research_paper, format_results_for_display

class TestIntegration:
    """Testes de integração entre extração de PDF e avaliação"""
    
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
    
    def test_pdf_extraction_and_evaluation(self, input_dir, pdf_files):
        """Testa o fluxo completo: extração de PDF + avaliação"""
        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_dir, pdf_file)
            print(f"\n{'='*60}")
            print(f"Testando integração completa: {pdf_file}")
            print(f"{'='*60}")
            
            # Passo 1: Extrair texto do PDF
            print(f"\n1. Extraindo texto de: {pdf_file}")
            article_text = extract_text_from_pdf(pdf_path)
            
            if not article_text:
                print(f"❌ Falha na extração de {pdf_file}")
                pytest.skip(f"Extração falhou para {pdf_file}")
            
            print(f"✅ Texto extraído: {len(article_text)} caracteres")
            
            # Passo 2: Definir tema para avaliação
            article_theme = self._get_theme_for_pdf(pdf_file)
            print(f"\n2. Tema para avaliação: {article_theme}")
            
            # Passo 3: Avaliar com Article Scout Agent
            print(f"\n3. Avaliando com Article Scout Agent...")
            try:
                results = evaluate_research_paper(article_text, article_theme)
                formatted_results = format_results_for_display(results)
                
                print(f"✅ Avaliação concluída!")
                print(f"\n{'='*60}")
                print("RESULTADOS DA AVALIAÇÃO:")
                print(f"{'='*60}")
                pprint.pprint(formatted_results)
                
                # Verificações básicas
                assert 'final_score' in results, "Resultado deve conter final_score"
                assert 'relevance_score' in results, "Resultado deve conter relevance_score"
                assert float(results['final_score']) >= 0, "Score final deve ser >= 0"
                assert float(results['final_score']) <= 1, "Score final deve ser <= 1"
                
                print(f"\n✅ Teste de integração passou para {pdf_file}")
                
            except Exception as e:
                print(f"❌ Erro na avaliação: {e}")
                pytest.fail(f"Falha na avaliação de {pdf_file}: {e}")
    
    def test_extraction_with_different_token_limits(self, input_dir, pdf_files):
        """Testa extração com diferentes limites de tokens"""
        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_dir, pdf_file)
            print(f"\nTestando limites de tokens para: {pdf_file}")
            
            # Teste com limite baixo
            text_1000 = extract_text_from_pdf(pdf_path, max_tokens=1000)
            print(f"1000 tokens: {len(text_1000)} caracteres")
            
            # Teste com limite médio
            text_3000 = extract_text_from_pdf(pdf_path, max_tokens=3000)
            print(f"3000 tokens: {len(text_3000)} caracteres")
            
            # Teste com limite alto
            text_5000 = extract_text_from_pdf(pdf_path, max_tokens=5000)
            print(f"5000 tokens: {len(text_5000)} caracteres")
            
            # Verifica se o truncamento está funcionando
            if text_1000 and text_3000 and text_5000:
                assert len(text_1000) <= 4000, "1000 tokens deve ser <= 4000 chars"
                assert len(text_3000) <= 12000, "3000 tokens deve ser <= 12000 chars"
                assert len(text_5000) <= 20000, "5000 tokens deve ser <= 20000 chars"
                print(f"✅ Truncamento funcionando corretamente para {pdf_file}")
    
    def test_evaluation_with_truncated_text(self, input_dir, pdf_files):
        """Testa avaliação com texto truncado"""
        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_dir, pdf_file)
            print(f"\nTestando avaliação com texto truncado: {pdf_file}")
            
            # Extrai com limite baixo
            article_text = extract_text_from_pdf(pdf_path, max_tokens=2000)
            
            if not article_text:
                pytest.skip(f"Extração falhou para {pdf_file}")
            
            article_theme = self._get_theme_for_pdf(pdf_file)
            
            try:
                results = evaluate_research_paper(article_text, article_theme)
                
                # Verifica se a avaliação funcionou mesmo com texto truncado
                assert 'final_score' in results, "Avaliação deve funcionar com texto truncado"
                assert 'truncation_warning' in results, "Deve haver aviso de truncamento"
                
                print(f"✅ Avaliação com texto truncado funcionou para {pdf_file}")
                print(f"Score final: {results['final_score']:.2f}")
                
            except Exception as e:
                print(f"❌ Erro na avaliação com texto truncado: {e}")
                pytest.fail(f"Falha na avaliação truncada de {pdf_file}: {e}")
    
    def _get_theme_for_pdf(self, pdf_filename: str) -> str:
        """Retorna um tema apropriado baseado no nome do arquivo PDF"""
        filename_lower = pdf_filename.lower()
        
        if "python" in filename_lower:
            return "Python Programming Fundamentals and Best Practices"
        elif "meeting" in filename_lower:
            return "Software Engineering Team Collaboration and Communication"
        elif "neural" in filename_lower or "network" in filename_lower:
            return "Deep Learning and Neural Network Applications"
        elif "borel" in filename_lower or "summation" in filename_lower:
            return "Mathematical Optimization and Numerical Methods"
        else:
            return "Computer Science and Software Development"

if __name__ == "__main__":
    # Execução direta para debug
    test_instance = TestIntegration()
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
    
    print("\n" + "="*60)
    
    # Testa o primeiro PDF encontrado
    pdf_file = pdf_files[0]
    pdf_path = os.path.join(input_dir, pdf_file)
    
    print(f"Testando integração com: {pdf_file}")
    print("="*60)
    
    # Extração
    print(f"\n1. Extraindo texto...")
    article_text = extract_text_from_pdf(pdf_path)
    
    if not article_text:
        print("❌ Falha na extração")
        sys.exit(1)
    
    print(f"✅ Texto extraído: {len(article_text)} caracteres")
    
    # Tema
    article_theme = test_instance._get_theme_for_pdf(pdf_file)
    print(f"\n2. Tema: {article_theme}")
    
    # Avaliação
    print(f"\n3. Avaliando...")
    try:
        results = evaluate_research_paper(article_text, article_theme)
        formatted_results = format_results_for_display(results)
        
        print(f"✅ Avaliação concluída!")
        print(f"\nRESULTADOS:")
        pprint.pprint(formatted_results)
        
    except Exception as e:
        print(f"❌ Erro na avaliação: {e}")
        sys.exit(1) 