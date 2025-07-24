# 🔮 Customer Churn Prediction System

[![Live Demo](https://img.shields.io/badge/Live%20Demo-View%20Dashboard-blue?style=for-the-badge&logo=streamlit)](https://customer-churn-dashboard-hyj1.onrender.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/VarenyaVisen/customer-churn-prediction-ml)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-orange?style=for-the-badge)](https://scikit-learn.org)

## 📋 Project Overview

A comprehensive machine learning system that predicts customer churn for telecom companies, enabling proactive customer retention strategies. This end-to-end solution includes data preprocessing, model development, evaluation, and deployment with an interactive web dashboard.

### 🎯 Business Problem
Customer acquisition costs are 5-25x higher than retention costs, yet many telecom companies lose 15-25% of customers annually. This system identifies at-risk customers before they churn, enabling targeted retention campaigns.

### 💰 Business Impact
- **Model Performance**: 84% ROC AUC score with Logistic Regression
- **Expected ROI**: $180,000+ annual net benefit through optimized retention campaigns
- **Customer Coverage**: Identifies 69% of actual churners with 57% precision
- **Deployment Ready**: Production-optimized threshold and business recommendations

## 🚀 Live Demo

**[👉 Try the Interactive Dashboard](https://customer-churn-dashboard-hyj1.onrender.com/)**

Upload customer data or use sample data to see real-time churn predictions with business insights.

## 🏗️ Project Architecture

```
├── 📊 Data Pipeline
│   ├── Exploratory Data Analysis
│   ├── Feature Engineering (5 new business features)
│   └── Comprehensive Preprocessing
├── 🤖 Machine Learning
│   ├── 4 Algorithm Comparison (Logistic, RF, XGBoost, LightGBM)
│   ├── Class Imbalance Handling (SMOTE)
│   └── Business Threshold Optimization
├── 📈 Model Evaluation
│   ├── Comprehensive Performance Analysis
│   ├── Feature Importance Insights
│   └── Business Impact Assessment
└── 🚀 Deployment
    ├── Interactive Streamlit Dashboard
    ├── RESTful API (Flask)
    └── Production-Ready Documentation
```

## 📊 Key Results

| Metric | Score | Business Interpretation |
|--------|--------|------------------------|
| **ROC AUC** | 0.840 | Excellent separation of churners vs non-churners |
| **Precision** | 0.574 | 57% of predicted churners are actual churners |
| **Recall** | 0.687 | Catches 69% of actual churners |
| **F1-Score** | 0.625 | Strong balanced performance |
| **Optimal Threshold** | 0.35 | Maximizes business value over default 0.5 |

## 🔍 Feature Engineering Highlights

Created 5 business-meaningful features that improved model performance:

- **Customer Lifetime Value**: Monthly charges × tenure
- **Services Count**: Total add-on services subscribed
- **Average Monthly Spend**: Spending behavior analysis
- **Price Per Service**: Value perception metric
- **Tenure Groups**: Business-relevant customer segments

## 🛠️ Tech Stack

**Core ML Stack:**
- **Python 3.8+** - Primary programming language
- **Pandas & NumPy** - Data manipulation and analysis
- **Scikit-learn** - Machine learning algorithms and preprocessing
- **XGBoost & LightGBM** - Advanced gradient boosting models

**Deployment & Visualization:**
- **Streamlit** - Interactive web dashboard
- **Flask** - RESTful API development
- **Plotly & Matplotlib** - Data visualization
- **Render** - Cloud deployment platform

**Development Tools:**
- **Jupyter Notebooks** - Development and analysis
- **Git & GitHub** - Version control
- **YAML** - Configuration management

## 📁 Project Structure

```
customer-churn-prediction-ml/
├── 📊 data/
│   ├── raw/                    # Original dataset
│   └── processed/              # Cleaned, ML-ready data
├── 📓 notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_model_development.ipynb
│   └── 04_model_evaluation.ipynb
├── 🤖 models/
│   └── best_model_logistic_regression.joblib
├── 📈 reports/
│   ├── model_comparison.csv
│   ├── feature_importance.csv
│   └── final_evaluation_summary.csv
├── 🚀 deployment/
│   ├── api/                    # Flask REST API
│   └── dashboard/              # Streamlit dashboard
└── 📝 Documentation
```

## 🚀 Quick Start

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/VarenyaVisen/customer-churn-prediction-ml.git
cd customer-churn-prediction-ml
```

2. **Create virtual environment**
```bash
python -m venv churn-env
source churn-env/bin/activate  # On Windows: churn-env\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Jupyter notebooks**
```bash
jupyter notebook notebooks/
```

5. **Launch dashboard locally**
```bash
streamlit run deployment/dashboard/streamlit_app.py
```

### API Usage

**Predict single customer:**
```python
import requests

customer_data = {
    "tenure": 12,
    "MonthlyCharges": 85.5,
    "TotalCharges": 1000.0,
    # ... other features
}

response = requests.post("http://localhost:5000/predict", json=customer_data)
prediction = response.json()
print(f"Churn Probability: {prediction['churn_probability']}")
```

## 📊 Model Performance Deep Dive

### Algorithm Comparison
| Model | ROC AUC | CV Score | Training Time | Interpretability |
|-------|---------|----------|---------------|------------------|
| **Logistic Regression** ⭐ | 0.840 | 0.831 ± 0.012 | Fast | High |
| Random Forest | 0.835 | 0.825 ± 0.015 | Medium | Medium |
| XGBoost | 0.832 | 0.823 ± 0.018 | Slow | Low |
| LightGBM | 0.829 | 0.820 ± 0.016 | Fast | Low |

### Feature Importance (Top 5)
1. **Contract_encoded** - Contract type (month-to-month highest risk)
2. **tenure** - Customer relationship length
3. **TotalCharges** - Historical spending
4. **MonthlyCharges** - Current monthly payment
5. **Customer_Lifetime_Value** - Engineered business metric

## 💼 Business Insights

### Key Churn Drivers
- **Contract Type**: Month-to-month customers 3x more likely to churn
- **Customer Age**: New customers (0-12 months) represent 67% of churn risk
- **Service Adoption**: Customers with fewer services show higher churn rates
- **Payment Method**: Electronic check users show elevated churn risk

### Retention Recommendations
1. **Target month-to-month contract customers** with annual contract incentives
2. **Implement new customer onboarding** programs for first 12 months
3. **Cross-sell additional services** to increase switching costs
4. **Optimize payment experience** for electronic check users

## 🎯 Future Enhancements

- [ ] Real-time model retraining pipeline
- [ ] A/B testing framework for retention campaigns
- [ ] Advanced feature engineering with temporal patterns
- [ ] Multi-model ensemble for improved performance
- [ ] Customer segmentation analysis
- [ ] Automated model monitoring and drift detection

## 🤝 Contributing

This project is part of my data science portfolio. Feedback and suggestions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📄 License

This project is for educational and portfolio purposes.

## 👤 Author

**Varenya Visen**
- 🌐 **Live Demo**: [Churn Prediction Dashboard](https://customer-churn-dashboard-hyj1.onrender.com/)
- 💼 **GitHub**: [@VarenyaVisen](https://github.com/VarenyaVisen)
- 📧 **Email**: [varenyavisen@gmail.com]
- 💼 **LinkedIn**: [Varenya Visen](https://www.linkedin.com/in/varenya-visen-a2680b265/)

---

⭐ **Star this repository if you found it helpful!**

*Built with ❤️ for solving real business problems through machine learning*
