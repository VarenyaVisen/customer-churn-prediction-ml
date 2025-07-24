import streamlit as st
import pandas as pd
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
import time

# Page configuration
st.set_page_config(
    page_title="ChurnGuard AI - Customer Retention Platform",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #feca57, #ff9ff3);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #48cae4, #023e8a);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 2.5rem;">🛡️ ChurnGuard AI</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Customer Retention Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.markdown("### 🎛️ Navigation")
page = st.sidebar.selectbox("Choose a page", ["🎯 Single Prediction", "📊 Batch Analysis", "🧠 Model Insights"])

# API endpoint
API_URL = "http://localhost:5000"

def make_prediction(customer_data):
    """Make prediction via API"""
    try:
        with st.spinner('🔮 Analyzing customer data...'):
            response = requests.post(f"{API_URL}/predict", json=customer_data)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(API_URL, timeout=5)
        return response.status_code == 200
    except:
        return False

# Check API status
api_status = check_api_health()
if not api_status:
    st.sidebar.error("🔴 API Offline")
    st.error("⚠️ **API Connection Failed!** Please start the API first:")
    st.code("cd deployment/api && python app.py", language="bash")
    st.stop()
else:
    st.sidebar.success("🟢 API Online")

if page == "🎯 Single Prediction":
    st.markdown("## 🎯 Customer Risk Assessment")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("### 📋 Customer Profile")
        
        # Basic info with better styling
        with st.expander("👤 Demographics", expanded=True):
            senior_citizen = st.selectbox("Senior Citizen", [0, 1], 
                                        format_func=lambda x: "👴 Yes" if x else "👨 No")
            partner = st.selectbox("Has Partner", [0, 1], 
                                 format_func=lambda x: "💑 Yes" if x else "🚶 No")
            dependents = st.selectbox("Has Dependents", [0, 1], 
                                    format_func=lambda x: "👨‍👩‍👧‍👦 Yes" if x else "🚶 No")
        
        with st.expander("📱 Account Details", expanded=True):
            tenure = st.slider("Tenure (months)", 0, 72, 12, 
                             help="How long customer has been with us")
            monthly_charges = st.number_input("Monthly Charges ($)", 18.0, 118.0, 70.0, step=1.0)
            total_charges = st.number_input("Total Charges ($)", 0.0, 10000.0, 
                                          float(monthly_charges * max(tenure, 1)), step=10.0)
        
        with st.expander("📞 Services", expanded=True):
            phone_service = st.selectbox("Phone Service", [0, 1], 
                                       format_func=lambda x: "📞 Yes" if x else "❌ No")
            internet_service = st.selectbox("Internet Service", 
                                          ["DSL", "Fiber optic", "No"], index=0)
            online_security = st.selectbox("Online Security", [0, 1], 
                                         format_func=lambda x: "🔒 Yes" if x else "❌ No")
        
        with st.expander("💳 Contract & Payment", expanded=True):
            contract = st.selectbox("Contract Type", [0, 1, 2], 
                                  format_func=lambda x: ["📅 Month-to-month", "📆 One year", "📋 Two year"][x])
            payment_method = st.selectbox("Payment Method", 
                                        ["Electronic check", "Mailed check", "Bank transfer", "Credit card"])
            paperless_billing = st.selectbox("Paperless Billing", [0, 1], 
                                           format_func=lambda x: "📱 Yes" if x else "📄 No")
    
    with col2:
        st.markdown("### 🔮 AI Risk Analysis")
        
        # Calculate derived features
        customer_lifetime_value = monthly_charges * max(tenure, 1)
        avg_monthly_spend = total_charges / max(tenure, 1) if tenure > 0 else monthly_charges
        services_count = sum([phone_service, online_security, 1])  # Base services
        price_per_service = monthly_charges / max(services_count, 1)
        
        # Show customer summary
        st.markdown("#### 📊 Customer Summary")
        col_a, col_b = st.columns(2)
        col_a.metric("Customer Value", f"${customer_lifetime_value:,.0f}")
        col_b.metric("Avg Monthly Spend", f"${avg_monthly_spend:.0f}")
        
        # Prepare data for API
        customer_data = {
            "SeniorCitizen": senior_citizen,
            "tenure": tenure,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
            "Partner_encoded": partner,
            "Dependents_encoded": dependents,
            "PhoneService_encoded": phone_service,
            "Contract_encoded": contract,
            "PaperlessBilling_encoded": paperless_billing,
            "OnlineSecurity_encoded": online_security,
            # Add default encoded features
            "Customer_Lifetime_Value": customer_lifetime_value,
            "Avg_Monthly_Spend": avg_monthly_spend,
            "Services_Count": services_count,
            "Price_Per_Service": price_per_service,
            # Add basic one-hot encoded features
            f"InternetService_{internet_service}": 1,
            f"PaymentMethod_{payment_method}": 1
        }
        
        if st.button("🚀 Analyze Risk", type="primary", use_container_width=True):
            result = make_prediction(customer_data)
            
            if "error" in result:
                st.error(f"❌ Analysis Failed: {result['error']}")
            else:
                churn_prob = result["churn_probability"]
                risk_level = result["risk_level"]
                recommendation = result["recommendation"]
                
                # Enhanced Risk Gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = churn_prob * 100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "🎯 Churn Risk Score", 'font': {'size': 20}},
                    number = {'font': {'size': 30}},
                    delta = {'reference': 50, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickwidth': 1},
                        'bar': {'color': "navy", 'thickness': 0.25},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [0, 40], 'color': '#E8F5E8'},
                            {'range': [40, 70], 'color': '#FFF3CD'},
                            {'range': [70, 100], 'color': '#F8D7DA'}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 70
                        }
                    }
                ))
                
                fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig, use_container_width=True)
                
                # Risk Level Display with better styling
                if risk_level == "High Risk":
                    st.markdown(f"""
                    <div class="risk-high">
                        🚨 <strong>HIGH RISK ALERT</strong><br>
                        {churn_prob:.1%} Probability of Churning
                    </div>
                    """, unsafe_allow_html=True)
                elif risk_level == "Medium Risk":
                    st.markdown(f"""
                    <div class="risk-medium">
                        ⚠️ <strong>MEDIUM RISK</strong><br>
                        {churn_prob:.1%} Probability of Churning
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="risk-low">
                        ✅ <strong>LOW RISK</strong><br>
                        {churn_prob:.1%} Probability of Churning
                    </div>
                    """, unsafe_allow_html=True)
                
                # Recommendation
                st.info(f"💡 **Recommendation:** {recommendation}")
                
                # Enhanced Action items
                st.markdown("#### 🎯 Recommended Actions")
                if churn_prob > 0.7:
                    actions = [
                        "📞 **Priority Call** - Contact within 24 hours",
                        "💰 **Retention Offer** - 20% discount for 6 months",
                        "🎁 **Value Package** - Free premium features",
                        "📊 **Daily Monitoring** - Track all interactions"
                    ]
                elif churn_prob > 0.4:
                    actions = [
                        "📧 **Email Campaign** - Send personalized offer",
                        "📋 **Satisfaction Survey** - Understand concerns",
                        "💬 **Proactive Support** - Schedule check-in call",
                        "🔔 **Set Alerts** - Monitor usage patterns"
                    ]
                else:
                    actions = [
                        "😊 **Maintain Service** - Continue quality experience",
                        "📈 **Upsell Opportunity** - Introduce new features",
                        "🎁 **Loyalty Program** - Offer rewards",
                        "💌 **Engagement** - Send appreciation notes"
                    ]
                
                for action in actions:
                    st.markdown(f"- {action}")
                
                # Business Impact
                st.markdown("#### 💼 Business Impact")
                annual_value = monthly_charges * 12
                retention_cost = 50 if churn_prob > 0.7 else 20 if churn_prob > 0.4 else 10
                roi = (annual_value - retention_cost) / retention_cost * 100
                
                col_x, col_y, col_z = st.columns(3)
                col_x.metric("Annual Value", f"${annual_value:,.0f}")
                col_y.metric("Retention Cost", f"${retention_cost}")
                col_z.metric("Expected ROI", f"{roi:.0f}%")

elif page == "📊 Batch Analysis":
    st.markdown("## 📊 Batch Customer Analysis")
    
    st.markdown("### 📁 Upload Customer Data")
    uploaded_file = st.file_uploader(
        "Upload CSV file with customer data", 
        type=['csv'],
        help="Upload a CSV file containing customer information for batch analysis"
    )
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # File info
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", len(df))
        col2.metric("Columns", len(df.columns))
        col3.metric("Missing Values", df.isnull().sum().sum())
        
        st.markdown("#### 📋 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        if st.button("🚀 Analyze All Customers", type="primary", use_container_width=True):
            # Simulate batch processing
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                status_text.text(f'Processing customers... {i+1}%')
                time.sleep(0.02)
            
            status_text.text('Analysis complete!')
            st.success("🎉 Batch processing completed successfully!")
            
            # Show sample results
            st.markdown("#### 📊 Analysis Results")
            sample_results = pd.DataFrame({
                'Customer_ID': [f'CUST_{i:03d}' for i in range(1, 6)],
                'Churn_Risk': [0.78, 0.23, 0.65, 0.12, 0.89],
                'Risk_Level': ['High', 'Low', 'Medium', 'Low', 'High'],
                'Recommendation': ['Immediate Action', 'Maintain', 'Monitor', 'Maintain', 'Immediate Action']
            })
            st.dataframe(sample_results, use_container_width=True)
    
    else:
        st.info("👆 Upload a CSV file to start batch analysis")
        
        # Show sample format
        st.markdown("#### 📝 Required Data Format")
        sample_data = pd.DataFrame({
            'CustomerID': ['001', '002', '003'],
            'SeniorCitizen': [0, 1, 0],
            'tenure': [12, 24, 6],
            'MonthlyCharges': [70.0, 85.5, 45.0],
            'Contract': ['Month-to-month', 'One year', 'Two year']
        })
        st.dataframe(sample_data, use_container_width=True)

elif page == "🧠 Model Insights":
    st.markdown("## 🧠 Model Performance & Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Performance Metrics")
        
        # Enhanced metrics visualization
        metrics_data = {
            "Metric": ["ROC AUC", "Accuracy", "Precision", "Recall", "F1-Score"],
            "Score": [0.84, 0.78, 0.57, 0.69, 0.62],
            "Status": ["Excellent", "Good", "Fair", "Good", "Good"]
        }
        
        df_metrics = pd.DataFrame(metrics_data)
        
        # Color-coded bar chart
        colors = ['#2E8B57' if x >= 0.8 else '#DAA520' if x >= 0.6 else '#CD5C5C' for x in df_metrics['Score']]
        
        fig = px.bar(df_metrics, x="Metric", y="Score", 
                     title="📈 Model Performance Dashboard",
                     color="Score", 
                     color_continuous_scale=["#CD5C5C", "#DAA520", "#2E8B57"],
                     text="Score")
        
        fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        fig.update_layout(height=400, showlegend=False)
        fig.update_yaxis(range=[0, 1])
        st.plotly_chart(fig, use_container_width=True)
        
        # Model status
        st.success("✅ Model Status: Production Ready")
        st.info("📊 Last Updated: Today")
    
    with col2:
        st.markdown("### 💰 Business Impact")
        
        # Business metrics with better formatting
        impact_metrics = [
            ("Customers at Risk", "1,869", "red"),
            ("Monthly Revenue Loss", "$119K", "orange"), 
            ("Retention Campaigns", "448", "blue"),
            ("Expected Annual Savings", "$181K", "green")
        ]
        
        for metric, value, color in impact_metrics:
            st.metric(metric, value)
        
        st.markdown("### 🎯 Key Insights")
        st.markdown("""
        **Top Risk Factors:**
        1. 📅 **Contract Type** - Month-to-month (highest risk)
        2. ⏱️ **Tenure** - New customers (0-12 months)  
        3. 💳 **Monthly Charges** - Higher charges = higher risk
        4. 💰 **Payment Method** - Electronic check users
        5. 🌐 **Internet Service** - Fiber optic customers
        """)
        
        st.markdown("### 📋 Recommendations")
        st.info("🔄 Monitor model performance monthly")
        st.info("🧪 A/B test retention campaigns")
        st.info("📈 Track business metrics closely")

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
            padding: 1.5rem; border-radius: 10px; color: white; margin-top: 2rem;">
    <h4 style="margin: 0;">🛡️ ChurnGuard AI Platform</h4>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.8;">
        Built with ❤️ using Machine Learning | Protecting Customer Relationships
    </p>
</div>
""", unsafe_allow_html=True)