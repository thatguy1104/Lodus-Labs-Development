DROP TABLE IF EXISTS all_games_all_data;
CREATE TABLE all_games_all_data(
        name_       CHAR(200),
        ids         CHAR(200),
        months          text[][],
        avg_players     float[],
        gains           float[],
        percent_gains   text[][],
        peak_players    integer[]
);