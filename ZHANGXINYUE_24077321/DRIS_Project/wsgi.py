import os
import sys

# 获取项目根目录路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)  # 确保在路径最前面

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRIS_Project.settings')

# 导入 WSGI 应用
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()