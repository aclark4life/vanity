import requests

def site_query(package_name,options=None):
    # outputs package download
    query=requests.get(generate_url(package_name,options))
    return parse_data(query.text)
    
def generate_url(package_name,options):
    site="pythonpackages.com/api"
    url=site+""
    return url
        
def parse_data(data):
    
    return 1







# def vanity(package, verbose=True):
#     """Parse args, verify package, retrieve details, return download count."""
 
#     if package.find('==') >= 0:package, version = package.split('==')
#     # try:package = normalize(package)
#     # except ValueError:
#     #     logger.debug('No such module or package %r', package)
#     #     continue
#     # Count downloads
#     total = count_downloads(package)
#     if total != 0:
#         if version:logger.debug('%s %s has been downloaded %s times!',
#                          package, version, locale.format("%d",total,grouping=True))
#         else:logger.debug('%s has been downloaded %s times!',
#                          package, locale.format("%d",total,grouping=True))
#     else:
#         if version:logger.debug('No downloads for %s %s.', package, version)
#         else:logger.debug('No downloads for %s.', package)

# def vanity(package):
#     count=0
#     items=[]
#     downloads=site_query(package,options=None)
#     if downloads==[]:
#         logger.debug('No such module or package %r', package)
#     for version_count in downloads:
#         items.append('%s    %9s' % (version_count[0], version_count[1]))
#         count += version_count[1]
#     longest = len(max(items, key=len))
#     for item in items:
#         logger.debug(item.rjust(longest))
#     if items!=[]:
#         logger.debug('-' * longest)
#         logger.debug('%s has been downloaded %s times!')
        



    

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description=__doc__)
#     parser.add_argument('package', help='pypi package name', nargs='+')
#     # parser.add_argument('-q',
#     #                     '--quiet',
#     #                     help='only show total downloads',
#     #                     action='store_true')
#     # parser.add_argument('-p',
#     #                     '--pattern',
#     #                     help='only show files matching a regex pattern')
#     args = parser.parse_args()

#     vanity(packages=args.package,
#           verbose=not (args.quiet))

from google.cloud import bigquery

def run_query_sql(query, auth):
    r=[]
    client=bigquery.Client.from_service_account_json(auth)
    query_results = client.run_sync_query(query)

    query_results.run()

    rows = query_results.fetch_data(max_results=20)
    for row in rows:
        r+=[[row[0],row[1]]]
    return r
        
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
    return run_query_sql(query, auth)

def vanity(package):
    count=0
    items=[]
    downloads=package_downloads(package,'Python Vanity Test-125254b19f45.json')
    if downloads==[]:
        print('No such module or package %r', package)
    for version_count in downloads:
        items.append('%s    %9s' % (version_count[0], version_count[1]))
        count += version_count[1]
    longest = len(max(items, key=len))
    for item in items:
        print(item.rjust(longest))
    if items!=[]:
        print('-' * longest)
        print('%s has been downloaded %s times!' % (package, count))
    
# Replace 'Python Vanity Test-125254b19f45.json' with own credentials 
if __name__ == '__main__':
    vanity('vanity')
    
