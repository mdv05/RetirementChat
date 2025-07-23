import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="RetireChat - AI Retirement Planning Coach",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling similar to RetireHub
st.markdown("""
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1f4e79 0%, #2980b9 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        color: white !important;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
        color: white !important;
    }
    
    /* Card styling */
    .feature-card {
        background: white;
        border: 1px solid #e1e8ed;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    
    .feature-card h3 {
        color: #1f4e79;
        margin-top: 0;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1f4e79 0%, #2980b9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(31, 78, 121, 0.3);
    }
    
    /* Chat styling */
    .chat-container {
        background: white;
        border-radius: 12px;
        border: 1px solid #e1e8ed;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Stats styling */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Footer styling */
    .footer {
        background-color: #f8f9fa;
        padding: 2rem;
        margin-top: 3rem;
        border-radius: 10px;
        border-top: 3px solid #1f4e79;
        text-align: center;
    }
    
    /* Navigation styling */
    .nav-container {
        background: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        border: 1px solid #e1e8ed;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .nav-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f4e79;
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
    }
    
    .nav-link {
        color: #1f4e79;
        text-decoration: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        transition: background-color 0.2s ease;
    }
    
    .nav-link:hover {
        background-color: #f8f9fa;
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
    # Navigation Bar
    st.markdown("""
    <div class="nav-container">
        <div class="nav-logo">💰 RetireChat</div>
        <div class="nav-links">
            <a href="#" class="nav-link">Dashboard</a>
            <a href="#" class="nav-link">Planning Tools</a>
            <a href="#" class="nav-link">Resources</a>
            <a href="#" class="nav-link">Support</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>AI Retirement Planning Coach</h1>
        <p>Delivering trusted advice that improves lives through personalized retirement planning</p>
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
        # Chat Interface
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI Retirement Planning Assistant</h3>
            <p>Get personalized answers to your retirement planning questions, powered by expert financial guidance</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        prompt = st.chat_input("Ask me about retirement planning, financial goals, or career development...")
        
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing your question..."):
                    response = get_ai_response(prompt, st.session_state.conversation_history)
                    st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.conversation_history.append({"role": "user", "content": prompt})
            st.session_state.conversation_history.append({"role": "assistant", "content": response})
    
    with col2:
        # Sidebar Features
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Planning Tools</h3>
            <p>Access comprehensive financial calculators and projection tools</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("### Quick Start Guides")
        
        if st.button("🎯 Create Retirement Plan", use_container_width=True):
            st.session_state.suggested_prompt = "Help me create a detailed retirement development plan based on my current financial situation and future goals."
        
        if st.button("📈 Skills Gap Analysis", use_container_width=True):
            st.session_state.suggested_prompt = "Analyze my current skills and identify any gaps that I need to fill to advance in my career."
        
        if st.button("📚 Learning Resources", use_container_width=True):
            st.session_state.suggested_prompt = "What courses, certifications, or workshops would you recommend for someone in my generation to plan retirement successfully?"
        
        if st.button("💡 Financial Education", use_container_width=True):
            st.session_state.suggested_prompt = "Explain the basics of retirement planning and what I should know to get started."
        
        # Stats
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Your Progress</h3>
            <div class="stat-card">
                <p class="stat-number">{}</p>
                <p class="stat-label">Questions Asked</p>
            </div>
        </div>
        """.format(len([msg for msg in st.session_state.messages if msg["role"] == "user"])), unsafe_allow_html=True)
        
        # Resources
        st.markdown("""
        <div class="feature-card">
            <h3>🔗 Trusted Resources</h3>
            <p><a href="https://2025-benefits.segalco.com/" target="_blank" style="color: #1f4e79;">Segal Benefits Portal</a></p>
            <p><a href="https://www.psca.org/news/psca-news/" target="_blank" style="color: #1f4e79;">PSCA Financial News</a></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.conversation_history = []
            st.session_state.messages = []
            st.rerun()
    
    # Handle suggested prompts
    if "suggested_prompt" in st.session_state:
        prompt = st.session_state.suggested_prompt
        del st.session_state.suggested_prompt
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your question..."):
                response = get_ai_response(prompt, st.session_state.conversation_history)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.conversation_history.append({"role": "user", "content": prompt})
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
        st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <h4>💰 RetireChat</h4>
        <p>Delivering trusted retirement planning advice powered by AI technology.</p>
        <p style="font-size: 0.9rem; opacity: 0.7;">
            © 2025 RetireChat. All rights reserved. | 
            <a href="#" style="color: #1f4e79;">Privacy Policy</a> | 
            <a href="#" style="color: #1f4e79;">Terms of Service</a> | 
            <a href="#" style="color: #1f4e79;">Contact Support</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()