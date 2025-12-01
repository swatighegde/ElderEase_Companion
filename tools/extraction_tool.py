import json

def extract_ingredients_to_list(ingredients: list[str]) -> str:
    """
    Takes a list of extracted ingredients and returns a structured JSON string.
    
    Args:
        ingredients: A comprehensive list of distinct ingredients.
        
    Returns:
        A JSON string containing the extracted ingredients list.
    """
    # This function is a placeholder to receive the structured data 
    # from the LLM after it performs the analysis.
    return json.dumps({"ingredients": ingredients})

# Tool Definition for Gemini (Used in Step 1 of grocery flow)
extract_ingredients_to_list.tool_declaration = {
    'name': 'extract_ingredients_to_list',
    'description': 'Analyzes the full meal plan text, identifies all necessary raw food ingredients across all meals, and returns them as a structured list.',
    'parameters': {
        'type': 'object',
        'properties': {
            'ingredients': {
                'type': 'array',
                'items': {'type': 'string'},
                'description': 'A comprehensive list of all distinct ingredients needed for the entire 7-day meal plan, including quantities where known (e.g., "1 head of broccoli", "1 lb tofu").'
            }
        },
        'required': ['ingredients']
    }
}