from google.cloud import bigquery
import pandas as pd
import plotly.express as px

# Connect to BigQuery
def connect_to_bigquery():
    client = bigquery.Client()
    print("Connected to BigQuery.")
    return client

# Query Data from Views
def query_view(client, view_name):
    query = f"SELECT * FROM `sustainathors_database.{view_name}`"
    return client.query(query).to_dataframe()

# Visualize Food Saved Percentages
def plot_food_saved(data, output_file, resolution=12):
    # Melt the dataframe to create bars for 100%, 50%, and 25% compliance
    data_melted = data.melt(
        id_vars=["UserID"],
        value_vars=["Saved_100", "Saved_50", "Saved_25"],
        var_name="ComplianceLevel",
        value_name="PercentageSaved"
    )

    # Add user-friendly labels
    data_melted["UserLabel"] = data_melted["UserID"].apply(lambda user_id: f"User {user_id}")
    data_melted["ComplianceLevel"] = data_melted["ComplianceLevel"].map({
        "Saved_100": "100% Compliance",
        "Saved_50": "50% Compliance",
        "Saved_25": "25% Compliance"
    })

    # Create bar chart with grouped bars
    fig = px.bar(
        data_melted,
        x="UserLabel",
        y="PercentageSaved",
        color="ComplianceLevel",
        barmode="group",
        title="Percentage of Food Saved Per User at Different Compliance Levels",
        labels={
            "UserLabel": "User",
            "PercentageSaved": "Percentage Saved (%)",
            "ComplianceLevel": "Compliance Level"
        },
        color_discrete_map={
            "100% Compliance": "#2C5F2D",
            "50% Compliance": "#6CA870",
            "25% Compliance": "#B9E4C9"
        },
    )
    fig.update_traces(texttemplate='%{y}%', textposition='outside')
    fig.update_layout(
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        template="plotly_white",
        title_font=dict(size=18, color="darkgreen"),  # Dark green title
        xaxis=dict(title="User", gridcolor="lightgrey"),
        yaxis=dict(title="Percentage Saved (%)", gridcolor="lightgrey"),
        plot_bgcolor="white",  # Clean white background
    )

    # Save plot as high-resolution PNG
    fig.write_image(output_file, scale=resolution)
    print(f"Plot saved as {output_file}")

# Main Function
if __name__ == "__main__":
    # Step 1: Connect to BigQuery
    client = connect_to_bigquery()

    # Step 2: Query Data from the View
    food_saved_data = query_view(client, "V_FoodSavedPerUser")

    # Step 3: Visualize Data
    plot_food_saved(
        food_saved_data,
        output_file="food_saved_per_user.png",
        resolution=5
    )
