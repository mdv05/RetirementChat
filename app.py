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
    
    /* Form styling */
    .form-container {
        background: white;
        border: 1px solid #e1e8ed;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .form-section {
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .form-section:last-child {
        border-bottom: none;
        margin-bottom: 0;
    }
    
    .form-section h4 {
        color: #1f4e79;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Profile summary styling */
    .profile-summary {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 1px solid #dee2e6;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .profile-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #dee2e6;
    }
    
    .profile-item:last-child {
        border-bottom: none;
    }
    
    .profile-label {
        font-weight: 600;
        color: #1f4e79;
    }
    
    .profile-value {
        color: #495057;
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

def create_optimized_prompt(user_profile, user_input):
    """Create a focused, efficient prompt for better AI responses"""
    
    # Extract key profile elements
    age = user_profile.get('age', 30)
    income = user_profile.get('annual_income', 'mid-range')
    savings = user_profile.get('current_savings', 'starting out')
    risk = user_profile.get('risk_tolerance', 'moderate')
    
    prompt = f"""You are a retirement planning expert. User profile: {age}yr, {income} income, {savings} saved, {risk} risk tolerance.

User question: {user_input}

Provide specific, actionable retirement advice. Be direct and helpful. Include numbers when relevant.

Keep response under 300 words and focus on practical next steps."""
    
    return prompt

def get_ai_response(user_input, conversation_history, user_profile):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Use optimized, shorter prompt
        prompt = create_optimized_prompt(user_profile, user_input)
        
        # Only include last 2 messages for context (reduce token usage)
        if conversation_history:
            recent_context = conversation_history[-2:]
            context_str = "\n".join([f"{msg['role']}: {msg['content'][:100]}" for msg in recent_context])
            prompt += f"\n\nRecent context: {context_str}"
        
        # Optimized generation settings for speed
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=400,  # Shorter responses for speed
                temperature=0.3,  # Lower temperature for more focused responses
            ),
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"}
            ]
        )
        
        # Faster response validation
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            try:
                return response.text.strip() if response.text else get_smart_fallback(user_input, user_profile)
            except:
                return get_smart_fallback(user_input, user_profile)
        else:
            return get_smart_fallback(user_input, user_profile)
            
    except Exception as e:
        return get_smart_fallback(user_input, user_profile)

def get_smart_fallback(user_input, user_profile):
    """Quick, targeted fallback responses based on keywords"""
    input_lower = user_input.lower()
    age = user_profile.get('age', 30)
    income = user_profile.get('annual_income', 'Not specified')
    
    # Quick keyword-based responses
    if any(word in input_lower for word in ['roth', 'hsa', '401k', 'account']):
        return f"""**Account Priority for Age {age}:**
1. **401(k) match** - Free money first
2. **HSA** - Triple tax advantage (if available)
3. **Roth IRA** - Tax-free growth (good at age {age})
4. **More 401(k)** - Additional savings

**Quick decision:** If choosing between Roth IRA and HSA, pick HSA if you have a high-deductible health plan, otherwise Roth IRA.

Next step: Check if your employer offers HSA and 401(k) match."""
    
    if any(word in input_lower for word in ['save', 'much', 'percent']):
        return f"""**Savings Target for Age {age}:**
- **Minimum:** 10% of income to retirement accounts
- **Better:** 15% including employer match
- **Income:** {income}

**Action steps:**
1. Start with employer 401(k) match
2. Increase by 1% every year
3. Automate contributions

**Rule of thumb:** Try to have 1x your salary saved by age 30, 3x by 40."""
    
    if any(word in input_lower for word in ['invest', 'portfolio', 'stocks']):
        stock_percent = min(90, 100 - age)
        return f"""**Investment Mix for Age {age}:**
- **Stocks:** ~{stock_percent}%
- **Bonds:** ~{100-stock_percent}%

**Simple approach:** Use target-date funds in your 401(k) - they automatically adjust over time.

**DIY approach:** Low-cost index funds (total stock market + bond index)."""
    
    return f"""**Quick Retirement Guidance:**

**Your profile:** Age {age}, Income {income}

**Top priorities:**
1. Get full employer 401(k) match
2. Save 10-15% of income total
3. Use age-appropriate investments

**Need specifics?** Ask about:
- "How much should I save?"
- "Roth IRA or 401k?"
- "What investments for my age?"

What's your most pressing retirement question?"""

def show_streamlined_form():
    """Streamlined onboarding form with only essential questions"""
    st.markdown("""
    <div class="main-header">
        <h1>Welcome to RetireChat</h1>
        <p>Quick profile setup for personalized advice</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="form-container">
        <h3 style="color: #1f4e79; margin-top: 0;">Quick Retirement Profile</h3>
        <p>Just 6 key questions to get personalized advice:</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("quick_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Your Age", min_value=18, max_value=80, value=30)
            
            annual_income = st.selectbox("Annual Income", [
                "Under $50,000",
                "$50,000 - $75,000", 
                "$75,000 - $100,000",
                "$100,000 - $150,000",
                "Over $150,000"
            ])
            
            current_savings = st.selectbox("Current Retirement Savings", [
                "Just starting ($0-$10K)",
                "Getting started ($10K-$50K)",
                "Building up ($50K-$150K)",
                "Well established ($150K+)"
            ])
        
        with col2:
            target_retirement_age = st.number_input("Target Retirement Age", min_value=50, max_value=80, value=65)
            
            risk_tolerance = st.selectbox("Investment Risk Comfort", [
                "Conservative (safety first)",
                "Moderate (balanced approach)",
                "Aggressive (growth focused)"
            ])
            
            main_goal = st.selectbox("Top Retirement Priority", [
                "Start saving regularly",
                "Increase current savings",
                "Optimize investments",
                "Catch up on savings",
                "Plan for early retirement"
            ])
        
        submitted = st.form_submit_button("Get Personalized Advice", use_container_width=True)
        
        if submitted:
            # Store simplified profile
            st.session_state.user_profile = {
                'age': age,
                'annual_income': annual_income,
                'current_savings': current_savings,
                'target_retirement_age': target_retirement_age,
                'risk_tolerance': risk_tolerance,
                'main_goal': main_goal
            }
            st.session_state.profile_complete = True
            st.success("✅ Profile ready! Ask me anything about retirement planning.")
            st.rerun()

def show_quick_profile_summary(user_profile):
    """Compact profile display"""
    st.markdown(f"""
    <div class="profile-summary">
        <h4 style="color: #1f4e79; margin-top: 0;">📋 Your Profile</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
            <div><strong>Age:</strong> {user_profile.get('age', 'N/A')}</div>
            <div><strong>Target Retirement:</strong> {user_profile.get('target_retirement_age', 'N/A')}</div>
            <div><strong>Income:</strong> {user_profile.get('annual_income', 'N/A')}</div>
            <div><strong>Savings:</strong> {user_profile.get('current_savings', 'N/A')}</div>
            <div><strong>Risk:</strong> {user_profile.get('risk_tolerance', 'N/A')}</div>
            <div><strong>Goal:</strong> {user_profile.get('main_goal', 'N/A')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Initialize session state
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "profile_complete" not in st.session_state:
        st.session_state.profile_complete = False
    
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {}
    
    # Show streamlined onboarding if needed
    if not st.session_state.profile_complete:
        show_streamlined_form()
        return
    
    # Navigation Bar
    st.markdown("""
    <div class="nav-container">
        <div class="nav-logo">💰 RetireChat</div>
        <div class="nav-links">
            <a href="#" class="nav-link">Dashboard</a>
            <a href="#" class="nav-link">Tools</a>
            <a href="#" class="nav-link">Resources</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>AI Retirement Coach</h1>
        <p>Fast, personalized retirement planning advice</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat Interface
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 Ask Your Retirement Questions</h3>
            <p>Get specific advice based on your profile</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Chat messages (limit display to last 6 for performance)
        recent_messages = st.session_state.messages[-6:] if len(st.session_state.messages) > 6 else st.session_state.messages
        for message in recent_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        prompt = st.chat_input("Ask about retirement savings, investments, accounts...")
        
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Getting advice..."):
                    response = get_ai_response(prompt, st.session_state.conversation_history, st.session_state.user_profile)
                    st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            # Keep conversation history smaller for performance
            st.session_state.conversation_history.append({"role": "user", "content": prompt})
            st.session_state.conversation_history.append({"role": "assistant", "content": response})
            
            # Limit history to last 10 messages for performance
            if len(st.session_state.conversation_history) > 10:
                st.session_state.conversation_history = st.session_state.conversation_history[-10:]
    
    with col2:
        # Quick profile summary
        show_quick_profile_summary(st.session_state.user_profile)
        
        # Update Profile Button
        if st.button("✏️ Update Profile", use_container_width=True):
            st.session_state.profile_complete = False
            st.rerun()
        
        # Quick Actions - more specific
        st.markdown("### Quick Questions")
        
        if st.button("💰 How much should I save?", use_container_width=True):
            st.session_state.suggested_prompt = "How much should I be saving for retirement given my age and income?"
        
        if st.button("🏦 Which account should I use?", use_container_width=True):
            st.session_state.suggested_prompt = "Should I prioritize 401k, Roth IRA, or HSA for my situation?"
        
        if st.button("📊 What investments for my age?", use_container_width=True):
            st.session_state.suggested_prompt = "What's the right investment mix for someone my age?"
        
        if st.button("🚀 How to catch up?", use_container_width=True):
            st.session_state.suggested_prompt = "I'm behind on retirement savings. What's the best strategy to catch up?"
        
        # Progress stats
        messages_count = len([msg for msg in st.session_state.messages if msg["role"] == "user"])
        st.markdown(f"""
        <div class="feature-card">
            <h3>📊 Your Progress</h3>
            <div class="stat-card">
                <p class="stat-number">{messages_count}</p>
                <p class="stat-label">Questions Asked</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Clear conversation
        if st.button("🗑️ Clear Chat", use_container_width=True):
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
            with st.spinner("Getting advice..."):
                response = get_ai_response(prompt, st.session_state.conversation_history, st.session_state.user_profile)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.conversation_history.append({"role": "user", "content": prompt})
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
        st.rerun()
    
    # Simplified footer
    st.markdown("""
    <div class="footer">
        <h4>💰 RetireChat</h4>
        <p>Fast, personalized retirement planning advice powered by AI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()