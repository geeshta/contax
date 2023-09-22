from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig

from server.env import PROJECT_ROOT

template_config = TemplateConfig(
    directory=PROJECT_ROOT / "server/templates", engine=JinjaTemplateEngine
)
