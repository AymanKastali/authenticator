import uvicorn

from presentation.web.fastapi.app import create_app
from presentation.web.fastapi.config import get_app_config

app_cfg = get_app_config()


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host=app_cfg.host, port=app_cfg.port, reload=app_cfg.debug)
