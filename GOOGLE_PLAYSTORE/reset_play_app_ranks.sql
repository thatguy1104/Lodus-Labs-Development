DROP TABLE IF EXISTS play_app_ranks;
CREATE TABLE play_app_ranks
(
    Developer NVARCHAR(100),
    App_Name NVARCHAR(100),
    App_Rank INT,
    Total_Rating BIGINT,
    Installs VARCHAR(100),
    Average_Rating FLOAT,
    Growth_30_days VARCHAR(100),
    Growth_60_days VARCHAR(100),
    Price VARCHAR(50),
    Last_Updated DATETIME
);