import unittest
from build_prompt import build_full_prompt

class TestBuildFullPrompt(unittest.TestCase):
    
    def setUp(self):
        # Mock user data
        self.user_data = {
            "age_group": "46-55",
            "dietary_type": "Mediterranean",
            "activity_level": "Moderately Active",
            "health_condition": "Heart Health"
        }
        self.type_of_meal = "breakfast"
        # Mock item data
        self.item_data = [
            {
                "item_name": "Lettuce",
                "category": "Vegetables",
                "nutritional_info": {"calories": 15, "carbs": 3, "fat": 0.1, "protein": 0.9}
            },
            {
                "item_name": "Tomatoes",
                "category": "Vegetables",
                "nutritional_info": {"calories": 20, "carbs": 4, "fat": 0.2, "protein": 1}
            },
            {
                "item_name": "Pork Chops",
                "category": "Meat/Fish",
                "nutritional_info": {"calories": 190, "carbs": 0, "fat": 14, "protein": 21}
            }
        ]
    
    def test_build_full_prompt(self):
        # Generate the prompt using the mock data
        prompt = build_full_prompt(self.user_data, self.item_data, self.type_of_meal)
        print(prompt)
        # Check if the prompt is generated correctly
        self.assertIn("am on a Mediterranean diet", prompt)
        self.assertIn("belong to the 46-55 age group", prompt)
        self.assertIn("activity level is Moderately Active", prompt)
        self.assertIn("health condition: Heart Health.", prompt)
        self.assertIn("are the items available for the recipe:", prompt)
        self.assertIn("ettuce (Category: Vegetables)", prompt)
        self.assertIn("ork Chops (Category: Meat/Fish)", prompt)
        print('OK')

    def test_missing_health_condition(self):
        # Remove health condition for testing
        user_data_without_health_condition = {**self.user_data, "health_condition": None}
        
        # Generate the prompt using the modified user data
        prompt = build_full_prompt(user_data_without_health_condition, self.item_data, self.type_of_meal)
        
        # Ensure that health condition is not included in the prompt
        self.assertNotIn("My health condition:", prompt)

if __name__ == '__main__':
    unittest.main()
