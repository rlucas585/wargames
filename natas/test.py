import requests as req

r = req.get('https://www.ncbi.nlm.nih.gov/pubmed/')

print (r.text)
