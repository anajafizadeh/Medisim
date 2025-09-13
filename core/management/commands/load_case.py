from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from core.models import Case
from pathlib import Path
import yaml

class Command(BaseCommand):
    help = 'Load a YAML case file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('yaml_path', type=str)
        parser.add_argument('--creator-email', type=str, default=None)

    def handle(self, *args, **opts):
        p = Path(opts['yaml_path'])
        if not p.exists():
            raise CommandError(f"File not found: {p}")
        blob = p.read_text()
        data = yaml.safe_load(blob)
        title = data.get('title', p.stem)
        rubric_id = data.get('rubric_id', 'rubric_default')
        user_model = get_user_model()
        creator = None
        if opts['creator_email']:
            creator = user_model.objects.filter(email=opts['creator_email']).first()
        case = Case.objects.create(title=title, specialty=data.get('specialty',''), difficulty=data.get('difficulty',''), yaml_blob=blob, rubric_id=rubric_id, created_by=creator)
        self.stdout.write(self.style.SUCCESS(f"Loaded case '{case.title}' (id={case.id})"))