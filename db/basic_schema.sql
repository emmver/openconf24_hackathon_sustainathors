CREATE TABLE sustainathors_database.Users (
    UserID INT NOT NULL, -- Use UUID for primary key
    AgeGroup STRING NOT NULL,
    DietaryType STRING NOT NULL,
    ActivityLevel STRING NOT NULL,
    HealthCondition STRING,
    CreatedAt TIMESTAMP NOT NULL
);

CREATE TABLE sustainathors_database.DietaryProfiles (
    ProfileID INT NOT NULL, -- Use UUID for primary key
    UserID INT NOT NULL,
    TimesEatingMeatPerWeek INT64,
    TimesEatingFishPerWeek INT64,
    DailyFruitIntake INT64,
    SnackTypePreference STRING,
    DailyWaterIntake FLOAT64,
    UpdatedAt TIMESTAMP NOT NULL,
    -- Add foreign key logic externally, as BigQuery does not enforce constraints
);

CREATE TABLE sustainathors_database.Items (
    ItemID INT NOT NULL, -- Use UUID for primary key
    UserID INT NOT NULL,
    ItemDetailID INT NOT NULL,
    ItemName STRING NOT NULL,
    Category STRING NOT NULL,
    BoughtDate DATE NOT NULL,
    ExpirationDate DATE NOT NULL,
    UsedBeforeExpiry BOOLEAN
);

CREATE TABLE sustainathors_database.ItemDetails (
    ItemDetailID INT NOT NULL, -- Use UUID for primary key
    ItemName STRING NOT NULL,
    TypicalUsageDays INT64,
    Category STRING NOT NULL,
    NutritionalInfo JSON,
    CreatedAt TIMESTAMP NOT NULL
);

CREATE TABLE sustainathors_database.Recommendations (
    RecommendationID INT NOT NULL, -- Use UUID for primary key
    UserID INT NOT NULL,
    RecommendationText STRING NOT NULL,
    Accepted BOOLEAN,
    CreatedAt TIMESTAMP NOT NULL
);

CREATE TABLE sustainathors_database.Locations (
    LocationID INT,             -- Unique identifier for each location
    LocationName STRING NOT NULL,     -- Name of the location
    Latitude FLOAT64 NOT NULL,                -- Latitude of the location
    Longitude FLOAT64 NOT NULL,               -- Longitude of the location
    LocationType STRING NOT NULL,      -- 'BrownBin' or 'Charity'
);
