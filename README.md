# Article Scout 📚

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Article Scout** is an intelligent research paper evaluation system that helps students and researchers assess the relevance and quality of academic papers for their TCC (Final Project) or research work.

## 🌟 Features / Funcionalidades

### 🔍 **PDF Text Extraction**
- Multi-method PDF text extraction (PyPDF2, pdfminer.six, PyMuPDF)
- Automatic text truncation for API limits
- Support for various PDF formats

### 🤖 **AI-Powered Evaluation**
- Comprehensive paper evaluation using Groq LLM
- Multiple evaluation criteria:
  - Relevance to research theme
  - Originality and novelty
  - Methodology quality
  - Results and discussion quality
  - Potential impact
  - Writing clarity
  - References timeliness

### 📊 **Interactive Web Interface**
- Streamlit-based web application
- Real-time evaluation results
- User-friendly interface
- Detailed explanations for each criterion

### 🧪 **Comprehensive Testing**
- Unit tests for PDF extraction
- Integration tests for complete workflow
- Performance testing
- Error handling validation

---

## 🚀 Quick Start / Início Rápido

### Prerequisites / Pré-requisitos

```bash
# Python 3.12+
# Groq API Key
# Required packages (see requirements.txt)
```

### Installation / Instalação

```bash
# Clone the repository
git clone https://github.com/yourusername/article-scout.git
cd article-scout

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Usage / Uso

#### Web Application / Aplicação Web
```bash
# Start Streamlit app
streamlit run streamlit_app.py
```

#### Command Line / Linha de Comando
```bash
# Test PDF extraction
python3 -m pytest tests/test_pdf_extraction.py -v

# Test complete integration
python3 -m pytest tests/test_integration.py -v

# Test Streamlit integration
python3 -m pytest tests/test_streamlit_integration.py -v
```

---

## 📁 Project Structure / Estrutura do Projeto

```
article_scout/
├── 📁 input_files/              # PDF files for testing
├── 📁 utils/
│   ├── __init__.py
│   └── pdf_extractor.py         # PDF text extraction module
├── 📁 tests/
│   ├── __init__.py
│   ├── test_pdf_extraction.py   # PDF extraction tests
│   ├── test_integration.py      # Integration tests
│   └── test_streamlit_integration.py  # Streamlit flow tests
├── article_scout_agent.py       # Main evaluation engine
├── streamlit_app.py             # Web interface
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

---

## 🔧 Configuration / Configuração

### Environment Variables / Variáveis de Ambiente

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### API Limits / Limites da API

- **Input limit**: 5000 characters (configurable in `article_scout_agent.py`)
- **Model**: llama-3.1-8b-instant (Groq)
- **Temperature**: 0.3 (for consistent results)

---

## 🧪 Testing / Testes

### Running Tests / Executando Testes

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test categories
python3 -m pytest tests/test_pdf_extraction.py -v      # PDF extraction
python3 -m pytest tests/test_integration.py -v         # Integration
python3 -m pytest tests/test_streamlit_integration.py -v  # Streamlit flow

# Run with detailed output
python3 -m pytest tests/ -v -s
```

### Test Coverage / Cobertura de Testes

- ✅ PDF text extraction with multiple methods
- ✅ Article Scout Agent evaluation workflow
- ✅ Streamlit integration flow
- ✅ Error handling and edge cases
- ✅ Performance testing
- ✅ API limit handling

---

## 📊 Evaluation Criteria / Critérios de Avaliação

The Article Scout evaluates papers based on 7 key criteria:

| Criterion / Critério | Weight / Peso | Description / Descrição |
|---------------------|---------------|-------------------------|
| **Relevance** | 20% | How well the paper aligns with your research theme |
| **Originality** | 15% | Novelty and innovation of the work |
| **Methodology** | 15% | Quality and robustness of research methods |
| **Results & Discussion** | 15% | Clarity and soundness of findings |
| **Potential Impact** | 15% | Significance and implications of the work |
| **Writing Clarity** | 10% | Readability and communication quality |
| **References** | 10% | Timeliness and relevance of citations |

---

## 🔄 Workflow / Fluxo de Trabalho

```
1. 📁 PDF Upload
   ↓
2. 🔍 Text Extraction (utils/pdf_extractor.py)
   ↓
3. 🤖 AI Evaluation (article_scout_agent.py)
   ↓
4. 📊 Results Display (streamlit_app.py)
```

### Detailed Flow / Fluxo Detalhado

1. **PDF Upload**: User uploads a research paper PDF
2. **Text Extraction**: System extracts text using multiple methods
3. **Text Truncation**: If needed, text is truncated to fit API limits
4. **AI Evaluation**: Article Scout Agent evaluates the paper
5. **Results Formatting**: Results are formatted for display
6. **Web Display**: Results are shown in the Streamlit interface

---

## 🛠️ Development / Desenvolvimento

### Adding New Features / Adicionando Novas Funcionalidades

1. **PDF Extraction Methods**:
   - Add new method in `utils/pdf_extractor.py`
   - Update fallback chain in `try_pdfminer()` or `try_pymupdf()`

2. **Evaluation Criteria**:
   - Add new criterion in `article_scout_agent.py`
   - Update `State` TypedDict and workflow
   - Add corresponding test cases

3. **Web Interface**:
   - Modify `streamlit_app.py` for new features
   - Update result formatting functions

### Code Style / Estilo de Código

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for all functions
- Write comprehensive tests

---

## 🐛 Troubleshooting / Solução de Problemas

### Common Issues / Problemas Comuns

#### PDF Extraction Fails / Falha na Extração de PDF
```bash
# Check if PDF is image-based
python3 -c "from utils.pdf_extractor import extract_text_from_pdf; print(extract_text_from_pdf('your_file.pdf'))"
```

#### API Key Issues / Problemas com Chave da API
```bash
# Verify environment variable
echo $GROQ_API_KEY
# or
python3 -c "import os; print(os.getenv('GROQ_API_KEY'))"
```

#### Import Errors / Erros de Importação
```bash
# Check Python path
python3 -c "import sys; print(sys.path)"
# Ensure you're in the project root directory
```

---

## 📈 Performance / Performance

### Benchmarks / Benchmarks

- **PDF Extraction**: < 10 seconds for most files
- **AI Evaluation**: < 60 seconds for standard papers
- **Total Workflow**: < 2 minutes end-to-end

### Optimization Tips / Dicas de Otimização

- Use smaller PDFs when possible
- Consider pre-processing large documents
- Cache evaluation results for repeated papers

---

## 🤝 Contributing / Contribuindo

### How to Contribute / Como Contribuir

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup / Configuração de Desenvolvimento

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
flake8 .

# Run type checking
mypy .

# Run all tests
python3 -m pytest tests/ -v --cov=.
```

---

## 📄 License / Licença

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🙏 Acknowledgments / Agradecimentos

- **Groq** for providing the LLM API
- **Streamlit** for the web framework
- **PyPDF2** and **pdfminer.six** for PDF processing
- **LangGraph** for workflow orchestration

---

## 📞 Support / Suporte

- **Issues**: [GitHub Issues](https://github.com/yourusername/article-scout/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/article-scout/discussions)
- **Email**: your.email@example.com

---

## 🔄 Changelog / Histórico de Versões

### v1.0.0 (2024-01-XX)
- ✅ Initial release
- ✅ PDF text extraction with multiple methods
- ✅ AI-powered paper evaluation
- ✅ Streamlit web interface
- ✅ Comprehensive test suite
- ✅ Integration testing framework

---

**Made with ❤️ for the academic community**

**Feito com ❤️ para a comunidade acadêmica**
