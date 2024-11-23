import json
from typing import Dict, List
from prompt.prompt_config import USER_PROMPT_RECIPE, USER_PROMPT_SHOP, ITEM_PROMPT_RECIPE, ITEM_PROMPT_SHOP, ITEM_ENTRY_TEMPLATE

# -- Parsing functions --
def parse_user_data(json_data: List[Dict]) -> Dict[str, str]:
    """
    Parses user data JSON to extract relevant fields for building the user prompt.
    Args:
        json_data (List[Dict]): List of user data, each as a dictionary.
    Returns:
        Dict[str, str]: A dictionary containing the parsed user information.
    """
    user = json_data[0]  # Assuming the list contains one user record
    return {
        "age_group": user.get("AgeGroup"),
        "dietary_type": user.get("DietaryType"),
        "activity_level": user.get("ActivityLevel"),
        "health_condition": user.get("HealthCondition", None),  # Optional field
    }

def parse_item_data(json_data: str) -> List[Dict[str, str]]:
    """
    Parses item data JSON to extract relevant fields for building the item prompt.
    Args:
        json_data (str): A JSON string containing item data.
    Returns:
        List[Dict[str, str]]: A list of dictionaries with parsed item information.
    """
    item_list = json.loads(json_data)  # Convert JSON string to a Python list
    parsed_items = []
    for item in item_list:
        parsed_item = {
            "item_name": item.get("ItemName"),
            "category": item.get("Category"),
        }
        parsed_items.append(parsed_item)
    return parsed_items

def parse_grouped_data(json_data: str) -> List[Dict[str, str]]:
    """
    Parses grouped data JSON to extract relevant fields for building the item prompt.
    """
    item_list = json.loads(json_data)  # Convert JSON string to a Python list
    parsed_items = []
    for item in item_list:
        parsed_item = {
            "item_name": item.get("ItemName"),
            "category": item.get("Category"),
            "portions": item.get("Portions"),
        }
        parsed_items.append(parsed_item)
    return parsed_items

# ----- Prompt building functions -----
def build_user_profile_recipe(user_data: Dict[str, str], type_of_meal) -> str:
    """
    Builds the user part of the prompt based on the user data and template.
    """
    health_condition_part = (
        f" I have a specific health condition: {user_data['health_condition']}."
        if user_data.get("health_condition") is None
        else ""
    )
    return USER_PROMPT_RECIPE.format(
        type_of_meal=type_of_meal,
        dietary_type=user_data["dietary_type"],
        age_group=user_data["age_group"],
        activity_level=user_data["activity_level"],
        health_condition_part=health_condition_part,
    )

def build_user_profile_shop(user_data: Dict[str, str]) -> str:
    """
    Builds the user part of the prompt based on the user data and template.
    """
    health_condition_part = (
        f" I have a specific health condition: {user_data['health_condition']}."
        if user_data.get("health_condition") is None
        else ""
    )
    return USER_PROMPT_SHOP.format(
        dietary_type=user_data["dietary_type"],
        age_group=user_data["age_group"],
        activity_level=user_data["activity_level"],
        health_condition_part=health_condition_part,
    )

def build_item_profile_recipe(item_data: List[Dict[str, str]]) -> str:
    """
    Builds the item part of the prompt based on the item data and templates.
    """
    item_list = "\n".join(
        ITEM_ENTRY_TEMPLATE.format(item_name=item["item_name"], category=item["category"])
        for item in item_data
    )
    return ITEM_PROMPT_RECIPE.format(item_list=item_list)

def build_item_profile_shop(item_data: List[Dict[str, str]]) -> str:
    """
    Builds the item part of the prompt based on the item data and templates.
    """
    item_list = "\n".join(
        ITEM_ENTRY_TEMPLATE.format(item_name=item["item_name"], category=item["category"])
        for item in item_data
    )
    return ITEM_PROMPT_SHOP.format(item_list=item_list)

def build_prompt_recipe(user_data: Dict[str, str], item_data: List[Dict[str, str]], type_of_meal: str) -> str:
    """
    Combines the user and item prompts into a full prompt.
    """
    user_prompt = build_user_profile_recipe(user_data, type_of_meal)
    item_prompt = build_item_profile_recipe(item_data)
    return f"{user_prompt}\n\n{item_prompt}"

def build_prompt_shop(user_data: Dict[str, str], item_data: List[Dict[str, str]]) -> str:
    """
    Combines the user and item prompts into a full prompt.
    """
    user_prompt = build_user_profile_shop(user_data)
    item_prompt = build_item_profile_shop(item_data)
    return f"{user_prompt}\n\n{item_prompt}"