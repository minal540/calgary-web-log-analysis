# calgary-web-log-analysis

# Calgary Web Server Log Analysis

This project analyzes real server logs from July 1995 (Calgary Access Log) to extract insights using Python and pandas.

## 🧠 Objective
To understand user behavior, server usage, and errors by cleaning, parsing, and analyzing raw HTTP log data.

## 📌 Key Questions Answered:
1. Total number of log records
2. Unique hosts count
3. Date-wise unique file requests
4. Number of 404 errors
5. Top 15 files causing 404
6. Top 15 file extensions with 404
7. Daily bandwidth usage
8. Hourly request distribution
9. Top 10 most requested files
10. HTTP status code distribution

## 🛠️ Tools Used
- Python
- pandas, numpy
- re (Regex)
- Matplotlib & Seaborn (for visualization)
- Jupyter Notebook

## 📂 Files Included
- `notebooks/log_analysis.ipynb`: Main analysis
- `output/cleaned_log_data.csv`: Cleaned version of the log
- `requirements.txt`: Package list

## 💡 Insights
- Most requests happen in early morning hours
- HTML and GIFs are the most common 404 extensions
- Some URLs repeatedly generate errors and may need attention

## 📸 Screenshots
(Add 2-3 screenshots of your notebook and plots here if you want.)

## 📬 Connect
Created by [Minal Jain](https://www.linkedin.com/in/minal-jain-26a6101a6/).  
Feel free to fork or connect with me on LinkedIn!
