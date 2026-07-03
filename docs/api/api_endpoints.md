# CivicMind AI API Endpoints

## Health

GET /health

---

## Coordinator

POST /api/coordinator/route

Input:

{
"query": "Predict traffic next week"
}

Output:

{
"domain": "mobility",
"intent": "prediction",
"target_agent": "prediction_agent"
}

---

## Analytics

POST /api/analytics/analyze

---

## Prediction

POST /api/predictions/forecast

---

## Insights

POST /api/insights/generate

---

## Recommendations

POST /api/recommendations/generate

---

## Reports

POST /api/reports/generate

---

## Knowledge Search

POST /api/rag/query
