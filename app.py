import streamlit as st
import re
from config import model
from finance_analysis import analyze_finances
from ai_advisor import generate_financial_advice, generate_goal_plan, finance_chatbot_response
from visualization import plot_advised_financial_overview
from utils import split_advice_sections, split_goal_sections

# Page configuration
st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="📠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS from file
def load_css():
    with open('styles.css', 'r') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

load_css()

# Initialize Session State
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None
if "generated_advice" not in st.session_state:
    st.session_state.generated_advice = None
if "goal_plan" not in st.session_state:
    st.session_state.goal_plan = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

# HEADER SECTION 
st.markdown('<div class="main-header"> 🌐 AI Financial Advisor</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Your Personal AI-Powered Financial Planning Assistant</div>', unsafe_allow_html=True)

st.markdown("""
<div class='hero-section' style='text-align: center;'>
    <h2 style='color: white; font-size: 2.5rem; margin-bottom: 1rem;'>Take Control of Your Financial Future</h2>
    <p style='font-size: 1.2rem; color: #f0f0f0; margin-bottom: 0.5rem;'>
    Get personalized financial advice, investment strategies, and goal planning powered by AI
    </p>
</div>
""", unsafe_allow_html=True)

# Features Grid
st.markdown("### 📠 What You Can Do")
feature_col1, feature_col2, feature_col3, feature_col4 = st.columns(4)

with feature_col1:
    st.markdown("""
    <div class='feature-card'>
        <h4>📊 Financial Health</h4>
        <p>Track income, expenses, savings, and debts with interactive visualizations</p>
    </div>
    """, unsafe_allow_html=True)

with feature_col2:
    st.markdown("""
    <div class='feature-card'>
        <h4>📝 Personalized Advice</h4>
        <p>Get actionable recommendations tailored to your financial profile</p>
    </div>
    """, unsafe_allow_html=True)

with feature_col3:
    st.markdown("""
    <div class='feature-card'>
        <h4>🎯 Goal Planning</h4>
        <p>Create detailed plans for your short-term and long-term financial goals</p>
    </div>
    """, unsafe_allow_html=True)

with feature_col4:
    st.markdown("""
    <div class='feature-card'>
        <h4>💬 AI Chat Support</h4>
        <p>Get instant answers to your financial questions anytime with using AI</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# SIDEBAR INPUTS
with st.sidebar:
    st.markdown(" ")
    profile = st.selectbox(
        "Select Profile Type:", 
        ["Professional", "Student", "Retiree"],
        help="Choose the profile that best matches your current financial situation"
    )

    if profile == "Student":
        income = st.number_input(
            "Monthly Pocket Money (₹):", 
            step=10000, 
            min_value=0,
            help="Total monthly pocket money received from family"
        )
        part_time = st.selectbox(
            "Do you have part-time income?", 
            ["No", "Yes"],
            help="Select if you have additional income from part-time work"
        )
        if part_time == "Yes":
            extra_income = st.number_input(
                "Monthly Part-Time Income (₹):", 
                step=5000, 
                min_value=0,
                help="Additional income from part-time jobs or freelancing"
            )
            income += extra_income
    elif profile == "Professional":
        income = st.number_input(
            "Monthly Salary (₹):", 
            step=10000, 
            min_value=0,
            help="Your take-home salary after all deductions"
        )
    else:
        income = st.number_input(
            "Monthly Pension / Passive Income (₹):", 
            step=10000, 
            min_value=0,
            help="Monthly pension, rental income, or other passive income sources"
        )

    expenses = st.number_input(
        "Monthly Expenses (₹):", 
        step=5000, 
        min_value=0,
        help="Total monthly spending including rent, food, utilities, transportation, etc."
    )
    
    existing_savings = st.number_input(
        "Existing Savings & Investments (₹):", 
        step=10000, 
        min_value=0,
        help="Total amount currently saved in bank accounts, investments, FDs, mutual funds, etc."
    )
    
    debts = st.number_input(
        "Total Debts (₹):", 
        step=5000, 
        min_value=0,
        help="Total outstanding loans including education loan, personal loan, credit card debt, etc."
    )
    
    goals_input = st.text_area(
        "Financial Goals (comma-separated)", 
        placeholder="e.g., Buy a house, Retirement, Emergency Fund, Marriage",
        height=80,
        help="List your financial goals separated by commas. Be specific about what you want to achieve."
    )
    goals = [goal.strip() for goal in goals_input.split(",") if goal.strip()]
    
    risk_tolerance = st.selectbox(
        "Risk Tolerance:", 
        ["Low", "Medium", "High"],
        help="Low: Prefer safe investments | Medium: Balanced approach | High: Willing to take risks for higher returns"
    )

    st.session_state.user_data = {
        "profile": profile,
        "income": income,
        "expenses": expenses,
        "debts": debts,
        "existing_savings": existing_savings,
        "goals": goals,
        "risk_tolerance": risk_tolerance
    }

    generate_btn = st.button("Financial Analysis & Advice")


# MAIN CONTENT AREA
if st.session_state.user_data and st.session_state.user_data['income'] > 0:

    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; 
                border-radius: 15px; 
                text-align: center; 
                margin-bottom: 2rem;
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);'>
        <h1 style='font-size: 2rem; font-weight: 700; color: white; margin-bottom: 0.3rem;'>
        🔢 Your Financial Summary
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    if generate_btn:
        st.session_state.analysis_data = analyze_finances(st.session_state.user_data)
        st.session_state.generated_advice = generate_financial_advice(
            st.session_state.user_data,
            st.session_state.analysis_data
        )
    
    if st.session_state.analysis_data:
        ad = st.session_state.analysis_data
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <h3>₹{st.session_state.user_data['income']:,.0f}</h3>
                <p>Monthly Income</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <h3>₹{ad['savings']:,.0f}</h3>
                <p>Monthly Savings</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <h3>{ad['savings_ratio']*100:.1f}%</h3>
                <p>Savings Ratio</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class='metric-card'>
                <h3>₹{ad['investment_capacity']:,.0f}</h3>
                <p>Investment Capacity</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(" ")
        st.markdown(" ")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <h3>₹{ad['total_net_worth']:,.0f}</h3>
                <p>Total Net Worth</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <h3>₹{st.session_state.user_data['existing_savings']:,.0f}</h3>
                <p>Existing Savings</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <h3>₹{ad['emergency_fund']:,.0f}</h3>
                <p>Emergency Fund Target</p>
            </div>
            """, unsafe_allow_html=True)

        # Progress Indicators
        st.markdown(" ")
        st.markdown(" ")
        st.markdown("#### Financial Health Indicators")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Savings Rate**")
            savings_progress = min(ad['savings_ratio'] * 100 / 50, 1.0)
            st.markdown(f"""
            <div class='progress-bar'>
                <div class='progress-fill' style='width: {savings_progress*100}%'></div>
            </div>
            <small>{ad['savings_ratio']*100:.1f}% (Target: 20-50%)</small>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("**Debt-to-Income Ratio**")
            debt_progress = min(ad['debt_to_income_ratio'] * 100 / 40, 1.0)
            st.markdown(f"""
            <div class='progress-bar'>
                <div class='progress-fill' style='width: {debt_progress*100}%; background: {'#ff6b6b' if ad['debt_to_income_ratio'] > 0.4 else '#667eea'}'></div>
            </div>
            <small>{ad['debt_to_income_ratio']*100:.1f}% (Safe: <40%)</small>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        # Financial Advice Section
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; 
                    border-radius: 15px; 
                    text-align: center; 
                    margin-bottom: 2rem;
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);'>
            <h1 style='font-size: 2rem; font-weight: 700; color: white; margin-bottom: 0.3rem;'>
            💡 Your Personalized Financial Plan
            </h1>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.generated_advice:
            sections = split_advice_sections(st.session_state.generated_advice)
            
            col1, col2 = st.columns(2)
            
            for i, (title, content_html) in enumerate(sections):
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"""
                        <div class='card'>
                            {f"<h4 style='color: #667eea; margin-bottom: 10px;'>{title}</h4>" if title else ""}
                            {content_html}
                        </div>
                    """, unsafe_allow_html=True)

        # Visualizations
        st.markdown(" ")
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; 
                    border-radius: 15px; 
                    text-align: center; 
                    margin-bottom: 2rem;
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);'>
            <h1 style='font-size: 2rem; font-weight: 700; color: white; margin-bottom: 0.3rem;'>
            💹 Financial Overview Visualizations
            </h1>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(" ")
        fig2 = plot_advised_financial_overview(st.session_state.user_data, ad)
        st.pyplot(fig2)
            
        # Advanced Planning Input
        st.markdown("---")
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; 
                    border-radius: 15px; 
                    text-align: center; 
                    margin-bottom: 2rem;
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);'>
            <h1 style='font-size: 2rem; font-weight: 700; color: white; margin-bottom: 0.3rem;'>
            🧩 Advanced Planning
            </h1>
        </div>
        """, unsafe_allow_html=True)

        user_instructions = st.text_area(
            "Your Specific Instructions:", 
            placeholder="e.g., I want to save 30% of income directly, Pay debt as fast as possible, Reach goal in 2 years, Invest only in stocks, etc.",
            height=80,
            help="Enter your specific financial instructions that will be prioritized above all else"
        )
        
        advanced_plan_btn = st.button("🎲 Generate Advanced Goal Plan", use_container_width=True)
        
        if advanced_plan_btn:
            if not user_instructions.strip():
                st.warning("Please enter your specific instructions for advanced planning")
            else:
                with st.spinner("Creating advanced plan with your specific instructions..."):
                    st.session_state.goal_plan = generate_goal_plan(
                        st.session_state.user_data,
                        st.session_state.analysis_data,
                        user_instructions
                    )
        
        if st.session_state.goal_plan:

            st.markdown("---")
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; 
                        border-radius: 15px; 
                        text-align: center; 
                        margin-bottom: 2rem;
                        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);'>
                <h1 style='font-size: 2rem; font-weight: 700; color: white; margin-bottom: 0.3rem;'>
                🎯 Goal-Oriented Planning
                </h1>
            </div>
            """, unsafe_allow_html=True)

            sections = split_goal_sections(st.session_state.goal_plan)
            
            col1, col2 = st.columns(2)
            
            for i, (title, content_html) in enumerate(sections):
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"""
                        <div class='goal-card'>
                            {f"<h4 style='color: #667eea; margin-bottom: 10px;'>{title}</h4>" if title else ""}
                            {content_html}
                        </div>
                    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <div style='text-align: center; padding: 4rem 2rem; background: #f8f9fa; border-radius: 15px;'>
        <h3 style='color: #667eea; margin-bottom: 1rem;'>Welcome to Your AI Financial Advisor! 👋</h3>
        <p style='font-size: 1.1rem; color: #666; margin-bottom: 2rem;'>
            To get started, please enter your financial details in the sidebar and click 
            <strong>"Generate Financial Analysis & Advice"</strong> to receive your personalized financial plan.
        </p>
        <div style='font-size: 2rem; margin-bottom: 1rem;'>⬅️</div>
        <p>Fill out the form in the sidebar to begin</p>
    </div>
    """, unsafe_allow_html=True)

# CHATBOT SECTION 
st.markdown("---")
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 1.5rem; 
            border-radius: 15px; 
            text-align: center; 
            margin-bottom: 2rem;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);'>
    <h1 style='font-size: 2rem; font-weight: 700; color: white; margin-bottom: 0.3rem;'>
    💬 Financial Assistant Chat
    </h1>
    <p style='font-size: 1rem; color: rgba(255,255,255,0.9); margin-bottom: 0;'>
    Your AI Financial Expert
    </p>
</div>
""", unsafe_allow_html=True)

chat_col1, chat_col2 = st.columns([2, 1])

with chat_col1:

    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg['user']:
                st.markdown(f'<div class="user-message">{msg["user"]}</div>', unsafe_allow_html=True)
            if msg['bot']:
                st.markdown(f'<div class="bot-message">{msg["bot"]}</div>', unsafe_allow_html=True)

    # Chat Input
    st.session_state.user_query = st.text_area(
        "Ask your financial question:",
        value=st.session_state.user_query,
        placeholder="e.g., How much should I invest monthly for retirement? What's the best way to pay off my debt?",
        height=80,
        key="chat_input",
        help="Enter your financial question here, and the AI will provide personalized advice based on your profile and goals. e.g., 'What's the best way to pay off my debt?', 'How much should I invest monthly for retirement?', etc."
    )

    ask_col1, ask_col2, ask_col3 = st.columns([1, 2, 1])
    with ask_col2:
        ask_btn = st.button("📨 Send Message", use_container_width=True)

    if ask_btn:
        if not st.session_state.user_query.strip():
            st.warning("Please enter a question before sending.")
        elif not st.session_state.user_data or st.session_state.user_data.get("income", 0) == 0:
            st.error("Please enter your financial details in the sidebar before using the chatbot.")
        elif not st.session_state.analysis_data:
            st.error("Please generate your financial analysis first.")
        else:
            with st.spinner("Analyzing your question..."):
                try:
                    response = finance_chatbot_response(
                        st.session_state.user_data,
                        st.session_state.analysis_data,
                        st.session_state.user_query
                    )
                    st.session_state.chat_history.append({
                        "user": st.session_state.user_query,
                        "bot": response
                    })
                    st.session_state.user_query = ""
                    st.rerun()
                except Exception as e:
                    st.error(f"Chatbot Error: {e}")

with chat_col2:
    st.markdown("""
    <div class='card'>
        <h4>💡 Chat Tips</h4>
        <ul style='font-size: 0.9rem;'>
            <li>Ask about investments</li>
            <li>Get budgeting advice</li>
            <li>Discuss debt management</li>
            <li>Plan for specific goals</li>
            <li>Understand financial terms</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem 0;'>
    <h3>About This Project</h3>
    <p>An intelligent AI-powered financial advisor designed to help you make smarter financial decisions, 
    plan for your goals, and achieve financial wellness.</p>
</div>
""", unsafe_allow_html=True)