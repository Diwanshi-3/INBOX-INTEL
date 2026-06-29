# 📧 INBOX-INTEL  
AI-Powered Gmail Spam Detection using Machine Learning and Python

---

## 🧠 Project Overview

This project, Inbox Intel: Spam Email Classifier, is an AI-powered system designed to automatically detect and classify emails as Spam or Ham (Legitimate Email) using Machine Learning and Natural Language Processing (NLP) techniques.

With the increasing number of unwanted and malicious emails such as phishing links, scams, and advertisements, manual filtering becomes inefficient and unreliable. To solve this problem, the system applies NLP-based text preprocessing and converts email content into numerical features using TF-IDF Vectorization.

A trained Multinomial Naive Bayes machine learning model is then used to classify emails with high accuracy. The system also integrates Google OAuth 2.0 authentication and the Gmail API to securely fetch real-time emails directly from the user’s inbox.

The predictions are displayed through an interactive Streamlit web application, making the system simple, fast, and user-friendly. This project demonstrates the practical use of Artificial Intelligence, Machine Learning, and Cloud APIs in improving email security and reducing spam-related threats.

---

## ⚙️ Tech Stack

- Python
- Scikit-learn
- Pandas
- NumPy
- NLP (TF-IDF Vectorizer)
- Streamlit (UI)
- Pickle (Model Saving)
- Google OAuth 2.0
- Gmail API

---

## 📂 Project Structure  


Spam_Email_Classifier/
├── app.py
├── model.pkl
├── vectorizer.pkl
├── requirements.txt
├── README.md
├── project.ipynb
├── dataset/
├── ml/
├── auth/
├── gmail/
├── ui/

---

## 🧪 How It Works  
- Email text is cleaned (NLP preprocessing)  
- Converted into numerical features using TF-IDF
- TF-IDF converts text into weighted feature vectors based on word importance 
- ML model predicts:  
  - Spam  
  - Not Spam  
- Result shown in Streamlit UI  

---

## 📊 Model Used  
- Multinomial Naive Bayes / Logistic Regression  

**Accuracy:** 96%

---

## ▶️ How to Run  

```bash
git clone https://github.com/Diwanshi-3/INBOX-INTEL.git
cd INBOX-INTEL
pip install -r requirements.txt
streamlit run app.py
```

## 📌 Features

- Spam detection in real-time
- NLP-based text processing
- TF-IDF based feature extraction
- Clean and interactive Streamlit UI
- Pre-trained Machine Learning model
- Secure Gmail integration using OAuth 2.0 and Gmail API

## 👩‍💻 Author

- Diwanshi  
- BTech CSE Student  
- Machine Learning Enthusiast 🚀  


## ⭐ Future Enhancements

- Deep Learning models (LSTM, BERT, Transformers)
- Better dataset expansion for higher accuracy
- Gmail API automation improvements
- Real-time continuous email monitoring
- Phishing and scam URL detection
- Email categorization (Promotions, Social, Updates, Spam)
- Cloud deployment (Streamlit, AWS, Azure, GCP)
- Mobile application development
- Explainable AI (show why email is marked spam)


## 📜 License
This project is developed for academic and learning purposes.
It is open-source and free to use with proper credit.
