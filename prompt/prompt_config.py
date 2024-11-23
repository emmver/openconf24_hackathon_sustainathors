# --- Templates for prompt construction ---
USER_PROMPT_RECIPE = (
    "I want you to prepare a {type_of_meal} meal. Here is my personal information: \n"
    "I am on a {dietary_type} diet. I belong to the {age_group} age group, "
    "and my activity level is {activity_level}."
    "{health_condition_part}"
)

USER_PROMPT_SHOP = (
    "I want you to provide me a grocery shopping list. Here is my personal information: \n"
    "I am on a {dietary_type} diet. I belong to the {age_group} age group, "
    "and my activity level is {activity_level}.\n Please also justify why you are suggesting these items."
)

ITEM_PROMPT_RECIPE = (
    "Here are the items available for the recipe:\n"
    "{item_list}\n"
    "Please prioritize the items based on the order provided."
)

ITEM_PROMPT_SHOP = ("Here are the items I already have in stock:\n"
    "{item_list}\n"
)

ITEM_ENTRY_TEMPLATE = "- {item_name} (Category: {category})."