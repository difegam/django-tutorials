from blog.models import Post
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Delete all posts"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Delete all posts without applying changes to the database",
        )

    def handle(self, *args, **options) -> None:
        dry_run = options["dry_run"]
        posts = Post.objects.all()
        count = posts.count()

        if dry_run:
            self.stdout.write(self.style.MIGRATE_LABEL("{:^50s}".format("Running in dry-run mode")))
            self.stdout.write(self.style.WARNING(f"Deleting {posts.count()} posts"))
            return

        posts.delete()

        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {count} posts"))
