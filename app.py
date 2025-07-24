import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Professional styling similar to RetireHub
st.set_page_config(
    page_title="RetireChat - AI Retirement Planning Coach",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main styling inspired by RetireHub */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
        color: #3b82f6;
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        color: #6b7280;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .dashboard-section {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #3b82f6;
    }
    
    .section-title {
        color: #1f2937;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .sidebar .sidebar-content {
        background: #f1f5f9;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .suggested-prompt {
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .suggested-prompt:hover {
        background: #e2e8f0;
        border-color: #3b82f6;
    }
    
    .chat-container {
        background: white;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        min-height: 400px;
    }
    
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.875rem;
        padding: 2rem 0;
        border-top: 1px solid #e5e7eb;
        margin-top: 2rem;
    }
    
    /* Chat message styling */
    .stChatMessage > div {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
    }
    
    /* Button styling */
    .stButton > button {
        background: #3b82f6;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #2563eb;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

RETIREMENT_COACH_PROMPT = """
You are an expert Retirement Planning Coach providing personalized retirement planning suggestions.

Goals:
* Getting to know the user: Start by asking about their current age and what stage of their career they are in (early career, mid-career, late career, near retirement, etc.). This helps personalize all advice.
* Understand the user's current retirement plan: use available data to learn about their plan. Tailor advice based on this information. Ask the user to describe their plan, savings, challenges, and debt.
* Identify retirement goals: ask about short-term and long-term goals. What age of retirement are they planning for? How much do they want to have saved at time of retirement?
* Assess skills and gaps: evaluate current skills and identify gaps to achieve career goals to achieve their priorities.
* Suggest learning opportunities: recommend courses, certifications, workshops, or other learning opportunities to acquire necessary skills.
* Create a plan of action: develop a step-by-step plan with actions, timelines, and milestone. If asked for a detailed plan, include immediate actions, next 3 months, next 6 months, next 1-2 years, and ongoing.
* Plan finalization: Once user expresses satisfaction in plan, ask the user if they wish the AI to create a printable professional document outlining their Plan of Action.

Overall direction:
* Make responses relevant to the user's current or desired plan
* Avoid overwhelming the user with multiple questions at one
* Ask clarifying and follow-up questions
* Be encouraging and maintain a professional, supportive tone
* Keep context across the conversation, ensuring ideas and responses relate to previous turns
* After each subtopic, ask if the user has follow-up questions or needs further help
* If greeted or asked what you can do, briefly explain your purpose with concise examples, then ask about their age and career stage to personalize your advice
* If asked unrelated questions, answer but try to refocus on retirement planning, financial wellness, and financial 101 questions.
* If asked about what certain plans are and their definition, or if you pull any information from a source, make sure it is credible and to have a little source link so that they can verify that your information is certifiable and correct
* At the end of each conversation, ask how you did and encourage feedback using the thumbs up or down.

Knowledge:
Https://2025-benefits.segalco.com/
Https://www.psca.org/news/psca-news/
"""

def get_ai_response(user_input, conversation_history):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Build conversation context
        context = RETIREMENT_COACH_PROMPT + "\n\nConversation History:\n"
        for msg in conversation_history[-10:]:  # Keep last 10 messages for context
            role = "User" if msg["role"] == "user" else "Assistant"
            context += f"{role}: {msg['content']}\n"
        
        context += f"\nUser: {user_input}\nAssistant:"
        
        response = model.generate_content(
            context,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=1000,
                temperature=0.7,
            )
        )
        return response.text
    except Exception as e:
        return f"I apologize, but I'm having trouble connecting to the AI service. Error: {str(e)}"

def main():
    # Main header section
    st.markdown("""
    <div class="main-header">
        <h1>💰 RetireChat</h1>
        <p>AI-Powered Retirement Planning That Improves Lives</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Features overview section
        st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🎯 Retirement Planning Customized for You</div>', unsafe_allow_html=True)
        
        # Feature cards
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Personalized Assessment</div>
                <div class="feature-description">Get customized advice based on your current financial situation and retirement goals</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📈</div>
                <div class="feature-title">Goal Planning</div>
                <div class="feature-description">Define short-term and long-term retirement objectives with actionable timelines</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_c:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🎓</div>
                <div class="feature-title">Learning Opportunities</div>
                <div class="feature-description">Discover courses, certifications, and resources to enhance your financial knowledge</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat interface section
        st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">💬 AI Retirement Planning Assistant</div>', unsafe_allow_html=True)
        st.markdown("Get personalized answers to your retirement planning questions, powered by financial planning expertise")
        
        # Display chat messages
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Sidebar content
        st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🚀 Quick Start</div>', unsafe_allow_html=True)
        
        st.markdown("Choose a topic to get started with your retirement planning journey:")
        
        # Suggested prompts as clickable cards
        if st.button("🎯 Create Retirement Development Plan", key="prompt1", help="Get a comprehensive retirement strategy"):
            st.session_state.suggested_prompt = "Help me create a detailed retirement development plan based on my current financial situation and future goals."
        
        if st.button("📊 Skill Gap Analysis", key="prompt2", help="Identify areas for career advancement"):
            st.session_state.suggested_prompt = "Analyze my current skills and identify any gaps that I need to fill to advance in my career."
        
        if st.button("📚 Learning Opportunities", key="prompt3", help="Discover educational resources"):
            st.session_state.suggested_prompt = "What courses, certifications, or workshops would you recommend for someone in my generation to plan retirement successfully?"
        
        if st.button("💰 Financial Assessment", key="prompt4", help="Evaluate your current financial status"):
            st.session_state.suggested_prompt = "Please help me assess my current financial situation and retirement readiness."
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Resources section
        st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📋 Trusted Resources</div>', unsafe_allow_html=True)
        
        st.markdown("""
        **Knowledge Sources:**
        - [Segal Benefits](https://2025-benefits.segalco.com/)
        - [PSCA News](https://www.psca.org/news/psca-news/)
        
        **Platform Features:**
        - ✅ Personalized retirement planning advice
        - ✅ Goal identification and planning
        - ✅ Skills gap analysis
        - ✅ Learning opportunity recommendations
        - ✅ Step-by-step action plans
        - ✅ Professional document generation
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Clear conversation button
        if st.button("🗑️ Clear Conversation", key="clear", help="Start a new conversation"):
            st.session_state.conversation_history = []
            st.session_state.messages = []
            st.rerun()
    
    # Handle suggested prompts
    suggested_prompt = None
    if "suggested_prompt" in st.session_state:
        suggested_prompt = st.session_state.suggested_prompt
        del st.session_state.suggested_prompt
    
    # Chat input
    chat_prompt = st.chat_input("Ask me about retirement planning, financial goals, or career development...")
    
    # Use suggested prompt if available, otherwise use chat input
    prompt = suggested_prompt or chat_prompt
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your request..."):
                response = get_ai_response(prompt, st.session_state.conversation_history)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.conversation_history.append({"role": "user", "content": prompt})
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
        
        # Auto-scroll to bottom
        st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2025 RetireChat - AI Retirement Planning Coach. Delivering trusted financial guidance.</p>
        <p>Powered by advanced AI technology for personalized retirement planning solutions.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()