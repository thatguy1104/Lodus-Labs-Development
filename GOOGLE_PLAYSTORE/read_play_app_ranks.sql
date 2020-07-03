SELECT TOP (1000)
  [Developer]
      , [App_Name]
      , [App_Rank]
      , [Total_Rating]
      , [Installs]
      , [Average_Rating]
      , [Growth_30_days_Percent]
      , [Growth_60_days_Percent]
      , [Price]
      , [Last_Updated]
FROM [dbo].[play_app_ranks]
ORDER BY App_Rank, Last_Updated ASC
