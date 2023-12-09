from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from operator import itemgetter
from plotly.graph_objs import Bar
from plotly import offline

#Lists/Dics
author_quotes = {}
lengths = []
tag = {}

#Init
shortest = ''
low = 99999
longest = ''
high = 0

#Scrape
for number in range(1,10):
    url = f'https://quotes.toscrape.com/page/{number}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    
    req = Request(url, headers=headers)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    quotes = soup.findAll('div', class_ = 'quote')

    for box in quotes:
        q = box.findAll('span')
        quote = q[0].text
        author = q[1].text.split('by ')[1].split('\n')[0].strip()
        length = len(quote)

        if author in author_quotes:
            author_quotes[author] += 1
        else:
            author_quotes[author] = 1
        
        quote_length = len(quote)
        lengths.append(quote_length)

        if length < low:
            shortest = quote
            low = length
        
        if length > high:
            longest = quote
            high = length

    tags = soup.findAll('a', class_ = 'tag')
    if tags:
        for t in tags:
            text = t.text
            if text in tag:
                tag[text] += 1
            else:
                tag[text] = 1

#Author Stats
print("\nNumber of Quotes by Author:\n")
for author, total in author_quotes.items():
    print(f'{author}: {total} quotes')

most_quotes_name = ''
most_quotes = -1
for author, total in author_quotes.items():
    if total > most_quotes:
        most_quotes = total
        most_quotes_name = author

print(f"\nThe author quoted the most is {most_quotes_name} with {most_quotes} quotes")
    

least_quotes_name = ''
least_quotes = 999999
for author, total in author_quotes.items():
    if total < least_quotes:
        least_quotes = total
        least_quotes_name = author

print(f"\nThe author quoted the least is {least_quotes_name} with {least_quotes} quotes.")

#Quote Analysis
average = sum(lengths) / len(lengths)
print(f"\nThe average quote length is {average:.2f} characters.")

print(f"\nThe longest quote is {longest}. It is {len(longest)} characters long.")
print(f"\nThe shorest quote is {shortest}. It is {len(shortest)} characters long.\n")

#Tag Analysis
pop_tag = max(tag, key = tag.get)
max_ = 0

for t, count in tag.items():
    print(f'{t}: {count}')
    if count > max_:
        pop_tag = t
        max_ = count

total_tags = len(tag)

print(f"\nThe most popular tag is {pop_tag}.")
print(f"\nThere is {total_tags} tags being used across all quotes.\n")

#Top 10 Authors
topauth = list(author_quotes.items())
topauth = sorted(topauth, key = itemgetter(1), reverse = True)

auth_names, auth_totals = [], []
i = 0

for author in topauth[:10]:
    auth_names.append(topauth[i][0])
    auth_totals.append(topauth[i][1])
    i += 1

#Top 10 Tags
toptags = list(tag.items())
toptags = sorted(toptags, key = itemgetter(1), reverse = True)

tag_names, tag_totals = [], []
i = 0

for tag in toptags[:10]:
    tag_names.append(toptags[i][0])
    tag_totals.append(toptags[i][1])
    i += 1

#Author Chart
data = [
    {
        "type": "bar",
        "x": auth_names,
        "y": auth_totals,
        "marker": {
            "color": "rgb(100,0,0)",
            "line": {"width": 1.25, "color": "rgb(0,0,0)"},
        },
        "opacity":0.8,
    }
]

layout = {
    "title": "Top 10 Authors from the first 10 pages of quotes.toscrape.com",
    "xaxis": {"title": "Author"},
    "yaxis": {"title": "Quotes"},
}

chart = {"data": data, "layout": layout}

offline.plot(chart, filename = "top10authors.html")

#Tag Chart
data = [
    {
        "type": "bar",
        "x": tag_names,
        "y": tag_totals,
        "marker": {
            "color": "rgb(100,0,0)",
            "line": {"width": 1.25, "color": "rgb(0,0,0)"},
        },
        "opacity":0.8,
    }
]

layout = {
    "title": "Top 10 Tags from the first 10 pages of quotes.toscrape.com",
    "xaxis": {"title": "Tag"},
    "yaxis": {"title": "Times Used"},
}

chart2 = {"data": data, "layout": layout}

offline.plot(chart2, filename = "top10tags.html")