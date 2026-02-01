# ASTRAGUARD — System Architecture

## 1. Data Layer
Inputs:
• Population & zone data  
• Route geometry & distance  
• Road capacity & congestion  
• Environmental risk indicators  

Data can be live, cached, or manually entered.

---

## 2. Scenario Engine
• Applies stress conditions (congestion, capacity loss)  
• Simulates worst-case scenarios  
• Forces conservative assumptions  

Purpose: prevent optimistic planning.

---

## 3. ML Prediction Engine
• Predicts evacuation time  
• Learns nonlinear relationships  
• Provides feature importance  

ML assists — it never decides alone.

---

## 4. Safety & Rule Layer (CORE MOAT)
• Enforces physical constraints  
• Blocks unsafe recommendations  
• Prevents underestimation  
• Flags low-confidence decisions  

This layer overrides ML when required.

---

## 5. Decision Comparator
• Compares baseline vs stressed scenarios  
• Detects decision instability  
• Triggers alerts  

Ensures decisions remain valid as conditions change.

---

## 6. Human-in-the-Loop Control
• High-risk routes require approval  
• Operators can override recommendations  
• System explains why decisions changed  

Human authority is always preserved.

---

## 7. Output Layer
• Recommended primary & backup routes  
• Confidence scores & risk flags  
• Zone-level evacuation plans  

Designed for command-center usage.
