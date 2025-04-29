import eel
from search import get_results

eel.init("web")

@eel.expose
def search_query(query):
    return get_results(query, n=0)

eel.start("index.html", size=(1000, 600), mode='brave')

