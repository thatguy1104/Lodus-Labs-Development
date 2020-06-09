DROP TABLE IF EXISTS static_data;
CREATE TABLE static_data(
    appid               INT,
    name_               CHAR(300),
    release_date        CHAR(300),
    english             INT,
    developer           CHAR(300),
    publisher           CHAR(300),
    platforms           CHAR(300),
    required_age        INT,
    categories          CHAR(300),
    genres              CHAR(300),
    steamspy_tags       CHAR(300),
    achievements        CHAR(300),
    positive_ratings    INT,
    negative_ratings    INT,
    average_playtime    FLOAT,
    median_playtime     INT,
    owners              CHAR(300),
    price               FLOAT
);

COPY static_data(appid,name_,release_date,english,
            developer,publisher,platforms,required_age,
            categories,genres,steamspy_tags,achievements,
            positive_ratings,negative_ratings,average_playtime,
            median_playtime,owners,price
) 
FROM '/Users/albert.ov11/Desktop/PROJECT/STEAM/Static Data Files/steam.csv' DELIMITER ',' CSV HEADER;