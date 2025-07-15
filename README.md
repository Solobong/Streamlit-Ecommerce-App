
# 📊 Customers RFM Segmentation

This project focuses on customer segmentation using RFM (Recency, Frequency, Monetary) analysis. It provides insight into customer behavior by analyzing transactional data and identifying different customer segments based on purchasing patterns.

---

## 📁 Dataset Overview

The dataset used contains records of online retail transactions, including columns like:

- **CustomerID**
- **Description**
- **Quantity**
- **UnitPrice**
- **InvoiceDate**

---

## 🧼 Data Cleaning

- **Missing Values**:  
  - `CustomerID`: Missing ~25% of values — handled using **forward fill**, assuming customers bought multiple items in one transaction.
  - `Description`: Less than 1% missing — **rows dropped**.

- **Outliers**:
  - Removed transactions with negative or zero `Quantity` and `UnitPrice < 0.1`.

---

## 📊 Exploratory Data Analysis

### 🔹 Product Analysis
- **Top Revenue-Generating Products**:
  - `Dotcom Postage`
  - `Regency Cakestand 3 Tier`
  - `Paper Craft, Little Birdie`

- **Most Ordered Products**:
  - `Paper Craft, Little Birdie` (81k units)
  - `Medium Ceramic Top Storage Jar`
  - `World War 2 Gliders Asstd Designs`

- **Most Popular Products by Frequency**:
  - `Regency Cakestand 3 Tier`
  - `White Hanging Heart T-light Holder`
  - `Party Bunting`

### 🔹 Transaction Analysis
- **Day of the Week**:
  - Wednesday = highest transaction volume.
  - Saturday = lowest.
  - Missing data for Friday noted.

- **Month of the Year**:
  - November 2017 recorded the **peak** in purchases.

---

## 📈 RFM Segmentation

Customers are segmented using:
- **Recency**: How recently a customer made a purchase.
- **Frequency**: How often they purchase.
- **Monetary**: How much money they spend.

The RFM analysis helps identify:
- Loyal customers
- High spenders
- At-risk customers
- Potential churners

---

## 📌 Tools Used

- Python
- Pandas, NumPy
- Matplotlib, Seaborn
- Jupyter Notebook

---

## 📂 How to Use

Clone the repository and run the notebook:

```bash
git clone https://github.com/Solobong/Streamlit-Ecommerce-App.git
cd Customer-Segmentation-Clustering
jupyter notebook
```

Open the notebook and run the cells to see the full analysis.

---

## 💡 Author

**Obong Solomon Francis**  
Systematical Data Scientist with strong attention to detail and a passion for data-driven insights.
