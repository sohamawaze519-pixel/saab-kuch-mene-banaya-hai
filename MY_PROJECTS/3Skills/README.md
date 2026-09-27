# Fake Job Posting Detection Using Natural Language Processing

## 1. Project Overview

The **Fake Job Posting Detection System** is an NLP-based machine learning project developed to identify potentially fraudulent job advertisements from textual job-posting data.

The system applies Natural Language Processing techniques to clean and transform job-posting content into meaningful numerical features. These features are then used with machine learning classification algorithms to distinguish between **genuine and fake job postings**.

The project demonstrates the application of text preprocessing, feature extraction, supervised machine learning, and classification evaluation in a practical fraud-detection problem.

---

## 2. Objectives

The primary objectives of this project are:

* To develop an automated system for detecting fake job postings.
* To preprocess and normalize unstructured job-posting text.
* To apply NLP techniques for extracting useful textual information.
* To convert textual data into numerical representations using TF-IDF.
* To apply machine learning algorithms for classification.
* To evaluate the classification performance using standard evaluation metrics.

---

## 3. Methodology

The system follows the following processing pipeline:

```text
Job Posting Data
       ↓
Data Preprocessing
       ↓
HTML Removal
       ↓
Text Normalization
       ↓
Tokenization
       ↓
Stopword Removal
       ↓
Lemmatization
       ↓
TF-IDF Feature Extraction
       ↓
Machine Learning Classification
       ↓
Model Evaluation
       ↓
Fake / Genuine Classification
```

---

## 4. NLP Techniques

The following Natural Language Processing techniques are implemented:

### Text Cleaning

HTML elements and unwanted characters are removed from the job-posting content.

### Lowercase Conversion

Text is converted to lowercase to maintain consistency during feature extraction.

### Tokenization

The text is divided into individual tokens using NLTK.

### Stopword Removal

Common English stopwords are removed to reduce unnecessary textual information.

### Lemmatization

Words are converted into their base or dictionary form using the WordNet Lemmatizer.

### TF-IDF Vectorization

The cleaned textual data is transformed into numerical feature vectors using **Term Frequency-Inverse Document Frequency (TF-IDF)**.

---

## 5. Machine Learning Models

The project includes machine learning classification approaches such as:

* Logistic Regression
* Multinomial Naive Bayes

The models are trained using the numerical features generated from the processed job-posting text.

---

## 6. Technologies and Libraries

| Technology / Library | Purpose                                             |
| -------------------- | --------------------------------------------------- |
| Python               | Programming language                                |
| Jupyter Notebook     | Development and experimentation                     |
| Pandas               | Data manipulation                                   |
| NumPy                | Numerical computation                               |
| NLTK                 | Natural Language Processing                         |
| BeautifulSoup        | HTML parsing and text extraction                    |
| Scikit-learn         | Feature extraction, machine learning and evaluation |
| Matplotlib           | Data visualization                                  |
| Seaborn              | Data visualization                                  |

---

## 7. Model Evaluation

The classification models are evaluated using standard machine learning metrics, including:

* Accuracy
* Precision
* Recall
* F1-Score
* Confusion Matrix
* ROC-AUC

These metrics provide different perspectives on the model's ability to distinguish between fake and genuine job postings.

> Actual evaluation values should be added to this section based on the final execution of the trained model.

---

## 8. Project Structure

```text
Fake-Job-Posting-Detection/
│
├── fake_job_posting_model.ipynb
├── README.md
├── requirements.txt
│
├── data/
│   └── job_postings.csv
│
└── models/
    └── trained_model.pkl
```

The directory structure may vary depending on the files included in the final project repository.

---

## 9. Installation

### Prerequisites

* Python 3.x
* Jupyter Notebook
* pip

### Install Dependencies

```bash
pip install pandas numpy nltk scikit-learn matplotlib seaborn beautifulsoup4 jupyter
```

If a `requirements.txt` file is provided:

```bash
pip install -r requirements.txt
```

---

## 10. Running the Project

Clone the repository:

```bash
git clone https://github.com/your-username/fake-job-posting-detection.git
```

Navigate to the project directory:

```bash
cd fake-job-posting-detection
```

Start Jupyter Notebook:

```bash
jupyter notebook
```

Open:

```text
fake_job_posting_model.ipynb
```

Execute the notebook cells sequentially to perform:

1. Dataset loading
2. Data exploration
3. Text preprocessing
4. NLP processing
5. TF-IDF feature extraction
6. Model training
7. Prediction
8. Model evaluation

---

## 11. Applications

The developed system can be applied in:

* Online job portals
* Recruitment platforms
* Job-search applications
* Automated job-posting screening systems
* Recruitment fraud detection
* Employment-related web applications

---

## 12. Advantages

* Automates the initial screening of job postings.
* Reduces manual effort involved in identifying suspicious advertisements.
* Uses established NLP and machine learning techniques.
* Can process large volumes of textual data.
* Provides multiple evaluation metrics for model assessment.
* Can be extended with advanced NLP and deep learning techniques.

---

## 13. Future Scope

The system can be further enhanced by:

* Incorporating additional numerical and categorical features from job postings.
* Experimenting with word-embedding techniques such as Word2Vec and GloVe.
* Implementing deep learning models such as LSTM and Bi-LSTM.
* Exploring transformer-based models such as BERT.
* Developing a web-based interface for real-time classification.
* Integrating explainable AI techniques to identify the factors contributing to a prediction.
* Periodically retraining the model using newly collected job-posting data.

---

## 14. Limitations

The effectiveness of the system depends on the quality and representativeness of the training dataset. Text-based classification may not capture all characteristics of fraudulent job postings, particularly when deceptive advertisements closely resemble legitimate postings.

Therefore, the model should be considered an **automated screening or decision-support mechanism**, rather than the sole basis for determining whether a job advertisement is fraudulent.

---

## 15. Conclusion

This project demonstrates the application of **Natural Language Processing and Machine Learning** for fake job posting detection. By combining systematic text preprocessing, TF-IDF feature extraction, and supervised classification, the system provides an automated approach for analyzing job advertisements.

The project provides a practical implementation of NLP techniques and establishes a foundation for developing more advanced recruitment fraud detection systems.

---

## 16. Author

**Soham Awaze**

Electronics and Telecommunication Engineering

---

## 17. License

This project has been developed for **academic and educational purposes**.
