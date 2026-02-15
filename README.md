Intelligent FMCG Pricing System (ML + Rules Based)

This project is an industrial-style pricing engine designed mainly for FMCG products (biscuits, milk, oil, beverages, bakery, etc.), but it is also extendable to categories like clothing, footwear, and electronics.

The system combines:
	•	Machine Learning price prediction
	•	Market price reference
	•	Rule-based price adjustment
	•	Brand, weight, and category logic
The goal is to avoid unrealistic ML predictions and generate real-world usable prices.


###Architecture Overview
 Request
  ↓
Feature Engineering
  ↓
ML Model Prediction
  ↓
Market Price Reference (optional)
  ↓
Price Adjustment Engine (rules)
  ↓
Final Price


  
Project structure
								   



Pricing-ML-System/
│
├── backend/
│   └── app/
│       ├── routes/
│       │   └── predict.py
│       ├── services/
│       │   ├── feature_service.py
│       │   ├── ml_service.py
│       │   ├── market_price_service.py
│       │   ├── cost_pricing_service.py
│       │   └── price_adjustment_service.py
│       ├── schemas/
│       │   └── prediction.py
│       └── main.py
│
├── ml/
│   ├── train.py
│   ├── features.py
│   └── dataset_merge.py
│
├── data/
│   └── raw/
│
├── models/
│   └── pricing_model.pkl
│
└── README.md





ML Model Details
	•	Algorithm used: Tree-based regression (stable for tabular data)
	•	Why not only ML?
	•	ML sometimes predicted absurd prices (₹10⁵⁰+ 😅)
	•	Especially bad for unseen categories

So ML is used as base intelligence, not final authority.
Price Adjustment engine is most important part.

Brand Multipliers
brand type 
generic with multiplier 1.0
mid with multiplier 1.05
premium with multiplier 1.25


result:
<img width="1680" height="1050" alt="Screenshot 2026-02-15 at 7 14 00 AM" src="https://github.com/user-attachments/assets/cc503ab1-9065-47c3-923f-d6730122c78f" />
<img width="1680" height="1050" alt="Screenshot 2026-02-15 at 7 13 55 AM" src="https://github.com/user-attachments/assets/6b236c3e-5cfa-4fc1-be80-745065017511" />
<img width="1680" height="1050" alt="Screenshot 2026-02-15 at 7 13 49 AM" src="https://github.com/user-attachments/assets/f32eafc0-65e1-4eda-9850-58ddd6d9bb53" />

Accuracy (FMCG Perspective)

Instead of textbook accuracy, this project measures:
	•	Market realism
	•	Price band correctness
	•	Business usability

Observed FMCG Accuracy:

✅ ~80% realistic pricing

This is considered good for pricing systems, because:
	•	Even real companies revise prices manually
	•	FMCG prices are policy + market driven

                                 Major Issues Faced & How They Were Solved
Issue 1: ML predicting absurd prices (10⁵⁷, 10⁶⁹)

Reason
	•	Poor generalization
	•	Dataset mismatch
	•	Tree model extrapolation
Fix
	•	Added hard category min/max caps
	•	ML price is now only a reference


Issue 2: Small snack packs priced too high
Example
	•	50g biscuit → ₹150 predicted



Issue 3: Dairy prices crossing ₹100
Reason
	•	ML ignored govt regulation
  fix
  if category == "dairy":
    price = min(price, 70)
