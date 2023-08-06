from dynaconf import Dynaconf
from .common import constant, common
import os


default_settings = {'name': '未定义的name', 'test_tags': [], 'test_case': 'all', 'is_debug': False, 'process_num': 1,
                    'tag_list': {'all': '其他'}, 'is_locust': False}
settings = Dynaconf(envvar_prefix=False, merge_enabled=True, environments=True, load_dotenv=True,
                    env_switcher="ENV", root_path=constant.CONFIG_FOLDER, includes=['*.toml'])
if settings.exists('run'):
    settings.set('run', {})
for key, value in default_settings.items():
    if key not in settings.run:
        setattr(settings.run, key, value)
