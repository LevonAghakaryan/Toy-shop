# Իմպորտներ
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from starlette.responses import HTMLResponse
# Մոդուլների router-ների ներմուծում
from .modules.products.presentation.router import router as products_router
from .modules.category.presentation.router import router as category_router
from .modules.orders.presentation.router import router as orders_router
from .modules.cart.presentation.router import router as cart_router
from .modules.admin.presentation.router import router as admin_router
app = FastAPI(title="FOODMARKET")

# Static ֆայլերի միացում
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")
templates = Jinja2Templates(directory="templates")
app.state.templates = templates
# UI-ի համար պարզ էջեր
@app.get("/", include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Մեր Մենյուն"})

@app.get("/products/all_products", include_in_schema=False)
async def products_page(request: Request):
    return templates.TemplateResponse("products/products.html", {"request": request, "title": "Մեր Մենյուն"})



@app.get("/aboutus",include_in_schema=False)
async def about(request: Request):
    return templates.TemplateResponse("aboutus/aboutus.html", {"request": request, "title": "Մեր մասին"})

@app.get("/cart", include_in_schema=False)
async def cart_page(request: Request):
    """
    Բեռնում է cart.html էջը և ցուցադրում զամբյուղի պարունակությունը։
    """
    return templates.TemplateResponse("order_cart/cart.html", {"request": request, "title": "Զամբյուղ"})

# ԲԼՈԳԻ ԷՋԻ ՌՈՈՒՏԵՐ
@app.get("/blog", response_class=HTMLResponse)
async def blog_page(request: Request):
    # Վերադարձնում է blog.html-ը
    return templates.TemplateResponse("blog/blog.html", {"request": request})

# ԱԿՑԻԱՆԵՐԻ ԷՋԻ ՌՈՈՒՏԵՐ
@app.get("/akcianer", response_class=HTMLResponse)
async def actions_page(request: Request):
    # Վերադարձնում է actions.html-ը
    return templates.TemplateResponse("akcianer/akcianer.html", {"request": request})

@app.get("/kap", include_in_schema=False)
async def contact_page(request: Request):
    """
    Բեռնում է kap.html էջը (Կապ մեզ հետ)։
    """
    # Ձեր template-ների կառուցվածքից ելնելով, ենթադրում եմ, որ այն կլինի templates/kap/kap.html
    return templates.TemplateResponse("kap/kap.html", {"request": request, "title": "Կապ Մեզ Հետ"})

# API Router-ների միացում
app.include_router(products_router)
app.include_router(category_router)
app.include_router(orders_router)
app.include_router(cart_router)
app.include_router(admin_router)
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
