DROP TABLE IF EXISTS steam_concurrentGames
CREATE TABLE steam_concurrentGames
(
    Name_ NVARCHAR,
    Current_Players BIGINT,
    Peak_Today BIGINT,
    Hours_Played BIGINT,
    Last_Updated DATETIME
);