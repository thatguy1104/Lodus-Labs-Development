SELECT [Name_]
      , [Current_Players]
      , [Peak_Today]
      , [Hours_Played]
      , [Last_Updated]
FROM [dbo].[steam_concurrentGames]
ORDER BY Current_Players DESC