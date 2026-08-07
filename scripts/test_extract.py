import pymupdf

pdf = pymupdf.open("data/cvs/Md Tasfiq Kamran.pdf")

text = ""
links = ""

for page in pdf:
    text += page.get_text()

    links = page.get_links()
    for 

print(text)
for link in links:
    print(link['uri'])