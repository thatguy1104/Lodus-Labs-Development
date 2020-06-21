SELECT TOP (1000)
    [Rank]
      , [Developer]
      , [Total_Ratings]
      , [Total_Installs]
      , [Applications]
      , [Average_Rating]
      , [Link]
      , [Last_Updated]
FROM [dbo].[play_dev_ranks]
ORDER BY Rank ASC