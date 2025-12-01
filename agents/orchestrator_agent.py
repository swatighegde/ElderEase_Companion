import os
import time 
from google import genai
from google.genai import types
from google.genai.types import ToolConfig, FunctionCallingConfig 
from .profile_agent import ProfileAgent
from .meal_agent import MealAgent
from tools.grocery_tool import compile_weekly_grocery_list
from tools.extraction_tool import extract_ingredients_to_list

# --- CORE ADK CONCEPT: IN MEMORY SERVICE ---
class InMemoryService:
    """
    A simple in-memory state manager to hold conversation context
    and current user session data without persistent storage.
    """
    def __init__(self):
        self._store = {}

    def set_state(self, key: str, value: any):
        self._store[key] = value

    def get_state(self, key: str):
        return self._store.get(key)

# --- ORCHESTRATOR AGENT ---
class OrchestratorAgent:
    """
    The central agent responsible for flow control, state management, and 
    sequential task routing (Meal -> Grocery Extraction -> Grocery Formatting).
    """
    
    MODEL_ID = "gemini-2.5-flash" 
    # Delay in seconds to respect the 10 requests/minute free tier limit
    RATE_LIMIT_DELAY = 30

    def __init__(self):
        self.memory = InMemoryService()
        self.profile_agent = ProfileAgent()
        self.meal_agent = MealAgent(model_id=self.MODEL_ID)
        self.client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    def start_session(self):
        """Initiates the user session and handles the top-level flow."""
        print("\n--- Elderly Meal Companion System ---")
        user_id = input("Please enter User ID (rita/joan/li/ashley/mark): ").strip().lower()
        
        profile = self.profile_agent.load_profile(user_id)
        if not profile:
            print(f"❌ Error: User profile '{user_id}' not found.")
            return

        self.memory.set_state('user_profile', profile)
        print(f"✅ Welcome, {profile['name']}. Profile loaded successfully.")
        
        # The flow is now hardcoded to start with the meal plan
        self._handle_meal_intent(profile)

    def _handle_meal_intent(self, profile):
        """
        Handles the request for a weekly meal plan, stores it, and prompts
        the user about the sequential grocery list.
        """
        print("\nGenering customized 7-day meal plan.")
        
        plan = self.meal_agent.generate_meal_plan(profile)
        
        print("\n" + "="*30)
        print("7-DAY PERSONALIZED MEAL PLAN")
        print("="*30)
        print(plan)
        print("="*30)
        
        self.memory.set_state('last_meal_plan', plan) 

        #  Delay after the first API call
        time.sleep(self.RATE_LIMIT_DELAY)
        
        grocery_request = input(
            "\nDo you want the Grocery List for the ingredients in this 7-day meal plan? (yes/no): "
        ).strip().lower()
        
        if grocery_request == 'yes':
            self._handle_extracted_grocery_intent(plan)
        else:
            print("Session ended. Have a great week!")

    def _handle_extracted_grocery_intent(self, meal_plan_text):
        """
        Executes the 2-step process: 1. Extract ingredients using LLM tool call. 
        2. Format the final list using LLM tool call.
        """
        print("\n--- Generating Grocery List from Meal Plan ---")

        # --- STEP 1: INGREDIENT EXTRACTION (API Call 2/3) ---
        print("1. Asking model to extract all unique ingredients...")
        
        extraction_prompt = (
            f"Analyze the following 7-day meal plan text carefully. Your goal is to identify "
            f"every single distinct raw food item and ingredient required to prepare ALL the "
            f"meals listed. Ignore calories, day names, and instructions. "
            f"Call the 'extract_ingredients_to_list' tool with the final comprehensive list.\n\n"
            f"MEAL PLAN TEXT:\n{meal_plan_text}"
        )
        
        tool_config_step1 = ToolConfig(
            function_calling_config=FunctionCallingConfig(
                mode="ANY", 
                allowed_function_names=["extract_ingredients_to_list"] 
            )
        )
        
        response_step1 = self.client.models.generate_content(
            model=self.MODEL_ID,
            contents=extraction_prompt,
            config=types.GenerateContentConfig(
                tools=[extract_ingredients_to_list], 
                tool_config=tool_config_step1
            )
        )

        extracted_ingredients = []
        if response_step1.function_calls:
            call = response_step1.function_calls[0]
            if call.name == 'extract_ingredients_to_list':
                extracted_ingredients = call.args.get('ingredients', [])
                print(f"✅ Extracted {len(extracted_ingredients)} ingredients.")
            
        if not extracted_ingredients:
            print("❌ Failed to extract ingredients from meal plan. Cannot create grocery list.")
            return

        #  Delay after the second API call
        time.sleep(self.RATE_LIMIT_DELAY)

        # --- STEP 2: GROCERY LIST FORMATTING (API Call 3/3) ---
        print("2. Formatting the final grocery list...")
        
        final_list_prompt = (
            "You are a shopping list formatter. Take the following list of raw ingredients "
            "and call the 'compile_weekly_grocery_list' tool to format it nicely for the user. "
            "Do not add or remove any items. You must call the tool."
            f"\n\nINGREDIENT LIST:\n{', '.join(extracted_ingredients)}"
        )
        
        tool_config_step2 = ToolConfig(
            function_calling_config=FunctionCallingConfig(
                mode="ANY",
                allowed_function_names=["compile_weekly_grocery_list"]
            )
        )
        
        response_step2 = self.client.models.generate_content(
            model=self.MODEL_ID,
            contents=final_list_prompt,
            config=types.GenerateContentConfig(
                tools=[compile_weekly_grocery_list],
                tool_config=tool_config_step2
            )
        )

        # Handle Final Tool Execution
        if response_step2.function_calls:
            call = response_step2.function_calls[0]
            if call.name == 'compile_weekly_grocery_list':
                args = call.args
                # We execute the final formatting function
                result = compile_weekly_grocery_list(
                    items=args.get('items', extracted_ingredients),
                    servings=args.get('servings', 1)
                )
                print("\n[Tool Output - Customized Grocery List]:")
                print(result)
        else:
            print("❌ Error: Final tool call failed. Could not format grocery list.")
            print(response_step2.text)