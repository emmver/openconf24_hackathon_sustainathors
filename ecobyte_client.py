from google.cloud import bigquery
import json
user_id_mapping = {"Option1": 6, "Option2": 5, "Option3": 3, "Option4": 7, "Option5": 9}


def fetch_user_profile(option):
    
    user_id = user_id_mapping[option]
    
    query = f"""
        SELECT
            U.UserID,
            U.AgeGroup,
            U.DietaryType,
            U.ActivityLevel,
            U.HealthCondition,
            DP.TimesEatingMeatPerWeek,
            DP.TimesEatingFishPerWeek,
            DP.DailyFruitIntake,
            DP.DailyWaterIntake,
            DP.SnackTypePreference
        FROM
            `openhack24ath-704.sustainathors_database.Users` as U
        INNER JOIN
            `openhack24ath-704.sustainathors_database.DietaryProfiles` as DP
        ON
            U.UserID = DP.UserID
        WHERE
            U.UserID = {user_id};
    """

    client = bigquery.Client(project="openhack24ath-704")
    results = client.query(query).result()
    
    # Convert results to a list of dictionaries
    rows = [dict(row) for row in results]

    # Convert the list to a JSON string
    json_data = json.dumps(rows, indent=4)
    return json_data


def fetch_available_stock(option):
    
    user_id = user_id_mapping[option]
    
    query = f"""
        SELECT      
            S.UsedBeforeExpiry,
            ID.ItemName,
            ID.Category,
            ID.NutritionalInfo
        FROM        
            `openhack24ath-704.sustainathors_database.Stock` as S
        INNER JOIN 
            `openhack24ath-704.sustainathors_database.ItemDetails` as ID
        ON          
            S.ItemDetailID = ID.ItemDetailID
        WHERE       
            S.UserID = {user_id}
        AND         
            S.UsedBeforeExpiry = FALSE
        AND        
            S.ExpirationDate >= CURRENT_DATE()
        ORDER BY    
            S.ExpirationDate;
    """

    client = bigquery.Client(project="openhack24ath-704")
    results = client.query(query).result()
    
    # Convert results to a list of dictionaries
    rows = [dict(row) for row in results]

    # Convert the list to a JSON string
    json_data = json.dumps(rows, indent=4)

    return json_data


def fetch_expired_unused_stock(option):
    
    user_id = user_id_mapping[option]
    
    query = f"""
        SELECT
            ExpirationDate,
            UsedBeforeExpiry,
            ItemName,
            Category
        FROM
            `openhack24ath-704.sustainathors_database.Stock`
        WHERE
            UserID = {user_id}
        AND
            UsedBeforeExpiry = FALSE
        AND
            ExpirationDate < CURRENT_DATE()
        ORDER BY    
            ExpirationDate;
    """

    client = bigquery.Client(project="openhack24ath-704")
    results = client.query(query).result()
    
    # Convert results to a list of dictionaries
    rows = [dict(row) for row in results]

    # Convert the list to a JSON string
    json_data = json.dumps(rows, indent=4)

    return json_data

def fetch_bad_recipe_data(option):
        user_id = user_id_mapping[option]
        
        query = f"""
                    SELECT      
                        S.UsedBeforeExpiry,
                        ID.ItemName,
                        ID.Category,
                        ID.NutritionalInfo
                    FROM        
                        `openhack24ath-704.sustainathors_database.Stock` as S
                    INNER JOIN 
                        `openhack24ath-704.sustainathors_database.ItemDetails` as ID
                    ON          
                        S.ItemDetailID = ID.ItemDetailID
                    WHERE       
                        S.UserID = 9
                    AND         
                        S.UsedBeforeExpiry = FALSE
                    AND        
                        S.ExpirationDate >= CURRENT_DATE()
                    AND ID.ItemName IN ('Banana',
                                    'Kale',
                                    'Tofu',
                                    'Edamame')
                    ORDER BY    
                        S.ExpirationDate;
                """

        client = bigquery.Client(project="openhack24ath-704")
        results = client.query(query).result()
        
        # Convert results to a list of dictionaries
        rows = [dict(row) for row in results]

        # Convert the list to a JSON string
        json_data = json.dumps(rows, indent=4)

        return json_data

def fetch_nearly_expired(option):
        user_id = user_id_mapping[option]
        query = f"""
                   SELECT      
                        ID.ItemName,
                        ID.Category,
                        -- S.UsedBeforeExpiry,
                        -- ID.NutritionalInfo,
                        CAST(count(1) as STRING) as Portions
                    FROM        
                        `openhack24ath-704.sustainathors_database.Stock` as S
                    INNER JOIN 
                        `openhack24ath-704.sustainathors_database.ItemDetails` as ID
                    ON          
                        S.ItemDetailID = ID.ItemDetailID
                    WHERE       
                        S.UserID = {user_id}
                    AND         
                        S.UsedBeforeExpiry = FALSE
                    AND        
                        (
                            CURRENT_DATE <= S.ExpirationDate
                            AND DATE_DIFF(S.ExpirationDate, CURRENT_DATE, DAY) <= 2
                        )
                    GROUP BY
                        ID.ItemName,
                        ID.Category
                        --,S.UsedBeforeExpiry
                        --,ID.NutritionalInfo
                    ORDER BY    
                        Portions DESC;
                """

        client = bigquery.Client(project="openhack24ath-704")
        results = client.query(query).result()
        
        # Convert results to a list of dictionaries
        rows = [dict(row) for row in results]

        # Convert the list to a JSON string
        json_data = json.dumps(rows, indent=4)

        return json_data

    