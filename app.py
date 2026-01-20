"""
Streamlit Web Interface for Multi-Agent Healthcare System
"""

import streamlit as st
import asyncio
import json
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.orchestrator import AgentOrchestrator
from src.security.privacy import DataAnonymizer, GDPRComplianceLogger
from src.fairness.bias_detection import EthicalAIMonitor


# Page configuration
st.set_page_config(
    page_title="HealthAssist AI - Multi-Agent Symptom Checker",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .urgency-emergency {
        background-color: #ff4444;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
        text-align: center;
    }
    .urgency-high {
        background-color: #ff9900;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
        text-align: center;
    }
    .urgency-medium {
        background-color: #ffcc00;
        color: black;
        padding: 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
        text-align: center;
    }
    .urgency-low {
        background-color: #44ff44;
        color: black;
        padding: 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
        text-align: center;
    }
    .agent-message {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .disclaimer {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = AgentOrchestrator()
    st.session_state.anonymizer = DataAnonymizer()
    st.session_state.gdpr_logger = GDPRComplianceLogger()
    st.session_state.ethics_monitor = EthicalAIMonitor()
    st.session_state.conversation_history = []


def display_header():
    """Display application header"""
    st.markdown('<div class="main-header">🏥 HealthAssist AI</div>', unsafe_allow_html=True)
    st.markdown("### Multi-Agent Symptom Checker System")
    st.markdown("*An AI-powered healthcare assistant using multi-agent architecture*")
    st.markdown("---")


def display_sidebar():
    """Display sidebar with system information"""
    with st.sidebar:
        st.header("ℹ️ System Information")
        
        # Agent status
        st.subheader("Active Agents")
        agents = st.session_state.orchestrator.get_all_agent_info()
        for agent in agents:
            with st.expander(f"🤖 {agent['name']}"):
                st.write(f"**ID:** {agent['agent_id']}")
                st.write(f"**Capabilities:** {', '.join(agent['capabilities'])}")
                st.write(f"**Tasks Completed:** {agent['performance_metrics']['tasks_completed']}")
                st.write(f"**Messages:** {agent['performance_metrics']['messages_sent']} sent, {agent['performance_metrics']['messages_received']} received")
        
        st.markdown("---")
        
        # System metrics
        st.subheader("📊 System Metrics")
        metrics = st.session_state.orchestrator.get_metrics()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Conversations", metrics['total_conversations'])
            st.metric("Active Agents", metrics['num_agents'])
        with col2:
            st.metric("Success Rate", f"{(metrics['successful_completions'] / max(metrics['total_conversations'], 1) * 100):.1f}%")
            st.metric("Avg Response Time", f"{metrics['average_response_time']:.2f}s")
        
        st.markdown("---")
        
        # Privacy controls
        st.subheader("🔒 Privacy & Ethics")
        privacy_enabled = st.checkbox("Enable PII Anonymization", value=True)
        ethics_monitoring = st.checkbox("Enable Ethics Monitoring", value=True)
        
        st.session_state.privacy_enabled = privacy_enabled
        st.session_state.ethics_monitoring = ethics_monitoring
        
        if st.button("View Ethics Report"):
            show_ethics_report()
        
        st.markdown("---")
        
        # Disclaimer
        with st.expander("⚠️ Important Disclaimer"):
            st.warning("""
            **Medical Disclaimer:**
            
            This system is for educational and informational purposes only. 
            It is NOT a substitute for professional medical advice, diagnosis, 
            or treatment.
            
            Always seek the advice of your physician or other qualified health 
            provider with any questions you may have regarding a medical condition.
            
            **In case of emergency, call 911 or go to your nearest emergency room.**
            """)


def process_query_async(query: str, user_data: dict):
    """Process query using async orchestrator"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(
        st.session_state.orchestrator.process_user_query(query, user_data)
    )
    loop.close()
    return result


def display_urgency_banner(urgency_level: str):
    """Display urgency level banner"""
    urgency_classes = {
        "emergency": "urgency-emergency",
        "high": "urgency-high",
        "medium": "urgency-medium",
        "low": "urgency-low"
    }
    
    urgency_messages = {
        "emergency": "⚠️ EMERGENCY - SEEK IMMEDIATE MEDICAL ATTENTION ⚠️",
        "high": "⚠️ HIGH PRIORITY - Prompt Medical Evaluation Recommended",
        "medium": "⚡ MEDIUM PRIORITY - Schedule Medical Consultation",
        "low": "✓ LOW PRIORITY - Self-Care May Be Appropriate"
    }
    
    css_class = urgency_classes.get(urgency_level, "urgency-low")
    message = urgency_messages.get(urgency_level, "Assessment Complete")
    
    st.markdown(f'<div class="{css_class}">{message}</div>', unsafe_allow_html=True)


def display_response(result: dict):
    """Display the response from the multi-agent system"""
    if result.get('status') == 'error':
        st.error(f"Error: {result.get('error', 'Unknown error')}")
        return
    
    # Display urgency banner
    urgency_level = result.get('urgency_level', 'low')
    display_urgency_banner(urgency_level)
    
    st.markdown("---")
    
    # Main response
    st.markdown("### 📋 Assessment Results")
    response_text = result.get('response_text', 'No response generated')
    st.markdown(response_text)
    
    # Display extracted symptoms
    if result.get('extracted_symptoms'):
        st.markdown("---")
        st.markdown("### 🔍 Detected Symptoms")
        symptoms = result.get('extracted_symptoms', [])
        cols = st.columns(min(len(symptoms), 4))
        for i, symptom in enumerate(symptoms):
            with cols[i % len(cols)]:
                st.info(f"✓ {symptom}")
    
    # Display matched conditions
    if result.get('condition_details'):
        st.markdown("---")
        st.markdown("### 🏥 Possible Conditions")
        
        for condition in result.get('condition_details', []):
            with st.expander(
                f"{condition['condition_name']} - {int(condition['confidence'] * 100)}% match"
            ):
                st.write(f"**Duration:** {condition.get('typical_duration', 'N/A')}")
                
                if condition.get('matching_symptoms'):
                    st.write("**Matching Symptoms:**")
                    for symptom in condition['matching_symptoms']:
                        st.write(f"  • {symptom}")
                
                if condition.get('self_care'):
                    st.write("**Self-Care Recommendations:**")
                    for tip in condition['self_care']:
                        st.write(f"  • {tip}")


def display_agent_communication(conversation_id: str):
    """Display agent-to-agent communication logs"""
    st.markdown("### 🔄 Agent Communication Log")
    
    conversation = st.session_state.orchestrator.get_conversation_log(conversation_id)
    
    if not conversation or not conversation.get('messages'):
        st.info("No agent communication logs available")
        return
    
    messages = conversation.get('messages', [])
    
    for i, msg in enumerate(messages):
        sender = msg.get('sender_id', 'unknown')
        receiver = msg.get('receiver_id', 'unknown')
        msg_type = msg.get('message_type', 'unknown')
        timestamp = msg.get('timestamp', '')
        
        with st.expander(
            f"Message {i+1}: {sender} → {receiver} ({msg_type})",
            expanded=(i == 0)
        ):
            st.json({
                "Message ID": msg.get('message_id'),
                "Timestamp": timestamp,
                "Type": msg_type,
                "Sender": sender,
                "Receiver": receiver,
                "Content Keys": list(msg.get('content', {}).keys())
            })


def show_ethics_report():
    """Display ethics monitoring report"""
    st.markdown("### 🛡️ Ethics & Fairness Report")
    
    report = st.session_state.ethics_monitor.generate_ethics_report()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Evaluations", report['total_evaluations'])
    with col2:
        st.metric("Issues Detected", report['issues_detected'])
    with col3:
        issue_rate = report.get('issue_rate', 0) * 100
        st.metric("Issue Rate", f"{issue_rate:.1f}%")
    
    status = report.get('status', 'unknown')
    if status == 'healthy':
        st.success("✓ System operating within ethical guidelines")
    else:
        st.warning("⚠️ Ethics review recommended")


def main():
    """Main application"""
    display_header()
    display_sidebar()
    
    # Main content area
    st.markdown("## 💬 Describe Your Symptoms")
    st.write("Tell us about what you're experiencing, and our AI agents will analyze your symptoms.")
    
    # User input form
    with st.form("symptom_form"):
        # Query input
        user_query = st.text_area(
            "What symptoms are you experiencing?",
            height=150,
            placeholder="Example: I have a headache, fever, and sore throat that started yesterday..."
        )
        
        # Optional user information
        with st.expander("Optional: Additional Information"):
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Age", min_value=0, max_value=120, value=None)
                gender = st.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Other"])
            with col2:
                chronic_conditions = st.checkbox("I have chronic health conditions")
        
        submitted = st.form_submit_button("🔍 Analyze Symptoms", type="primary", use_container_width=True)
    
    # Process query
    if submitted and user_query:
        with st.spinner("🤖 Our AI agents are analyzing your symptoms..."):
            # Prepare user data
            user_data = {
                "age": age if age else None,
                "gender": gender if gender != "Prefer not to say" else None,
                "chronic_conditions": chronic_conditions
            }
            
            # Anonymize if enabled
            if st.session_state.get('privacy_enabled', True):
                user_query_processed = st.session_state.anonymizer.anonymize_text(user_query)
                query_to_process = user_query_processed['anonymized_text']
                
                if user_query_processed['pii_detected']:
                    st.info(f"🔒 Protected PII: {', '.join(user_query_processed['pii_detected'])}")
            else:
                query_to_process = user_query
            
            # Process query
            result = process_query_async(query_to_process, user_data)
            
            # Ethics monitoring
            if st.session_state.get('ethics_monitoring', True):
                ethics_eval = st.session_state.ethics_monitor.evaluate_response(
                    result.get('response_text', ''),
                    user_data
                )
                if ethics_eval.get('has_issues'):
                    st.warning("⚠️ Ethics monitoring detected potential issues in response")
            
            # Store in conversation history
            st.session_state.conversation_history.append({
                "timestamp": datetime.now(),
                "query": user_query,
                "result": result
            })
            
            # Display results
            display_response(result)
            
            # Show agent communication
            st.markdown("---")
            with st.expander("🔍 View Agent Communication Details"):
                display_agent_communication(result.get('conversation_id'))
    
    elif submitted and not user_query:
        st.warning("⚠️ Please describe your symptoms before submitting")
    
    # Previous conversations
    if st.session_state.conversation_history:
        st.markdown("---")
        st.markdown("## 📜 Previous Conversations")
        
        for i, conv in enumerate(reversed(st.session_state.conversation_history[-5:])):
            with st.expander(
                f"{conv['timestamp'].strftime('%Y-%m-%d %H:%M')} - {conv['query'][:50]}..."
            ):
                display_response(conv['result'])


if __name__ == "__main__":
    main()
