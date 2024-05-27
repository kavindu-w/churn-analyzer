from h2o_wave import ui, site
from src.common import utils

async def home_page_impl(q:dict, details: dict) -> dict:
    header = []
    
    items = []
    
    cfg = {
        "tag": "home",
        "items": items,
        "header": header
    }
    
    return cfg