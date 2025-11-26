
import uvicorn
from app.core.database import Base, engine
from app.modules.cart.domain import models
from app.modules.products.domain import models
from app.modules.category.domain import models
from app.modules.orders.domain import models
from app.modules.users.domain import models
if __name__ == "__main__":
    # Աղյուսակները ստեղծելու/թարմացնելու համար (միայն զարգացման փուլում)
    # Խորհուրդ է տրվում օգտագործել Alembic արտադրական միջավայրում
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully (Development mode).")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")


    # Uvicorn-ի միջոցով հավելվածի գործարկում
    print("🚀 Starting Uvicorn server...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)