# Multi-Agent Healthcare System 🏥

A production-ready multi-agent AI system for healthcare symptom checking, demonstrating advanced agentic AI, ethical AI practices, and secure data handling.

![System Architecture](https://img.shields.io/badge/Architecture-Multi--Agent-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Overview

This project showcases a sophisticated multi-agent system where specialized AI agents collaborate to provide healthcare symptom assessments. The system demonstrates:

- **Agentic AI**: Autonomous agents with specialized roles and decision-making capabilities
- **Multi-Agent Communication**: Structured message-passing protocols between agents
- **LLM Integration**: Advanced prompt engineering for medical knowledge processing
- **Ethical AI**: Bias detection, fairness metrics, and responsible AI practices
- **Privacy & Security**: GDPR-compliant data handling with PII anonymization
- **Conversational AI**: Natural language interaction through modern chatbot frameworks

## 🏗️ Architecture

### Agent Roles

The system consists of three specialized agents working in sequence:

1. **Triage Agent** 🚑
   - Initial symptom intake and processing
   - Urgency level assessment (emergency, high, medium, low)
   - Symptom categorization by body system
   - Patient demographic extraction

2. **Knowledge Agent** 📚
   - Medical knowledge retrieval from knowledge base
   - Symptom-to-condition matching with confidence scoring
   - Evidence-based information assembly
   - Context enrichment for response generation

3. **Response Agent** 💬
   - Natural language response generation
   - Medical information formatting for users
   - Personalization based on user context
   - Safety disclaimers and care recommendations

### Communication Flow

```
User Query
    ↓
Triage Agent (Assess & Categorize)
    ↓
Knowledge Agent (Retrieve & Match)
    ↓
Response Agent (Generate & Format)
    ↓
User Response
```

### Key Components

- **Agent Orchestrator**: Manages agent lifecycle, message routing, and workflow execution
- **Privacy Module**: PII detection, anonymization, and GDPR compliance logging
- **Fairness Module**: Bias detection, fairness metrics, and ethical AI monitoring
- **Message Bus**: Structured JSON-based message passing with conversation tracking
- **State Management**: Redis-backed state persistence (configurable)

## 🚀 Features

### Multi-Agent System
- ✅ Autonomous agents with specialized capabilities
- ✅ Asynchronous message passing with conversation tracking
- ✅ State management and context preservation
- ✅ Performance metrics and monitoring
- ✅ Health checks and error handling

### Ethical AI & Fairness
- ✅ Demographic parity metrics
- ✅ Equalized odds calculations
- ✅ Disparate impact analysis
- ✅ Language bias detection
- ✅ Representation bias monitoring
- ✅ Real-time ethics evaluation

### Privacy & Security
- ✅ PII detection and anonymization (email, phone, SSN, etc.)
- ✅ GDPR-compliant activity logging
- ✅ Data retention policies
- ✅ Consent management
- ✅ Pseudonymization with consistent hashing
- ✅ Data breach logging (Article 33 compliance)

### Conversational AI
- ✅ Natural language understanding
- ✅ Context-aware responses
- ✅ Multi-turn conversation support
- ✅ User-friendly Streamlit interface
- ✅ Response personalization
- ✅ Medical disclaimer integration

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- (Optional) Redis for state persistence

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/multi-agent-healthcare-system.git
cd multi-agent-healthcare-system
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment** (optional)
```bash
cp .env.example .env
# Edit .env with your configurations
```

## 🎯 Usage

### Running the Streamlit Interface

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

### Using the API Programmatically

```python
import asyncio
from src.agents.orchestrator import AgentOrchestrator

# Initialize orchestrator
orchestrator = AgentOrchestrator()

# Process a query
async def check_symptoms():
    result = await orchestrator.process_user_query(
        query="I have a headache and fever",
        user_data={"age": 30, "gender": "female"}
    )
    print(result['response_text'])

# Run
asyncio.run(check_symptoms())
```

### Example Queries

```
"I have a cough, sore throat, and runny nose that started 2 days ago"

"Severe chest pain and difficulty breathing"

"Headache with nausea and sensitivity to light"

"Stomach pain, nausea, and diarrhea for the past day"
```

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v --cov=src
```

### Run Specific Test Suites

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Test coverage report
pytest --cov=src --cov-report=html
```

### Example Test

```python
import pytest
from src.agents.triage_agent import TriageAgent

@pytest.mark.asyncio
async def test_triage_agent():
    agent = TriageAgent()
    
    result = await agent.execute_task({
        "query": "I have a fever and cough",
        "user_data": {"age": 25}
    })
    
    assert result["status"] == "triaged"
    assert "fever" in result["extracted_symptoms"]
    assert result["urgency_level"] in ["low", "medium", "high", "emergency"]
```

## 📊 System Metrics

The system tracks comprehensive metrics:

- **Performance**: Response times, throughput, success rates
- **Agent Activity**: Messages sent/received, tasks completed
- **Privacy**: PII detected, anonymizations performed
- **Ethics**: Bias detections, fairness scores
- **System Health**: Agent status, error rates

Access metrics through:
- Streamlit sidebar (real-time)
- Orchestrator API (`get_metrics()`)
- Prometheus endpoint (optional)

## 🔒 Privacy & GDPR Compliance

### Data Protection

The system implements multiple privacy safeguards:

1. **PII Detection**: Automatically detects personal information
   - Email addresses
   - Phone numbers
   - Social Security numbers
   - Credit card numbers
   - IP addresses
   - Dates of birth

2. **Anonymization**: Multiple strategies
   - Redaction: `[EMAIL]`, `[PHONE]`
   - Pseudonymization: Consistent fake data
   - Hashing: One-way cryptographic hashing

3. **GDPR Logging**: Article 30 compliance
   - Data access logs
   - Consent tracking
   - Deletion requests
   - Breach notifications

### Example: Anonymizing Data

```python
from src.security.privacy import DataAnonymizer

anonymizer = DataAnonymizer()

# Anonymize text
result = anonymizer.anonymize_text(
    "Contact me at john@example.com or 555-1234"
)
# Returns: "Contact me at [EMAIL] or [PHONE]"

# Anonymize user data
user_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
}
anonymized = anonymizer.anonymize_user_data(user_data)
```

## ⚖️ Fairness & Bias Detection

### Implemented Metrics

1. **Demographic Parity**: Equal positive prediction rates across groups
2. **Equalized Odds**: Equal TPR and FPR across groups
3. **Disparate Impact**: 80% rule compliance
4. **Language Bias**: Detection of biased terms and stereotypes
5. **Representation Bias**: Data distribution fairness

### Example: Checking Fairness

```python
from src.fairness.bias_detection import FairnessMetrics

metrics = FairnessMetrics()

predictions = {
    "group_a": [1, 0, 1, 1, 0],
    "group_b": [1, 1, 0, 1, 0]
}

result = metrics.calculate_demographic_parity(predictions)
print(f"Fair: {result['fair']}")
print(f"Max Disparity: {result['max_disparity']}")
```

## 📈 Performance Optimization

### Best Practices Implemented

1. **Async Processing**: Non-blocking agent communication
2. **Message Queuing**: Efficient message handling
3. **Caching**: Anonymization cache for consistency
4. **State Management**: Redis for distributed deployments
5. **Lazy Loading**: On-demand knowledge base loading

### Scalability Considerations

- Horizontal scaling: Add more agent instances
- Load balancing: Distribute queries across agents
- Caching layer: Redis/Memcached for state
- Message queue: RabbitMQ for reliable delivery

## 🎓 Educational Value

### Skills Demonstrated

This project showcases proficiency in:

1. **Agentic AI Design**
   - Agent role definition and specialization
   - Autonomous decision-making
   - Goal-oriented behavior

2. **Multi-Agent Systems**
   - Inter-agent communication protocols
   - Message passing and serialization
   - Workflow orchestration

3. **LLM Integration**
   - Prompt engineering for medical domains
   - Context management
   - Response formatting

4. **Ethical AI**
   - Fairness metrics implementation
   - Bias detection algorithms
   - Responsible AI practices

5. **Security & Privacy**
   - PII protection
   - GDPR compliance
   - Data anonymization techniques

6. **Software Engineering**
   - Clean architecture
   - Comprehensive testing
   - Documentation
   - Production-ready code

## 🗺️ Roadmap

### Phase 1 (Weeks 1-2) ✅
- [x] Core agent implementation
- [x] Basic orchestration
- [x] Simple UI

### Phase 2 (Weeks 3-4) ✅
- [x] Privacy & security features
- [x] Fairness metrics
- [x] Enhanced UI
- [x] Documentation

### Phase 3 (Week 5)
- [ ] Advanced LLM integration
- [ ] Redis state management
- [ ] Performance optimization
- [ ] Comprehensive testing
- [ ] Deployment configuration

### Future Enhancements
- [ ] Integration with real medical databases (SNOMED CT, ICD-10)
- [ ] Support for multiple languages
- [ ] Voice interface
- [ ] Mobile app
- [ ] Telemedicine integration
- [ ] Clinical decision support
- [ ] Medication interaction checking

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 📧 Contact

**Your Name**
- Email: your.harshanandhanreddy820@gmail.com
- LinkedIn: https://www.linkedin.com/in/harshanandhan-reddy-gajulapalli-91a951395/
- GitHub: [@yourusername](https://github.com/Harshanandhan)

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com) and [AutoGen](https://microsoft.github.io/autogen/)
- UI powered by [Streamlit](https://streamlit.io)
- Fairness metrics inspired by [Fairlearn](https://fairlearn.org) and [AIF360](https://aif360.mybluemix.net)
- Medical knowledge structured based on healthcare standards

---

**Star ⭐ this repository if you find it helpful!**
