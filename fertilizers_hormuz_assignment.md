# Fertilizers and the Gulf of Hormuz

## Background

The Iran war has most famously affected the price of oil, because of the current holdup in the Strait of Hormuz. But oil is not the whole story: Persian Gulf countries also export a great deal of fertilizer via the strait (as well as helium and aluminum).

In fact, these countries export so much fertilizer that there are concerns about the price and availability of fertilizer for the world's farmers, just as planting season begins in the northern hemisphere.

Source: https://www.nytimes.com/2026/03/27/business/economy/fertilizer-food-supply-iran-war.html

---

### Why Fertilizer?

While we often think of cow manure as fertilizer, modern agriculture has relied on synthetic fertilizers for over a century.

The Haber–Bosch process combines nitrogen and hydrogen to produce ammonia (NH₃), which is then used to create urea, a nitrogen-rich fertilizer.

- Nitrogen → sourced from air  
- Hydrogen → typically sourced from natural gas  
- Process → highly energy-intensive  

This gives Persian Gulf countries a structural advantage due to:
- Abundant natural gas
- Low energy costs

---

### Market Impact

According to the article:

- Urea prices ↑ 50%
- Ammonia prices ↑ 20%

For farmers, this represents a significant and unexpected increase in input costs.

---

## Assignment

This week, we analyze fertilizer trade using data from the FAO (Food and Agriculture Organization of the United Nations):

https://www.fao.org/

We will explore:

- How much fertilizer comes from the Persian Gulf  
- Which countries depend on these exports  

---

# FAOSTAT Fertilizer Trade (RFM) — Data Dictionary

## 1. Core Identifiers

| Field | Type | Description |
|------|------|-------------|
| Area Code (Reporter) | Integer | Numeric code for reporting country |
| Area (Reporter) | String | Country reporting the trade |
| Partner Code | Integer | Numeric code for partner country |
| Partner Countries | String | Trade partner country |
| Item Code | Integer | Code for fertilizer type |
| Item | String | Fertilizer category (nutrient basis) |
| Element Code | Integer | Code for trade variable |
| Element | String | Type of measurement |

---

## 2. Time Dimension

| Field | Type | Description |
|------|------|-------------|
| Year Code | Integer | Numeric year identifier |
| Year | Integer | Calendar year (e.g., 2023) |

---

## 3. Measurement / Value Fields

| Field | Type | Description |
|------|------|-------------|
| Unit | String | Measurement unit (typically *tonnes of nutrient*) |
| Value | Float | Reported trade value |
| Flag | String | Data quality flag |
| Flag Description | String | Explanation of flag |

---

## 4. Elements (Key Analytical Variables)

| Element | Meaning |
|--------|--------|
| Import quantity (tonnes N) | Nitrogen imported |
| Export quantity (tonnes N) | Nitrogen exported |
| Import quantity (tonnes P2O5) | Phosphate imports |
| Export quantity (tonnes P2O5) | Phosphate exports |
| Import quantity (tonnes K2O) | Potash imports |
| Export quantity (tonnes K2O) | Potash exports |

> Note: Values are expressed in nutrient-equivalent terms, not raw fertilizer weight.

---

## 5. Item (Fertilizer Types)

| Item | Description |
|------|------------|
| Nitrogen fertilizers (N) | Urea, ammonium nitrate, etc. |
| Phosphate fertilizers (P2O5) | Phosphoric acid-based fertilizers |
| Potash fertilizers (K2O) | Potassium-based fertilizers |

---

## 6. Flags (Data Quality)

| Flag | Meaning |
|------|--------|
| A | Official data |
| E | Estimated |
| F | FAO estimate |
| M | Missing data |
| X | Not applicable |

---

## 7. Conceptual Structure

Each row represents:

(Reporter Country, Partner Country, Fertilizer Type, Element, Year) → Value

This is a multi-dimensional panel dataset:

- Cross-section → country pairs  
- Time → yearly  
- Measures → imports/exports by nutrient  

---

## 8. Typical Transformations

### Example workflow

```python
df = (
    df
    .loc[lambda d: d["Element"] == "Import quantity (tonnes N)"]
    .assign(
        year=lambda d: d["Year"].astype(int)
    )
    .groupby("Area (Reporter)")["Value"]
    .sum()
)
```

---

## Questions

### 1. Data Preparation
- Read the "all fertilizers trade matrix, no flag" CSV file into a DataFrame  
- Keep only rows where:
  - Element == "Export quantity (tonnes N)"  
- Keep only year-related columns  

---

### 2. Persian Gulf Exports Analysis

Persian Gulf countries:

- Saudi Arabia  
- Bahrain  
- Iran  
- Iraq  
- Oman  
- Qatar  
- Kuwait  
- United Arab Emirates  

Tasks:

- Create a stacked bar chart showing total fertilizer exports by country over time  
- Create another chart showing:
  - Persian Gulf urea exports  
  - As a share of total global fertilizer exports  

---

### 3. Top Importers (2023)

- Identify the top 10 importers of nitrogen fertilizers  
- Source: Persian Gulf countries  

---

### 4. Dependency Risk Analysis (2023)

- Identify the top 10 countries by % dependence on Persian Gulf fertilizer imports  
- Exclude Persian Gulf countries  
- Display results as percentages  
