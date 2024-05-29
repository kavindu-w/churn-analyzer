from h2o_wave import ui, site
# from src.common import utils

async def home_page_impl(q:dict, details: dict) -> dict:
    about = [

    ]
    items = [

    ]
    
    cfg = {
        "tag": "home",
        "items": items,
        "about": about
    }
    
    return cfg