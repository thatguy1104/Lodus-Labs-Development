SELECT [Country]
      , [Total_Bytes]
      , [Avg_MB_Per_Sec]
      , [Percentage_of_Global_Traffic]
      , [Last_Updated]
FROM [dbo].[steam_network_data]
ORDER BY Total_Bytes DESC