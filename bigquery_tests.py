from google.cloud import bigquery
import inspect
# export GOOGLE_APPLICATION_CREDENTIALS=/PythonVanityTest-4073c8620c48.json
# print(inspect.getsource(bigquery.Client))

# json_account_data={
#   "type": "service_account",
#   "project_id": "python-vanity-test",
#   "private_key_id": "4073c8620c481cad13b2e82a1989af3a0c891523",
#   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC4+1AilaO0ILaW\nUOq1NnGVNvSHInD3uq9kL3W7UmP4GuT7BcOFhHefgqweRLkneSzjg0KfidbnQPUh\nmgbrkWZaglByyNyhpxj1NXXGZ94A+0aXRpInw3B3r2MlZiyKEv56q4HeZQuBn2fH\nKLM1tIwqO3dQJ1Qpj00hQcmxWbv2fVFERXptMn8ZaNE3vVxZoYpa4VEEGVo4cqfq\nSgaNe8lLdDY5vl6j+Rk3XyABhNykLMKQIaf5jbh4dZXedCOPS/oJUrPkOQ9TlrQ/\n9fZWCJxi5CN3pjIMxWhUKnnxpCTAIQIOS6wlHHa6QcTiCeriDLHFZ/MdWC+96u95\nZxlxZNXPAgMBAAECggEALlZ+F3vGu1uqgXMZqHVP9KIElUlyZQw13XHqGxejhUYv\ncBZciTjKwoF4Xki23QWE0iVSbiaYV+u0vEsaSq5spmWYg3h/lFsIbHyM2TuxqCtJ\n3qFGAYH6zXB49KhopdnmN5J5AN3tCPaGh6RRaDWnGvk0hTak5ZhJKPiS7sNcy3zh\nAeClx43tsbj3uwPrwZzy6GRLaAWOQGHr2NojNli3ycPa1/5JZ7o+AZ8StF7ZjcSr\nIyAouV7j0VcgzXoLClWDnzptdtL45Z1XHy6SGq1LPRd+ly8Y/af+vjvoauDfaaSX\noHC4v3zokSDbfjc89wv2IGagPcrRCo0C8DIk5e8F+QKBgQD4TWQIot33NW4HM5MA\nxE5E7skCerSzrl1EURjV2nSVboVDxvhZpplkQrkXSoHmgMLSlyWaG2r2zxG683hQ\ng9caNid9FQ9VhBh5/Jt75pRjJbK8n19Kwx947yaq+qxU4pCodMDTwlPRh4BElfoA\nBx6VNNwYu486CEi0WCDBthk5iwKBgQC+t2OQEejKcw5eG9+HFMK93KF4nm30pg5G\nWS5B9DHhUZA82QTHCUL81CJ7Pi8LtdGO69mkNn69eqAvPRYbbKCNeqinXB9MTZw/\n1mPkb85zDdbiyaewrsnXSIfkQNiO0QrJY8Utjge4dK3P9rEDEU5ePTvNFvdOemSQ\n+C8zScZ1TQKBgQDexhidAvrg4+gOwAABLR8IC7D+73aWyzbUp2n/3JrCw0D/eVGy\npZ1z7cVAl1GKrDWfWYqcBENooonG0NA+dLsVwkaVm8KBOB35vGEHve2eMuF1CAwn\n+H6RMwffWT4qfofJC89BblVjZQ34+xIs2jZfKejaq9Sp/Wq1m2fwRF/HVwKBgFnf\nykeGaRGejtLCh9/8ZJlcc6uH3YFBD9EPDcF+9lKcQUCrdJjnQG4s+eLiNwFpuUuE\n0ZeVJrzcIMiiHNznn/GMMBZOT2GB4XQj8AciuUN27iEJrsCQXgXZ5FAoTuVelZq6\nLZ1+JR1DvvUV5+zuJuQ6LwhDHmAZRXMbwgKFbcSxAoGANF5efSm7AgwJAkpWZ/MW\njaNWYimh+xIW481/qfUmSU7ibmXv0yYcDqCpZT6+lOKYVn2gf67JXt779duQTya8\nBnJR6AFIJKSLpQwxZlW5XiuqM8olk84WA3ZCkgrJvhuv8wg3rIjRNmiJswBFPpeX\nWtsrB1y71vA9ifBxDjL56fA=\n-----END PRIVATE KEY-----\n",
#   "client_email": "python-vanity-test@appspot.gserviceaccount.com",
#   "client_id": "110771443544420869463",
# #   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
# #   "token_uri": "https://accounts.google.com/o/oauth2/token",
# #   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
# #   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/python-vanity-test%40appspot.gserviceaccount.com"
# }



def query_shakespeare():
    client=bigquery.Client.from_service_account_json("PythonVanityTest-4073c8620c48.json")
    query_results = client.run_sync_query("""
        SELECT
            APPROX_TOP_COUNT(corpus, 10) as title,
            COUNT(*) as unique_words
        FROM `publicdata.samples.shakespeare`;""")

    # Use standard SQL syntax for queries.
    # See: https://cloud.google.com/bigquery/sql-reference/
    query_results.use_legacy_sql = False

    query_results.run()

    rows = query_results.fetch_data(max_results=10)

    for row in rows:
        print(row)



def query_test1():
    client=bigquery.Client.from_service_account_json("PythonVanityTest-4073c8620c48.json")
    query_results = client.run_sync_query("""
        SELECT
  REGEXP_EXTRACT(details.python, r"^([^\.]+\.[^\.]+)") as python_version,
  COUNT(*) as download_count,
FROM
  TABLE_DATE_RANGE(
    [the-psf:pypi.downloads],
    DATE_ADD(CURRENT_TIMESTAMP(), -31, "day"),
    DATE_ADD(CURRENT_TIMESTAMP(), -1, "day")
  )
WHERE
  file.project = 'cryptography'
GROUP BY
  python_version,
ORDER BY
  download_count DESC
LIMIT 100
;""")

    # Use standard SQL syntax for queries.
    # See: https://cloud.google.com/bigquery/sql-reference/
    # query_results.use_legacy_sql = False

    query_results.run()

    rows = query_results.fetch_data(max_results=10)

    for row in rows:
        print(row)

def query_test2():
    client=bigquery.Client.from_service_account_json("PythonVanityTest-4073c8620c48.json")
    query_results = client.run_sync_query("""
SELECT
  file.filename,
  COUNT(*) as total_downloads,
FROM
  TABLE_DATE_RANGE(
    [the-psf:pypi.downloads],
    DATE_ADD(CURRENT_TIMESTAMP(), -31, "day"),
    DATE_ADD(CURRENT_TIMESTAMP(), -1, "day")
  )
WHERE
  file.project = 'cryptography'
AND
  file.filename like '%1.6%'
GROUP BY
  file.filename
ORDER BY
  total_downloads DESC
LIMIT 100
;""")

    # Use standard SQL syntax for queries.
    # See: https://cloud.google.com/bigquery/sql-reference/
    # query_results.use_legacy_sql = False

    query_results.run()

    rows = query_results.fetch_data(max_results=10)

    for row in rows:
        print(row)

    

def run_query_sql(query):
    client=bigquery.Client.from_service_account_json("PythonVanityTest-4073c8620c48.json")
    query_results = client.run_sync_query(query)

    query_results.run()

    rows = query_results.fetch_data(max_results=10)

    for row in rows:
        print(row)
        
def package_downloads(name):
    query="""
SELECT
  file.filename,
  COUNT(*) as total_downloads,
FROM
  TABLE_DATE_RANGE(
    [the-psf:pypi.downloads],
    DATE_ADD(CURRENT_TIMESTAMP(), -31, "day"),
    DATE_ADD(CURRENT_TIMESTAMP(), -1, "day")
  )
WHERE
  file.project = '{}'
GROUP BY
  file.filename,
ORDER BY
  total_downloads DESC
LIMIT 100
""".format(name)
    run_query_sql(query)

    
    
    
# Doesn't print on time spans about ~200-300
query1="""SELECT
  file.filename,
  COUNT(*) as total_downloads,
FROM
  TABLE_DATE_RANGE(
    [the-psf:pypi.downloads],
    DATE_ADD(CURRENT_TIMESTAMP(), -356, "day"),
    DATE_ADD(CURRENT_TIMESTAMP(), -300, "day")
  )
WHERE
  file.project = 'django'
AND
  file.filename like '%1.6%'
GROUP BY
  file.filename,
ORDER BY
  total_downloads DESC
LIMIT 100
"""

query2="""SELECT
  *
FROM
  TABLE_DATE_RANGE(
    [the-psf:pypi.downloads],
    DATE_ADD(CURRENT_TIMESTAMP(), -31, "day"),
    DATE_ADD(CURRENT_TIMESTAMP(), -1, "day")
  )
WHERE
  file.project = 'django'
AND
  file.filename like '%1.6%'
LIMIT 100
"""


# import os
# print(os.listdir(os.getcwsd()))
if __name__ == '__main__':
    # run_query_sql(query1)
    package_downloads("vanity")
    


# print('{} {}'.format('one', 'two'))


