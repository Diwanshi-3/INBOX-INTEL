📧 INBOX-INTEL

AI-Powered Gmail Spam Detection using Machine Learning and Python

🧠 Project Overview

This project uses Machine Learning + NLP to classify emails as:

✅ Ham (Normal Email)
🚫 Spam (Unwanted / Scam Email)

⚙️ Tech Stack
Python 🐍
Scikit-learn 🤖
Pandas
NumPy
NLP (TF-IDF Vectorizer)
Streamlit (UI)
Pickle (Model Saving)

📂 Project Structure
Spam_Email Classifier/
│
├── app.py
├── model.pkl
├── vectorizer.pkl
├── dataset/
├── ml/
├── auth/
├── ui/
├── gmail/
├── project.ipynb
├── README.md

🧪 How It Works
Email text is cleaned (NLP preprocessing)
Converted into numerical features using TF-IDF
ML model predicts:
Spam
Not Spam
Result shown in Streamlit UI
📊 Model Used
Multinomial Naive Bayes / Logistic Regression

Accuracy: 96%

▶️ How to Run
# Clone repository
git clone https://github.com/Diwanshi-3/INBOX-INTEL.git

# Go to project folder
cd INBOX-INTEL

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py

📌 Features
Spam detection in real-time
NLP-based text processing
Clean Streamlit UI
Pre-trained ML model

👩‍💻 Author

Diwanshi
BTech CSE Student
Machine Learning Enthusiast 🚀

⭐ Future Improvements
Deep Learning (LSTM / Transformers)
Better dataset expansion
Gmail API integration
Cloud deployment (Render / AWS / Streamlit Cloud)

📜 License

This project is open-source and free to use.
