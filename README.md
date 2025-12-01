# ElderEase Companion

An AI-powered elderly companion that provides personalized weekly meal planning, recipe generation, and grocery assistance, with a modular architecture built to expand into medication reminders and safety monitoring.

---

## 📌 Problem

Elderly individuals often face challenges maintaining proper nutrition and independence. Meal planning becomes difficult due to:

* Dietary restrictions (e.g., low sodium, gluten-free)
* Health conditions (e.g., hypertension, diabetes)
* Difficulty chewing or digesting certain foods
* Cognitive load of weekly grocery planning

Without support, seniors risk poor nutrition, inconsistency in meals, and increased dependency on caregivers.

---

## ✅ Solution

**ElderEase Companion** is a multi-agent system built using **Google ADK (Agent Development Kit 6+)** and **Gemini 2.5 Flash**, designed to:

* Generate **personalized 7-day meal plans**
* Provide **breakfast, lunch, and dinner recipes** tailored to diets and conditions
* Produce a **consolidated weekly grocery list**
* Store and retrieve data using **InMemorySessionService**
* Lay the foundation for future modules: medication reminders, check-ins, and safety monitoring

This system supports independent living while reducing caregiver load.

---

## 🧠 Architecture Overview
![Architecture Diagram](https://github.com/swatighegde/ElderEase_Companion/blob/main/ElderEase_companion_Architecture.png)

### **Project Structure**

```
ElderlyEase_companion/
│
├── main.py
├── requirements.txt
├── .env
│
├── agents/
│   ├── orchestrator_agent.py
│   ├── meal_agent.py
│   └── profile_agent.py
│
├── tools/
│   ├── grocery_tool.py
│   └── extraction_tool.py
│
└── profiles/
    ├── rita.json
    ├── joan.json
    └── li.json
    ├── mark.json
    └── ashley.json
```

### 🧩 **Agents**

#### **1. Profile Agent**

* Loads and validates user profiles
* Processes dietary restrictions, health conditions, preferences, and calorie targets

#### **2. Meal Agent**

* Uses **Gemini 2.5 Flash** to generate:

  * 7-day meal plan
  * Recipes for breakfast, lunch, dinner
* Respects health conditions, diet, chewing preferences, and calorie limits

#### **3. Orchestrator Agent**

* Coordinates flow between agents and tools
* Handles user inputs and requests
* Stores outputs in **InMemorySessionService**

### 🛠 Tools

#### **Grocery Tool**

* Extracts ingredients from all recipes
* Produces weekly consolidated grocery list

#### **Extraction Tool**

* Structures recipe content for downstream processing
* Helps maintain consistency in memory storage

### 💾 **Memory System**

* Uses Google ADK’s **InMemorySessionService** to store:

  * User profile
  * Weekly meal plan
  * Recipes
  * Grocery lists

---

## 🔄 System Flow Diagram 



---

## 🚀 Setup Instructions

### **1. Clone the Repository**

```bash
git clone <your-repo-url>
cd ElderlyEase_companion
```

### **2. Create & Activate Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### **3. Install Requirements**

```bash
pip install -r requirements.txt
```

### **4. Create `.env` File**

Add your Gemini key:

```
GOOGLE_API_KEY=your_api_key_here
```

### **5. Run the Application**

```bash
python main.py
```

You should see:

```
Welcome to ElderEase Companion
Please enter your User ID:
```

Enter one of the existing profile IDs:

* `rita`
* `joan`
* `li`
* `mark`
* `ashley`
---

## 🌟 Features

* Personalized weekly meal plans
* Recipes adapted for senior dietary needs
* Grocery list generation
* Modular multi-agent architecture
* Gemini 2.5 Flash-powered reasoning
* In-memory context for conversational follow-ups

---

## 🔮 Future Enhancements

* **Medication Agent**: reminders, interaction checks, scheduling
* **Safety Check-In Agent**: daily wellness prompts, fall detection alerts
* **Voice-based interface** for accessibility
* **Remote caregiver dashboard**

---

## 📜 License

This project is for demo purposes as part of Google ADK-based agent systems.

---

## 🙌 Acknowledgments

Built using:

* **Google ADK 6+**
* **Gemini 2.5 Flash**
* Python 3+

ElderEase Companion demonstrates how multi-agent AI systems can meaningfully support senior wellness, nutrition, and independence.

