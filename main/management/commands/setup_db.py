import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Setup database (makemigrations + migrate + seed)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete database before setup"
        )

    def handle(self, *args, **options):
        db_path = settings.BASE_DIR / "db.sqlite3"

        # 🧨 Optional reset
        if options["reset"]:
            if os.path.exists(db_path):
                self.stdout.write(self.style.WARNING("🧨 Deleting existing database..."))
                os.remove(db_path)
            else:
                self.stdout.write("ℹ️ No database file found, skipping delete.")

        # 🆕 MAKE MIGRATIONS
        self.stdout.write("🛠️ Making migrations...")
        call_command("makemigrations")

        # 📦 APPLY MIGRATIONS
        self.stdout.write("📦 Applying migrations...")
        call_command("migrate")

        # 🌱 SEED DATA
        self.stdout.write("🌱 Seeding database...")
        call_command("seed_data")

        # ✅ DONE
        self.stdout.write(self.style.SUCCESS("✅ Database setup complete!"))