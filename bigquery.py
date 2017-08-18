from google.cloud import bigquery




def run_query_sql(query, auth):
    client=bigquery.Client.from_service_account_json(auth)
    query_results = client.run_sync_query(query)

    query_results.run()

    rows = query_results.fetch_data(max_results=20)
    
    for row in rows:
        print("{}       {}".format(row[0],row[1]))
        # print(row)
        
def package_downloads(name,auth):
    query="""
SELECT  
  file_version,
  SUM(total_downloads) as downloads
FROM [python-vanity-test:Download_Data.file_counts]
WHERE
  file_project='{}'
GROUP BY
  file_version 
ORDER BY
  file_version
""".format(name)
    run_query_sql(query, auth)

# Replace 'Python Vanity Test-125254b19f45.json' with own credentials 
if __name__ == '__main__':
    package_downloads("vanity",'Python Vanity Test-125254b19f45.json')