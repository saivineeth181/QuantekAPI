import json

from bs4 import BeautifulSoup
from bs4 import element
from fastapi import FastAPI,Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class scrapy:
    def __init__(self):
        self.tag_list = {}
        self.data = []
    
    def process(self,doc):
        try:
            for tag in doc.children:
                if isinstance(tag,element.Tag):
                    self.tag_list[tag] = self.tag_list.get(tag,0) + 1
                    self.process(tag)
        except:
            raise HTTPException(status_code=404, detail="Please give valid input")
    
    def dict2data(self):
        self.tag_list = {k: v for k, v in sorted(self.tag_list.items(), key=lambda item: item[1],reverse=True)}
        for i in self.tag_list.keys():
            if self.tag_list.get(i) > 1 :
                tag = {}
                tag["tag"] = str(i)
                tag["tag_name"] = str(i.name).upper()
                tag["count"] = self.tag_list.get(i)
                self.data.append(tag)


@app.post("/post")
def post(html_doc:str):
    doc = BeautifulSoup(html_doc,'html.parser')
    s = scrapy()
    s.process(doc.body)
    s.dict2data()
    data = json.dumps(s.data)
    return Response(content=data,media_type="application/html")

