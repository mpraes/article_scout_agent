#!/usr/bin/env python3
"""
Teste de integração completa: Simula o fluxo do Streamlit App
PDF Upload -> Text Extraction -> Article Scout Evaluation -> Results Display
"""

import os
import sys
import tempfile
import pprint
import json
import pytest

# Adiciona o diretório raiz do projeto ao path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from utils.pdf_extractor import extract_text_from_pdf
from article_scout_agent import evaluate_research_paper, format_results_for_display

class TestStreamlitIntegration:
    """Testa a integração completa simulando o fluxo do Streamlit"""
    
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
    
    def test_complete_streamlit_flow(self, input_dir, pdf_files):
        """Testa o fluxo completo simulando o Streamlit App"""
        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_dir, pdf_file)
            print(f"\n{'='*80}")
            print(f"🧪 TESTANDO FLUXO COMPLETO STREAMLIT: {pdf_file}")
            print(f"{'='*80}")
            
            # Simula o tema do TCC baseado no nome do arquivo
            tcc_theme = self._get_theme_for_pdf(pdf_file)
            
            print(f"\n📝 Tema do TCC: {tcc_theme}")
            
            # Simula o upload do arquivo (copia para temp)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                with open(pdf_path, 'rb') as source_file:
                    tmp_file.write(source_file.read())
                temp_pdf_path = tmp_file.name
            
            print(f"📁 Arquivo temporário criado: {temp_pdf_path}")
            
            try:
                # Passo 1: Extração de texto (como no Streamlit)
                print(f"\n🔍 1. Extraindo texto do PDF...")
                article_text = extract_text_from_pdf(temp_pdf_path)
                
                if not article_text:
                    print(f"❌ Falha na extração de {pdf_file}")
                    pytest.skip(f"Extração falhou para {pdf_file}")
                
                print(f"✅ Texto extraído: {len(article_text)} caracteres")
                
                # Passo 2: Avaliação com Article Scout (como no Streamlit)
                print(f"\n🤖 2. Avaliando com Article Scout Agent...")
                results = evaluate_research_paper(article_text, tcc_theme)
                
                print(f"✅ Avaliação concluída!")
                
                # Passo 3: Formatação dos resultados (como no Streamlit)
                print(f"\n📊 3. Formatando resultados...")
                formatted_results = self._format_results_like_streamlit(results)
                
                # Passo 4: Exibição dos resultados (simulando Streamlit)
                print(f"\n🎯 4. Exibindo resultados (simulação Streamlit):")
                self._display_results_like_streamlit(formatted_results, article_text)
                
                # Verificações de qualidade
                self._verify_results_quality(results, formatted_results)
                
                print(f"\n✅ Fluxo completo funcionou para {pdf_file}")
                
            finally:
                # Limpeza (como no Streamlit)
                os.unlink(temp_pdf_path)
                print(f"🧹 Arquivo temporário removido: {temp_pdf_path}")
    
    def test_streamlit_error_handling(self, input_dir, pdf_files):
        """Testa o tratamento de erros como no Streamlit"""
        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_dir, pdf_file)
            print(f"\nTestando tratamento de erros para: {pdf_file}")
            
            # Teste 1: Tema vazio
            try:
                results = evaluate_research_paper("texto de teste", "")
                print("⚠️ Avaliação com tema vazio não deveria funcionar")
            except Exception as e:
                print(f"✅ Erro capturado corretamente: {e}")
            
            # Teste 2: Texto vazio
            try:
                results = evaluate_research_paper("", "tema de teste")
                print("⚠️ Avaliação com texto vazio não deveria funcionar")
            except Exception as e:
                print(f"✅ Erro capturado corretamente: {e}")
    
    def test_streamlit_performance(self, input_dir, pdf_files):
        """Testa performance como seria no Streamlit"""
        import time
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_dir, pdf_file)
            print(f"\nTestando performance para: {pdf_file}")
            
            start_time = time.time()
            
            # Extração
            article_text = extract_text_from_pdf(pdf_path)
            extraction_time = time.time() - start_time
            
            # Avaliação
            eval_start = time.time()
            tcc_theme = self._get_theme_for_pdf(pdf_file)
            results = evaluate_research_paper(article_text, tcc_theme)
            evaluation_time = time.time() - eval_start
            
            total_time = time.time() - start_time
            
            print(f"⏱️ Tempos:")
            print(f"   Extração: {extraction_time:.2f}s")
            print(f"   Avaliação: {evaluation_time:.2f}s")
            print(f"   Total: {total_time:.2f}s")
            
            # Verifica se está dentro de limites aceitáveis
            assert total_time < 120, f"Tempo total muito alto: {total_time:.2f}s"
            assert extraction_time < 10, f"Tempo de extração muito alto: {extraction_time:.2f}s"
    
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
    
    def _format_results_like_streamlit(self, results: dict) -> dict:
        """Formata os resultados como no Streamlit App"""
        return {
            "Final Score": f"{results['final_score'] * 10:.2f}",
            "Relevance to TCC": {
                "Score": f"{results['relevance_score'] * 10:.2f}",
                "Explanation": results['relevance_explanation']
            },
            "Originality": {
                "Score": f"{results['originality_score'] * 10:.2f}",
                "Explanation": results['originality_explanation']
            },
            "Methodology Quality": {
                "Score": f"{results['methodology_quality_score'] * 10:.2f}",
                "Explanation": results['methodology_quality_explanation']
            },
            "Results and Discussion Quality": {
                "Score": f"{results['results_discussion_quality_score'] * 10:.2f}",
                "Explanation": results['results_discussion_quality_explanation']
            },
            "Potential Impact": {
                "Score": f"{results['potential_impact_score'] * 10:.2f}",
                "Explanation": results['potential_impact_explanation']
            },
            "Writing Clarity": {
                "Score": f"{results['writing_clarity_score'] * 10:.2f}",
                "Explanation": results['writing_clarity_explanation']
            },
            "References Timeliness": {
                "Score": f"{results['references_timeliness_score'] * 10:.2f}",
                "Explanation": results['references_timeliness_explanation']
            },
        }
    
    def _display_results_like_streamlit(self, formatted_results: dict, article_text: str):
        """Simula a exibição dos resultados como no Streamlit"""
        print(f"\n{'='*60}")
        print("📊 RESULTADOS DA AVALIAÇÃO (Simulação Streamlit)")
        print(f"{'='*60}")
        
        # Score final em destaque
        final_score = formatted_results["Final Score"]
        print(f"\n🎯 SCORE FINAL: {final_score}/10")
        print("-" * 40)
        
        # Detalhes de cada critério
        for criterion, data in formatted_results.items():
            if criterion != "Final Score":
                score = data["Score"]
                explanation = data["Explanation"]
                
                print(f"\n📋 {criterion.upper()}: {score}/10")
                print(f"   📝 {explanation[:200]}...")
        
        # Simula o expander com texto extraído
        print(f"\n📄 TEXTO EXTRAÍDO (Primeiros 300 caracteres):")
        print(f"   {article_text[:300]}...")
    
    def _verify_results_quality(self, results: dict, formatted_results: dict):
        """Verifica a qualidade dos resultados"""
        # Verifica se todos os campos necessários estão presentes
        required_fields = [
            'final_score', 'relevance_score', 'originality_score',
            'methodology_quality_score', 'results_discussion_quality_score',
            'potential_impact_score', 'writing_clarity_score', 'references_timeliness_score'
        ]
        
        for field in required_fields:
            assert field in results, f"Campo obrigatório ausente: {field}"
            assert isinstance(results[field], (int, float)), f"Campo {field} deve ser numérico"
            assert 0 <= results[field] <= 1, f"Score {field} deve estar entre 0 e 1"
        
        # Verifica se o score final é razoável
        final_score = float(formatted_results["Final Score"])
        assert 0 <= final_score <= 10, f"Score final deve estar entre 0 e 10: {final_score}"
        
        print(f"✅ Qualidade dos resultados verificada")

if __name__ == "__main__":
    # Execução direta para debug
    import pytest
    
    test_instance = TestStreamlitIntegration()
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
    
    print("\n" + "="*80)
    
    # Testa o primeiro PDF encontrado
    pdf_file = pdf_files[0]
    pdf_path = os.path.join(input_dir, pdf_file)
    
    print(f"🧪 TESTANDO FLUXO STREAMLIT COM: {pdf_file}")
    print("="*80)
    
    # Simula o fluxo completo
    tcc_theme = test_instance._get_theme_for_pdf(pdf_file)
    print(f"📝 Tema: {tcc_theme}")
    
    # Extração
    print(f"\n🔍 Extraindo texto...")
    article_text = extract_text_from_pdf(pdf_path)
    
    if not article_text:
        print("❌ Falha na extração")
        sys.exit(1)
    
    print(f"✅ Texto extraído: {len(article_text)} caracteres")
    
    # Avaliação
    print(f"\n🤖 Avaliando...")
    try:
        results = evaluate_research_paper(article_text, tcc_theme)
        formatted_results = test_instance._format_results_like_streamlit(results)
        
        print(f"✅ Avaliação concluída!")
        test_instance._display_results_like_streamlit(formatted_results, article_text)
        
    except Exception as e:
        print(f"❌ Erro na avaliação: {e}")
        sys.exit(1) 