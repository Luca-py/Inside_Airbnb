# Airbnb Pricing Analysis: Berlin vs Munich

---

## 1. Project Overview

This project investigates what factors drive Airbnb listing prices in two major German cities: **Berlin** and **Munich**.  
Using a combination of **SQL**, **Python**, and **statistical testing** (t-tests, correlations), I analyzed the effects of **room type**, **location**, and **city differences** on listing prices.

---

## 2. Key Findings

### Room Type vs. Price
- **T-statistic**: -17.2141
- **P-value**: < 0.0001

**⇒ Conclusion**:  
Listings offering a **Private Room** are **cheaper** than listings offering an **Entire Home/Apt**.

**Insight**:  
Room type is a strong driver of price variation on Airbnb.

---

### Downtown vs Non-Downtown
- **T-statistic**: 8.0603
- **P-value**: < 0.0001

**⇒ Conclusion**:  
**Downtown listings** are **more expensive** than listings located outside of downtown neighborhoods.

**Insight**:  
**Location** is a key factor influencing Airbnb pricing.

---

### Berlin vs Munich
- **T-statistic**: -7.6223
- **P-value**: < 0.0001

**⇒ Conclusion**:  
**Berlin listings** are **cheaper** than **Munich listings** on average.

**Insight**:  
City-specific market dynamics lead to major price differences.

---

### Correlation Between Price and Review Score
- **Correlation coefficient**: -0.0346

**⇒ Conclusion**:  
There is **almost no meaningful correlation** between a listing’s review score and its price.

**Insight**:  
Higher review scores do not substantially impact pricing.

---

## 3. Methods Used

- **Data Sources**: [Inside Airbnb datasets](http://insideairbnb.com/get-the-data.html) for Berlin and Munich
- **Data Storage**: PostgreSQL
- **Data Cleaning**: Python (Pandas), SQL
- **Statistical Analysis**:
  - T-tests using `scipy.stats.ttest_ind`
  - Correlation analysis using `pandas.DataFrame.corr()`
- **Visualization Tool**: Tableau Public
- **Dashboard**: https://public.tableau.com/views/InsideAirbnb_17457534285250/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link