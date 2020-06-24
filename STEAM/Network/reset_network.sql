DROP TABLE IF EXISTS steam_network_data;
CREATE TABLE steam_network_data
(
    Country VARCHAR(100),
    Total_Bytes BIGINT,
    Avg_MB_Per_Sec NUMERIC,
    Percentage_of_Global_Traffic FLOAT,
    Last_Updated DATETIME DEFAULT CURRENT_TIMESTAMP
);