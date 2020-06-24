SELECT TOP (1000)
      [Month]
      , [Year_]
      , [name_]
      , [ids]
      , [avg_players]
      , [gains]
      , [percent_gains]
      , [peak_players]
      , [Last_Updated]
FROM [dbo].[steam_all_games_all_data]
ORDER BY Year_ DESC