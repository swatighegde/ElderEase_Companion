import json

def compile_weekly_grocery_list(items: list[str], servings: int = 1) -> str:
    """
    Compiles a finalized weekly grocery list based on needed items.
    
    Args:
        items: A list of ingredient names (strings) needed for the week.
        servings: Number of servings to plan for (default 1).
        
    Returns:
        A formatted string confirming the grocery list creation.
    """
    formatted_list = f"--- WEEKLY GROCERY LIST (Servings: {servings}) ---\n"
    for item in items:
        # Simple formatting: ensures item is present
        formatted_list += f"[ ] {item}\n"
    
    formatted_list += "----------------------------------------------"
    return formatted_list

# Tool Definition for Gemini (Used in Step 2 of grocery flow)
compile_weekly_grocery_list.tool_declaration = {
    'name': 'compile_weekly_grocery_list',
    'description': 'Generates and formats a final weekly grocery shopping list based on a list of ingredients.',
    'parameters': {
        'type': 'object',
        'properties': {
            'items': {
                'type': 'array',
                'items': {'type': 'string'},
                'description': 'List of ingredients to buy.'
            },
            'servings': {
                'type': 'integer',
                'description': 'Number of people to buy for.'
            }
        },
        'required': ['items']
    }
}