from flask import Flask, render_template, request, jsonify
from collections import defaultdict
import json
from prompt.generate_prompt import generate
from ecobyte_client import fetch_user_profile, fetch_available_stock, fetch_nearly_expired
from prompt.build_prompt import parse_user_data, parse_item_data, parse_grouped_data, build_prompt_recipe, build_prompt_shop
# Logging functionality
import google.cloud.logging
client = google.cloud.logging.Client()
client.setup_logging()
import logging

app = Flask(__name__)

def get_type_of_meal(selected_option):
    if any(word in selected_option for word in ['breakfast', 'lunch', 'dinner']):
        type_of_meal = [word for word in ['breakfast', 'lunch', 'dinner'] if word in selected_option][0]
    else:
        type_of_meal = None
    return type_of_meal

def process(selected_user, selected_option):
    match selected_option:
        case 'expire-items':
            item_json = fetch_nearly_expired(selected_user)
            items = parse_grouped_data(item_json)

            # Transform the input list into a dictionary
            category_dict = defaultdict(list)
            for item in items:
                category_dict[item['category']].append(item['item_name'] + " (" + item['portions'] + ")")

            # Create the desired output format
            output = []
            for category, item_list in category_dict.items():
                output.append(f"{category}: {', '.join(item_list)}")

            # Print the result
            output = "\t \n".join(output)
            print(output)
            #output = "\t ".join(output)

        case 'breakfast-recipe' | 'lunch-recipe' | 'dinner-recipe' | 'shopping-list':
            
            # Fetch user profile data
            user_json = fetch_user_profile(selected_user)
            user_data = parse_user_data(json.loads(user_json))  # Parse the user data from JSON string
            # Fetch available stock data
            item_json = fetch_available_stock(selected_user)
            item_data = parse_item_data(item_json)  # Parse the item data from JSON string
            
            if selected_option == 'shopping-list':
                prompt = build_prompt_shop(user_data, item_data)
                print("Asking for a shopping list..")
                logging.info(f"Asking for a shopping list..")
            else:
                type_of_meal = get_type_of_meal(selected_option)
                prompt = build_prompt_recipe(user_data, item_data, type_of_meal)
                print("Asking for a specific meal, based on user profile..")
                logging.info(f"Asking for a specific meal, based on user profile..")
            
            agent_output = generate(prompt)
            #output = agent_output + '\n'+f'This answer was based on the following prompt: {prompt}'
            output = agent_output
            print(output)
        case _:
            print('Non matching case.. \n')
            output = ""

    return output


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/chat', methods=['POST'])
def chat():
    selected_user = request.json.get('user') # Retrieve the user's id from the dropdown
    selected_option = request.json.get('option')  # Retrieve the user's option from the dropdown

    logging.info(f"This is user's option: {selected_option}")
    print(f"This is user's option: {selected_option}")
    
    output = process(selected_user, selected_option)
    return jsonify({'response': output})  # Send the response back as JSON


if __name__ == '__main__':
    app.run(debug=True)
