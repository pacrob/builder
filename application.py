from app import create_app
from config import ProductionConfig

application = create_app(ProductionConfig)
