# Khanoomi Beauty E-Commerce: Market Intelligence and Advanced Feature Pipeline

## Project Overview & Business Objectives
This repository contains the end-to-end data pipeline designed for processing raw e-commerce metadata extracted from Khanoomi (www.khanoumi.com), Iran's leading beauty and cosmetics online cosmetics retailer. 

The primary business objective of this project is to build a robust, scalable engineering infrastructure that transforms fragmented, unstructured web scraped data into a high-dimensional, model-ready feature store. By joining core catalog metrics with direct consumer behavior signals, the system uncovers actionable market insights such as:
* **Pricing Elasticity & Strategy:** Segmenting commercial items into structural price categories dynamically mapped against specific sub-category benchmarks.
* **Consumer Sentiment & Engagement Dynamics:** Translating long-tail text reviews, user interactions, and engagement indicators into quantitative weights.
* **Product Popularity Formulation:** Designing combined interaction indexes to evaluate market trends independent of frequency bias.

---

## Technical Project Structure
To comply with modular design principles and avoid execution failures across different environments, all core execution scripts are located directly within the root directory:

* `database_connection.py`: Centralized utility using native connections to safely interact with the local SQLite data engine.
* `load_data.py`: Handles raw entity ingestion via an advanced SQL query executing a analytical `LEFT JOIN` between products and aggregated feedback counters.
* `preprocess.py`: Implements numerical imputation using group-specific median calculations, drops anomalous values, and standardizes categorical features.
* `feature_engineering.py`: Extracted an advanced multi-dimensional matrix comprising 32 specific behavioral, lexical, and scaled statistical features.
* `pipeline.py`: Automated orchestration script that chains the ingestion, cleansing, and feature construction phases sequentially.
* `requirements.txt`: System-generated artifact containing absolute library dependencies and exact package hashes.
* `khanoomi.db`: Structured SQLite binary housing compiled relational schemas for products, reviews, and product categories.

---

## Detailed Feature Engineering Taxonomy (32 Columns Compiled)
The automated line-of-code produces a matrix of shape `(19814, 32)`. The engineering scope is categorized into the following behavioral sections:

1. **Product Categorical & Identity Features:**
   * `is_top_brand`: Binary classification (0 or 1) indicating market dominance based on high-conversion brand clusters (e.g., Bioaqua, Cinere, Lafarrerr).
   * `name_length`: Character density count of product naming structures.
   * `main_category_encoded`: Structural layout encoder mapping items into makeup or skincare macro environments.

2. **User Feedback Aggregations (Relational Metrics):**
   * `review_count`: Total textual review instances bound per product ID from the independent comments ledger.
   * `avg_comment_likes`: Social validation metric tracking the average community likes given to an item's product reviews.
   * `comment_length_avg`: Lexical structural depth marker indicating user involvement levels through overall text lengths.

3. **Advanced Mathematical & Commercial Formulation:**
   * `price_segment`: Non-biased dynamic quantile scaling (0: Economy, 1: Mid-tier, 2: Luxury) generated relative to specific sub-category behaviors rather than global pricing averages.
   * `popularity_score`: Interaction feature multiplying item metrics with log-transformed rating aggregates to prevent raw volume dominance.
   * `value_for_money_index`: Financial efficiency indicator dividing target scores by standard normalized prices.

4. **Natural Language Processing & Matrix Vectorization:**
   * `tfidf_[word]`: 10 distinct columns representing structural weights of localized high-frequency keywords (e.g., lexical extractions like "ضد") mapped directly out of text titles using a restricted vocabulary configuration.

5. **Normalization and Scale Constraints:**
   * `price_scaled`, `name_length_scaled`, `rate_scaled`: Minimum-maximum bounded features scaled strictly between 0 and 1 via `MinMaxScaler` to prevent mathematical algorithm distortion.

---

## Installation & Local Execution Guide

Follow these sequential steps within your terminal environment to initiate the execution process:

### 1. Initialize Virtual Environment
Isolate your systemic variables from the project space:
```bash
python -m venv venv

# Activate on Windows Environment:
venv\Scripts\activate

# Activate on Mac / Linux Environment:
source venv/bin/activate{\rtf1}