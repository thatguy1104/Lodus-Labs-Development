SELECT [Country_Code]
      , [asname]
      , [totalbytes]
      , [avgmbps]
      , [Last_Updated]
FROM [dbo].[steam_provider_data]
ORDER BY avgmbps