from h2o_wave import Q, app, main, run_on, ui
from loguru import logger

from src.pages.home_page import home_page_impl
logger.add(
    "./logs/debug.log",
    level='DEBUG',
    backtrace=False,
    rotation='5 MB',
    compression='zip',
)
logger.add(
    "./logs/error.log",
    rotation='5 MB',
    compression='zip',
    backtrace=True,
)

@app('/')
async def serve(q: Q):
    try:
        if not q.client.initialized:
            if q.user.config is None:
                q.user.config = {
                    "app_title": "Churn Analyzer",
                    "sub_title": "Analyze your churn data with ease!",
                    "footer_text": 'This application is built using H2O Wave',
                }
            q.client.initialized = True

        #handlers
        await home_page(q, {"flag": "about"})

    except Exception as e:
        logger.exception(e)
        q.page["meta"].notification_bar = ui.notification_bar(
            title="Error occured",
            type="error",
            name="error_bar"
        )
    await q.page.save()


def create_layout(q: Q, tag=None):
    config = q.user.config
    q.page.drop()
    
    q.page["header"] = ui.header_card(
        box=ui.box(
            "header",
            order=2,
        ),
        title=config["app_title"],
        subtitle=config["sub_title"],
        # image="",
    )

    q.page["footer"] = ui.footer_card(box="footer", caption=config["footer_text"])
    zones = [ui.zone(name="content_0", size="840px", direction="row")]
    if tag in ["home"]:
        zones = [
            ui.zone(
                name="content_0",
                direction="row",
                zones=[
                    ui.zone(name="content_01", size='10%', direction="row"), 
                    ui.zone(
                        name="content_02",
                        size='90%',
                    ),
                ],
            ),
        ]

    else:
        pass
    
    q.page["meta"] = ui.meta_card(
        box="",
        # theme = "light",
        title= config["app_title"] + " | Kavindu Warnakulasuriya",
        layouts=[
            ui.layout(
                breakpoint="xs",
                zones=[
                    ui.zone(name="header",size="80px",),
                    ui.zone(name="content", zones=zones),
                    ui.zone("footer",size="79px",),
                ]
                
            )
        ],
    )

async def render_template(q: Q, page_cfg):
    create_layout(q, tag=page_cfg["tag"])
    
    
    if page_cfg["tag"] == "home":
        q.page["content_left"] = ui.nav_card(
            box=ui.box(zone="content_01", height='840px', width="100%", order=1),
            title="",
            value=page_cfg["flag"],
            items=page_cfg["items"],
        )
        if page_cfg["flag"] in ["about"]:
            q.page["content_02"] = ui.form_card(
                box=ui.box(zone="content_02",  width="100%", order=1),
                title="",
                items=page_cfg["items"],
            )
        else:
            pass


    else:
        pass
    
    await q.page.save()

# page handlers
async def home_page(q: Q, details: dict):
    cfg = await home_page_impl(q, details)
    await render_template(q, cfg)
