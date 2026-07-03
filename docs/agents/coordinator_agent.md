# Coordinator Agent

## Purpose

The Coordinator Agent serves as the central orchestration layer of CivicMind AI.

Its responsibility is to understand user requests, identify the domain and task type, and route the request to the appropriate specialized agent.

---

## Responsibilities

### Intent Classification

Determine whether the request involves:

* Analytics
* Forecasting
* Recommendations
* Knowledge Retrieval
* Report Generation

---

### Domain Classification

Identify the target domain:

* Public Health
* Environment
* Urban Mobility

---

### Agent Routing

Route requests to:

* Analytics Agent
* Prediction Agent
* Insight Agent
* Recommendation Agent
* RAG Agent
* Report Agent

---

## Input

User query

Uploaded datasets

Conversation context

---

## Output

Routing decision object

Example:

{
"domain": "environment",
"intent": "prediction",
"target_agent": "prediction_agent"
}

---

## Success Criteria

* Accurate intent classification
* Accurate domain classification
* Reliable agent orchestration
* Low latency routing
