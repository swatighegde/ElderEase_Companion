import os
from google import genai

class MealAgent:
    """Handles the generative task of creating the 7-day meal plan."""
    
    def __init__(self, model_id="gemini-2.5-flash"):
        self.client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model_id = model_id

    def generate_meal_plan(self, profile: dict) -> str:
        """
        Generates a 7-day (weekly) meal plan based on health profile.
        """
        # Defensive coding using .get() for safety
        prompt = (
            f"Act as a geriatric nutritionist. Create a **7-DAY WEEKLY MEAL PLAN** for {profile.get('name', 'User')} "
            f"(Age: {profile.get('age', 'Unknown')}).\n"
            f"Health Conditions: {', '.join(profile.get('health_conditions', []))}\n"
            f"Dietary Restrictions: {', '.join(profile.get('dietary_restrictions', []))}\n"
            f"Preferences: {', '.join(profile.get('preferences', []))}\n"
            f"Target Calories: {profile.get('calorie_target', '1600')} per day.\n\n"
            "**Output Format (Strictly adhere to this format):**\n"
            "For each day (Monday-Sunday), provide:\n"
            "**[DAY NAME]**\n"
            "BREAKFAST: [Recipe Name] (Ingredients: list of ingredients **with quantities**)-Full Recipe- [Approx. Calories]\n"
            "LUNCH: [Recipe Name] (Ingredients: list of ingredients **with quantities**) -Full Recipe - [Approx. Calories]\n"
            "DINNER: [Recipe Name] (Ingredients: list of ingredients **with quantities**) -Full Recipe- [Approx. Calories]\n"
            "Ensure the output includes detailed ingredients with full receipe in 2 lines (e.g., Add '1 cup rolled oats' and '2 tbsp honey') for accurate grocery list generation in the next step."
        )

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        return response.text