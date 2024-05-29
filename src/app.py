from h2o_wave import Q, app, main, run_on, ui
from loguru import logger
from datetime import datetime

from src.pages.home_page import home_page_impl
from src.pages.analyze_page import analyze_page_impl


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
        logger.debug(f"Request: {q.args}")
        if not q.client.initialized:
            if q.user.config is None:
                q.user.config = {
                    "app_title": "Churn Analyzer",
                    "sub_title": "Analyze your churn data with ease!",
                    "footer_text": f'This application is built using H2O Wave | Copyright © {datetime.now().year} Kavindu Warnakulasuriya',
                }
            q.client.initialized = True

        #handlers
        if q.args.tab == "home":
            await home_page(q, {"flag": "home"})
        elif q.args.tab == "analyze":
            await analyze_page(q, {"flag": "analyze"})
        elif q.args.button_analyze_data:
            await analyze_page(q, {"path": "data/Bank Customer Churn Prediction.csv"})
        else:
            # await analyze_page(q, {"flag": "analyze"})
            await home_page(q, {"flag": "home"})

    except Exception as e:
        logger.exception(e)
        q.page["meta"].notification_bar = ui.notification_bar(
            text="Error occured, please try again later",
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
        image="https://img.icons8.com/?size=100&id=92028&format=png&color=000000",
        secondary_items=[
            ui.tabs(
                name="tab",
                items=[
                    ui.tab(name="home", label="Home", icon="Home"),
                    ui.tab(name="analyze", label="Analyze", icon="Financial"),
                ],
                value=q.client.tab or "home",
            )        
        ]
    )

    q.page["footer"] = ui.footer_card(box="footer", caption=config["footer_text"])
    zones = [ui.zone(name="content_0", size="840px", direction="row")]
    if tag == "home":
        zones = [
            ui.zone(
                name="content_0",
                direction="row",
                zones=[
                    ui.zone(name="content_01", size='30%', direction="row"), 
                    ui.zone(
                        name="content_02",
                        size='70%',
                    ),
                ],
            ),
        ]
    elif tag == "analyze":
        zones = [
            ui.zone(
                name="content_0",
                direction="column",
                zones=[
                    ui.zone(name="content_01", direction="row"), 
                    ui.zone(
                        name="content_02",
                        direction="row",
                        zones=[
                            ui.zone(name="content_021", size='50%', direction="row"),
                            ui.zone(name="content_022", size='50%', direction="row"),
                        ],
                    ),
                    ui.zone(name="content_03", direction="row"), 
                    ui.zone(name="content_04", direction="row"), 
                    ui.zone(name="content_05", direction="row")
                    
                    
                ],
            ),
        ]
    else:
        pass
    
    q.page["meta"] = ui.meta_card(
        box="",
        theme = "lighting",
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
        q.page["content_01"] = ui.form_card(
            box=ui.box(zone="content_01", width="100%", height="680px"),
            title="",
            items=page_cfg["items"],
        )
        q.page["content_02"] = ui.form_card(
            box=ui.box(zone="content_02",  width="100%", height="100%"),
            title="",
            items=page_cfg["about"],
        )
    elif page_cfg["tag"] == "analyze":
        q.page['content_011'] = ui.tall_stats_card(
            box=ui.box(zone="content_01", width="20%", order=1),
            items=page_cfg["stats_left"]
        )
        q.page["content_012"] = ui.form_card(
            box=ui.box(zone="content_01", width="100%", order=2),
            title="",
            items=page_cfg["stats_tables"],
        )
        q.page["content_021"] = ui.image_card(
            box=ui.box(zone="content_021",  width="100%",),
            title="",
            type="png",
            image=page_cfg["correlation_matrix"],
        )
        q.page["content_022"] = ui.image_card(
            box=ui.box(zone="content_022",  width="100%"),
            title="",
            type="png",
            image=page_cfg["missing_values"],
        )
        q.page["content_03"] = ui.image_card(
            box=ui.box(zone="content_03",  width="100%"),
            title="",
            type="png",
            image=page_cfg["categorical_plots"],
        )
        q.page["content_04"] = ui.image_card(
            box=ui.box(zone="content_04",  width="100%"),
            title="",
            type="png",
            image=page_cfg["numerical_plots"],
        )
        q.page["content_05"] = ui.image_card(
            box=ui.box(zone="content_05",  width="100%"),
            title="",
            type="png",
            image=page_cfg["histograms"],
        )

    else:
        pass
    
    await q.page.save()

# page handlers
async def home_page(q: Q, details: dict):
    cfg = await home_page_impl(q, details)
    await render_template(q, cfg)


async def analyze_page(q: Q, details: dict):
    cfg = await analyze_page_impl(q, details)
    await render_template(q, cfg)
