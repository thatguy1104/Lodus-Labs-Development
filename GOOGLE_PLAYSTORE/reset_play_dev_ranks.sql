DROP TABLE IF EXISTS dbo.play_dev_ranks;
CREATE TABLE play_dev_ranks
(
    Rank INT,
    Developer NVARCHAR(200),
    Total_Ratings BIGINT DEFAULT 0,
    Total_Installs BIGINT DEFAULT 0,
    Applications INT DEFAULT 0,
    Average_Rating FLOAT DEFAULT 0.0,
    Link VARCHAR(200),
    Last_Updated DATETIME
);