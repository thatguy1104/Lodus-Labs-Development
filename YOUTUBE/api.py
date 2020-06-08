from googleapiclient.discovery import build


api_key = '956133523530-e63bvbv9to2mk9hnj02ios490s3dhtd4.apps.googleusercontent.com'
service_name = 'youtubeAnalytics'
version = 'v2'

service = build(service_name, version, developerKey=api_key)

