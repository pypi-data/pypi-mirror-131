import os
import sys
from pathlib import Path


def init_run(application_name='application'):
    sys.path.insert(0, str(Path(__file__).parent.parent))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{application_name}.settings')
    import django
    django.setup()
