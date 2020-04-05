import os.path
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT
from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser

class WSearch():
    def __init__(self, storage_location = "app//main_page_module//data//"):
        
        self.storage_location = storage_location
        
    def index_create(self):
        
        schema = Schema(file_name=TEXT(stored=True), content=TEXT(stored=True))
        
        if not os.path.exists(".index"):
            os.mkdir(".index")
            
        ix = create_in(".index", schema)
        
        files = []
        # r=root, d=directories, f = files
        for _, _, f in os.walk(self.storage_location):
            for file in f:
                if '.txt' in file:
                    files.append(os.path.join(self.storage_location, file))
                    
        
        writer = ix.writer()
        
        for f in files:
            with open(f'{f}', 'r') as file:
                data = file.read().replace('\n', '')
                
                writer.add_document(file_name=u"{}".format(f), content=u"{}".format(data))                
            #print(f)
            
        writer.commit()

    def index_search(self,querystring):
        
        ix = open_dir(".index")
        
        parser = QueryParser("content", ix.schema)
        myquery = parser.parse(querystring)
        
        file_names = []
        with ix.searcher() as searcher:
            results = searcher.search(myquery)
            print(f"Found {len(results)} results.")
            for found in results:
                file_names.append([found["file_name"], found.highlights("content")])
                #print(found.highlights("content"))
            
            return file_names
        
        