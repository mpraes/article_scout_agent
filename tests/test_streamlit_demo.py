#!/usr/bin/env python3
"""
Demo da integração completa: PDF -> Extração -> Avaliação -> Resultados
Simula o fluxo do Streamlit App de forma simples
"""

import os
import sys
import tempfile
import pprint

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.pdf_extractor import extract_text_from_pdf
from article_scout_agent import evaluate_research_paper

def main():
    """Demonstra o fluxo completo da integração"""
    
    print("🚀 DEMO: Integração Completa Streamlit + Article Scout")
    print("=" * 60)
    
    # 1. Encontra PDFs disponíveis
    input_dir = "input_files"
    if not os.path.exists(input_dir):
        print(f"❌ Diretório {input_dir} não encontrado!")
        return
    
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"❌ Nenhum PDF encontrado em {input_dir}")
        return
    
    print(f"📁 PDFs disponíveis:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"   {i}. {pdf_file}")
    
    # 2. Usa o primeiro PDF para demonstração
    pdf_file = pdf_files[0]
    pdf_path = os.path.join(input_dir, pdf_file)
    
    print(f"\n🎯 Testando com: {pdf_file}")
    print("-" * 40)
    
    # 3. Simula upload do arquivo (cria arquivo temporário)
    print("📤 Simulando upload do arquivo...")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        with open(pdf_path, 'rb') as source_file:
            tmp_file.write(source_file.read())
        temp_pdf_path = tmp_file.name
    
    print(f"✅ Arquivo temporário criado: {temp_pdf_path}")
    
    try:
        # 4. Extração de texto (como no Streamlit)
        print(f"\n🔍 Extraindo texto do PDF...")
        article_text = extract_text_from_pdf(temp_pdf_path)
        
        if not article_text:
            print("❌ Falha na extração de texto")
            return
        
        print(f"✅ Texto extraído: {len(article_text)} caracteres")
        
        # 5. Define tema do TCC
        tcc_theme = get_theme_for_pdf(pdf_file)
        print(f"\n📝 Tema do TCC: {tcc_theme}")
        
        # 6. Avaliação com Article Scout (como no Streamlit)
        print(f"\n🤖 Avaliando com Article Scout Agent...")
        results = evaluate_research_paper(article_text, tcc_theme)
        
        print(f"✅ Avaliação concluída!")
        
        # 7. Formatação dos resultados (como no Streamlit)
        print(f"\n📊 Formatando resultados...")
        formatted_results = format_results_like_streamlit(results)
        
        # 8. Exibição dos resultados (simulando Streamlit)
        print(f"\n🎯 RESULTADOS DA AVALIAÇÃO:")
        print("=" * 50)
        
        # Score final em destaque
        final_score = formatted_results["Final Score"]
        print(f"\n🏆 SCORE FINAL: {final_score}/10")
        print("-" * 30)
        
        # Detalhes de cada critério
        for criterion, data in formatted_results.items():
            if criterion != "Final Score":
                score = data["Score"]
                explanation = data["Explanation"]
                
                print(f"\n📋 {criterion.upper()}: {score}/10")
                print(f"   📝 {explanation[:150]}...")
        
        # 9. Informações adicionais
        print(f"\n📄 INFORMAÇÕES ADICIONAIS:")
        print(f"   • Texto extraído: {len(article_text)} caracteres")
        print(f"   • Arquivo original: {pdf_file}")
        print(f"   • Tema avaliado: {tcc_theme}")
        
        if 'truncation_warning' in results and results['truncation_warning']:
            print(f"   ⚠️ {results['truncation_warning']}")
        
        print(f"\n✅ Demo concluído com sucesso!")
        
    finally:
        # Limpeza (como no Streamlit)
        os.unlink(temp_pdf_path)
        print(f"🧹 Arquivo temporário removido")

def get_theme_for_pdf(pdf_filename: str) -> str:
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

def format_results_like_streamlit(results: dict) -> dict:
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

if __name__ == "__main__":
    main() 