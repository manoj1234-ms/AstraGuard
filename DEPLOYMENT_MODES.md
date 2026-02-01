# ASTRAGUARD — Deployment Modes

## 1. Online Mode (Normal)
• Cloud-hosted Streamlit / Web app  
• Live data feeds (traffic, sensors, weather)  
• Full ML + scenario simulation enabled  

## 2. Offline Mode (Critical)
• Runs on local laptop / command vehicle  
• Uses last-known data snapshot  
• ML model preloaded  
• Rule-based safety always active  

## 3. Degraded Mode (Worst Case)
• Minimal inputs only (population, distance, capacity)  
• Conservative evacuation time estimates  
• ML optional, rules mandatory  
• Human approval required for execution  

ASTRAGUARD automatically shifts modes based on system health.
