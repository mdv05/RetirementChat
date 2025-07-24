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
    
    prompt = f"""You are a financial planning expert helping with retirement and general financial questions.

User profile: {age} years old, {income} income, {savings} saved, {risk} risk tolerance.

User question: "{user_input}"

Provide specific, actionable financial advice that directly answers their question. If it's about budgeting, give actual budget categories and amounts. If it's about debt, give specific strategies. Be practical and helpful.

Keep response under 400 words and focus on answering their specific question."""
    
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
    
    # Retirement planning questions
    if any(phrase in input_lower for phrase in ['retirement plan', 'long term plan', 'retirement strategy', 'plan for retirement', 'retirement roadmap', 'retirement steps']):
        target_age = user_profile.get('target_retirement_age', 65)
        years_to_retirement = target_age - age
        
        if age <= 25:
            monthly_target = "$200-400"
            milestone_30 = "1x annual salary"
            milestone_40 = "3x annual salary"
        elif age <= 35:
            monthly_target = "$400-800"
            milestone_30 = "1x annual salary"
            milestone_40 = "3x annual salary"
        else:
            monthly_target = "$800-1,500"
            milestone_30 = "1x annual salary (catch up needed)"
            milestone_40 = "3x annual salary"
        
        return f"""**Long-Term Retirement Plan for Age {age}**

**Your Timeline:** {years_to_retirement} years until retirement at {target_age}

**Phase 1: Foundation (Ages {age}-30)**
- **Goal:** Build retirement saving habit
- **Target:** Save {monthly_target}/month
- **Priority:** Get full employer 401(k) match
- **Milestone:** Have {milestone_30} saved by age 30
- **Accounts:** 401(k) for match, then Roth IRA

**Phase 2: Acceleration (Ages 30-40)**
- **Goal:** Increase savings rate to 15-20%
- **Target:** Max Roth IRA ($7,000/year), increase 401(k)
- **Milestone:** Have {milestone_40} saved by age 40
- **Focus:** Career growth to increase income

**Phase 3: Optimization (Ages 40-50)**
- **Goal:** Max retirement accounts
- **Target:** $22,500 to 401(k), $7,000 to Roth IRA
- **Milestone:** Have 6x annual salary saved
- **Strategy:** Consider additional investments

**Phase 4: Pre-Retirement (Ages 50-{target_age})**
- **Goal:** Catch-up contributions, reduce risk
- **Target:** Max savings with catch-up limits
- **Milestone:** 10x annual salary by retirement
- **Prep:** Plan withdrawal strategy

**Investment Strategy by Age:**
- **Ages {age}-30:** 90% stocks, 10% bonds (aggressive growth)
- **Ages 30-40:** 80% stocks, 20% bonds
- **Ages 40-50:** 70% stocks, 30% bonds
- **Ages 50+:** Gradually shift to 60% stocks, 40% bonds

**Action Steps This Year:**
1. Start contributing to employer 401(k) for match
2. Open Roth IRA if no employer plan
3. Automate monthly contributions
4. Invest in target-date funds or index funds

**Rule of Thumb:** Save 10-15% of income consistently, starting now. Time is your biggest advantage at age {age}!

What part of this plan would you like me to explain further?"""
    
    # Budget and expense questions
    if any(word in input_lower for word in ['budget', 'monthly', 'rent', 'expenses', 'spend', 'bills']):
        income_range = income.replace('Under ', '').replace('Over ', '').replace('$', '').replace(',', '')
        
        if 'under 50' in income.lower() or '50,000' in income:
            monthly_income = "$3,000-4,000"
            rent_max = "$1,200"
            food = "$400"
            transport = "$300"
            retirement = "$300"
        elif '50,000 - 75,000' in income:
            monthly_income = "$4,200-6,200"
            rent_max = "$1,500"
            food = "$500"
            transport = "$400"
            retirement = "$500"
        elif '75,000 - 100,000' in income:
            monthly_income = "$6,200-8,300"
            rent_max = "$2,000"
            food = "$600"
            transport = "$500"
            retirement = "$700"
        else:
            monthly_income = "$8,300+"
            rent_max = "$2,500+"
            food = "$700"
            transport = "$600"
            retirement = "$1,000+"
        
        return f"""**Monthly Budget Plan for Age {age}**

**Estimated Monthly Income:** {monthly_income}

**Essential Expenses (50-60%):**
- Rent/Housing: {rent_max} max (30% of income)
- Food: {food}
- Transportation: {transport}
- Utilities: $150-200
- Insurance: $200-300

**Student Loans & Debt (10-20%):**
- Student loan payments: Pay minimums first
- Extra payments: Focus on highest interest rates
- Target: Pay off before age 30 if possible

**Savings & Retirement (20%):**
- Emergency fund: $1,000 starter, then 3-6 months expenses
- Retirement (401k/IRA): {retirement}
- Get employer match first!

**Flexible Spending (10-20%):**
- Entertainment, shopping, hobbies

**Quick Tips:**
- Use 50/30/20 rule: needs/wants/savings
- Pay student loan minimums, then max employer 401k match
- Build $1,000 emergency fund before extra debt payments

Need help with specific numbers or categories?"""
    
    # Student loan and debt questions
    if any(word in input_lower for word in ['student loan', 'debt', 'loans', 'pay off', 'payment']):
        return f"""**Student Loan Strategy for Age {age}**

**Payment Priority Order:**
1. **Pay minimums** on all loans
2. **Get employer 401k match** (free money!)
3. **Pay extra** on highest interest rate loans first
4. **Build emergency fund** ($1,000 minimum)

**Specific Strategy:**
- **Federal loans:** Often 4-6% interest
- **Private loans:** Usually higher rates - pay these first
- **Income-driven plans:** Consider if payments are high

**Monthly Approach:**
- List all loans with balances and rates
- Pay minimums on all
- Put any extra toward highest rate loan
- Don't skip retirement savings completely

**Timeline Goal:**
- Aim to pay off by age 30
- Balance loan payments with retirement savings
- Don't sacrifice employer match for loans under 5% interest

**Quick Math:**
At age {age}, every $1,000 you put in retirement grows to ~$20,000 by retirement. Balance this with loan interest rates.

What are your loan interest rates? This affects the strategy."""
    
    # Savings and investment questions
    if any(word in input_lower for word in ['save', 'saving', 'much', 'percent', 'how much']):
        return f"""**Savings Target for Age {age}:**
- **Minimum:** 10% of income to retirement accounts
- **Better:** 15% including employer match
- **Income:** {income}

**Monthly Breakdown:**
- Emergency fund: $100-200/month until $1,000 saved
- Retirement: 10-15% of gross income
- If income is $40K: Save $333-500/month total

**Action steps:**
1. Start with employer 401(k) match
2. Build $1,000 emergency fund
3. Increase retirement by 1% every year
4. Automate all savings

**Milestones by Age:**
- Age 30: 1x annual salary saved
- Age 40: 3x annual salary saved
- Age 50: 6x annual salary saved

**Rule of thumb:** At age {age}, time is your biggest advantage. Even small amounts grow significantly over time."""
    
    # Account and investment allocation questions
    if any(word in input_lower for word in ['roth', 'hsa', '401k', 'account', 'invest', 'portfolio', 'stocks', 'allocation']):
        stock_percent = min(90, 100 - age)
        
        return f"""**Complete Investment Strategy for Age {age}:**

**Account Priority:**
1. **401(k) match** - Free money first
2. **HSA** - Triple tax advantage (if available)
3. **Roth IRA** - Tax-free growth (perfect at age {age})
4. **More 401(k)** - Additional tax-deferred savings

**Investment Allocation:**
- **Stocks:** ~{stock_percent}%
- **Bonds:** ~{100-stock_percent}%

**Simple Approach:**
- Use target-date funds (automatically adjusts over time)
- Choose target date around 2065 for your age

**DIY Approach:**
- 70% Total Stock Market Index
- 20% International Stock Index  
- 10% Bond Index

**Key Principles:**
- Start aggressive while young (more stocks)
- Keep fees low (under 0.5%)
- Don't try to time the market
- Automate everything

**Quick decision:** If choosing between Roth IRA and HSA, pick HSA if you have a high-deductible health plan, otherwise Roth IRA."""
    
    # Emergency fund questions
    if any(word in input_lower for word in ['emergency', 'fund', 'savings account']):
        return f"""**Emergency Fund for Age {age}:**

**Starter Goal:** $1,000 in savings account
**Full Goal:** 3-6 months of expenses

**Priority Order:**
1. Save $1,000 emergency fund first
2. Get employer 401(k) match
3. Pay off high-interest debt (>6%)
4. Build full emergency fund
5. More retirement savings

**Where to keep it:**
- High-yield savings account (3-5% interest)
- Keep it separate from checking
- Don't invest emergency funds

**Monthly target:** Save $100-200/month until you reach your goal."""
    
    # Career and income questions
    if any(word in input_lower for word in ['career', 'job', 'income', 'raise', 'promotion', 'salary']):
        return f"""**Career Growth Strategy for Age {age}:**

**Income Growth Plan:**
- Target 3-5% raises annually through performance
- Consider job changes every 2-3 years for larger increases
- Develop in-demand skills in your field
- Network within your industry

**Retirement Impact:**
- Every $10K income increase = $100-150/month more for retirement
- Career growth is often better than investment returns early on
- Focus on both earning more AND saving more

**Action Steps:**
1. Track your accomplishments for review time
2. Research market rates for your role
3. Invest in skills training or certifications
4. Update LinkedIn and resume regularly

**Smart Moves:**
- Increase 401(k) contribution with every raise
- Don't let lifestyle inflation eat all income growth
- Save at least 50% of any raise for retirement

At age {age}, investing in your career can have the biggest impact on retirement readiness."""
    
    # General financial planning questions
    if any(word in input_lower for word in ['financial plan', 'money plan', 'financial goals', 'financial advice']):
        return f"""**Complete Financial Plan for Age {age}:**

**Immediate Priorities (Next 6 months):**
1. Build $1,000 emergency fund
2. Get employer 401(k) match
3. Pay minimums on all debts
4. Track spending for one month

**Short-term Goals (1-2 years):**
1. Pay off high-interest debt (>6%)
2. Build 3-month emergency fund
3. Increase retirement savings to 10%
4. Consider Roth IRA

**Medium-term Goals (2-10 years):**
1. Increase retirement savings to 15%
2. Build 6-month emergency fund
3. Pay off student loans
4. Save for major purchases (house, etc.)

**Long-term Goals (10+ years):**
1. Max retirement accounts ($22,500 + $7,000)
2. Build wealth through investments
3. Plan for financial independence
4. Consider early retirement options

**Monthly Action Plan:**
- Automate retirement savings
- Review and optimize expenses
- Invest in career growth
- Monitor progress quarterly

**Key Principle:** Start now, even with small amounts. Consistency beats perfection at age {age}."""
    
    # Default response - but much more helpful
    return f"""**I can help with your question about: "{user_input}"**

**Your profile:** Age {age}, Income {income}

Based on your question, here's what I recommend:

**If this is about retirement planning:**
At age {age}, you have ~40 years until retirement. Even saving $200/month could grow to over $500,000. Start with employer 401(k) match, then Roth IRA.

**If this is about budgeting:**
With {income} income, aim for 50% needs, 30% wants, 20% savings. Priority: emergency fund, then retirement.

**If this is about debt:**
Pay minimums on everything, get employer match, then attack highest interest rate debt first.

**If this is about investing:**
At age {age}, go aggressive: 80-90% stocks through index funds or target-date funds.

**Want more specific advice?** Just ask:
- "Create a retirement plan for my age"
- "How should I budget my income?"
- "What's my investment strategy?"
- "How do I pay off debt faster?"

What aspect would you like me to dive deeper into?"""

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