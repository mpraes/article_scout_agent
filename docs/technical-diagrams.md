# Technical Diagrams 📊

This document contains detailed technical diagrams for the Article Scout project.

## 🔄 Data Flow Diagram

```mermaid
flowchart TD
    A[User Input] --> B[Streamlit Interface]
    B --> C[PDF Upload]
    C --> D[PDF Extractor]
    D --> E{Extraction Method}
    E -->|Method 1| F[PyPDF2]
    E -->|Method 2| G[pdfminer.six]
    E -->|Method 3| H[PyMuPDF]
    F --> I[Text Processing]
    G --> I
    H --> I
    I --> J[Token Limit Check]
    J --> K[AI Agent]
    K --> L[Groq API]
    L --> M[Evaluation Results]
    M --> N[Score Calculation]
    N --> O[Results Display]
    
    style A fill:#e8f5e8
    style O fill:#e3f2fd
    style L fill:#fff3e0
```

## 🏗️ Component Architecture

```mermaid
graph TB
    subgraph "Presentation Layer"
        A[Streamlit Web App]
        B[User Interface]
    end
    
    subgraph "Application Layer"
        C[Article Scout Agent]
        D[PDF Extractor]
        E[Configuration Manager]
    end
    
    subgraph "External Services"
        F[Groq AI API]
        G[PDF Processing Libraries]
    end
    
    subgraph "Data Layer"
        H[Environment Variables]
        I[Settings Configuration]
        J[PDF Files]
    end
    
    A --> B
    B --> C
    B --> D
    C --> F
    D --> G
    E --> H
    E --> I
    D --> J
    
    style A fill:#e3f2fd
    style C fill:#f3e5f5
    style F fill:#fff3e0
```

## 🔍 PDF Processing Pipeline

```mermaid
sequenceDiagram
    participant U as User
    participant S as Streamlit
    participant P as PDF Extractor
    participant A as AI Agent
    participant G as Groq API
    
    U->>S: Upload PDF + TCC Theme
    S->>P: Extract Text
    P->>P: Try PyPDF2
    alt Success
        P->>S: Return Text
    else Failure
        P->>P: Try pdfminer.six
        alt Success
            P->>S: Return Text
        else Failure
            P->>P: Try PyMuPDF
            P->>S: Return Text
        end
    end
    S->>A: Process with AI
    A->>G: API Request
    G->>A: Evaluation Results
    A->>S: Formatted Results
    S->>U: Display Evaluation
```

## 📊 Evaluation Criteria Flow

```mermaid
graph LR
    A[Research Paper] --> B[AI Analysis]
    B --> C[Relevance Score]
    B --> D[Originality Score]
    B --> E[Methodology Score]
    B --> F[Results Score]
    B --> G[Impact Score]
    B --> H[Clarity Score]
    B --> I[References Score]
    
    C --> J[Weighted Calculation]
    D --> J
    E --> J
    F --> J
    G --> J
    H --> J
    I --> J
    
    J --> K[Final Score]
    
    style A fill:#e8f5e8
    style K fill:#e3f2fd
    style J fill:#fff3e0
```

## 🚀 Deployment Architecture

```mermaid
graph TB
    subgraph "Development Environment"
        A[Local Development]
        B[uv Package Manager]
        C[Streamlit Local]
    end
    
    subgraph "Container Environment"
        D[Docker Container]
        E[Python 3.12]
        F[uv Environment]
        G[Streamlit Server]
    end
    
    subgraph "External Services"
        H[Groq API]
        I[PDF Processing]
    end
    
    A --> B
    B --> C
    C --> H
    C --> I
    
    D --> E
    E --> F
    F --> G
    G --> H
    G --> I
    
    style A fill:#e8f5e8
    style D fill:#e3f2fd
    style H fill:#fff3e0
```

## 🔧 Configuration Management

```mermaid
graph TD
    A[Environment Variables] --> B[Settings Manager]
    B --> C[API Configuration]
    B --> D[PDF Settings]
    B --> E[Streamlit Config]
    
    C --> F[Groq API Key]
    C --> G[Model Selection]
    C --> H[Temperature]
    
    D --> I[Max Tokens]
    D --> J[Max Characters]
    
    E --> K[Server Port]
    E --> L[Server Address]
    
    style A fill:#e8f5e8
    style B fill:#fff3e0
    style F fill:#ffcdd2
```

## 🧪 Testing Strategy

```mermaid
graph TD
    A[Test Suite] --> B[Unit Tests]
    A --> C[Integration Tests]
    A --> D[End-to-End Tests]
    
    B --> E[PDF Extractor Tests]
    B --> F[AI Agent Tests]
    B --> G[Configuration Tests]
    
    C --> H[Streamlit Integration]
    C --> I[API Integration]
    C --> J[Data Flow Tests]
    
    D --> K[Complete User Flow]
    D --> L[Error Handling]
    D --> M[Performance Tests]
    
    style A fill:#e8f5e8
    style K fill:#e3f2fd
    style E fill:#fff3e0
```
