from django.core.management.base import BaseCommand
from prettytable import PrettyTable

from bc.channel.models import Channel
from bc.channel.utils.masto import get_mastodon


class Command(BaseCommand):
    help = "Post something manually to one or more channels."

    def handle(self, *args, **options):
        tab = PrettyTable()
        channel_mapping = {}
        tab.field_names = ["ID", "Service", "Account", "Enabled", "URL"]
        db_channels = Channel.objects.all()
        for channel in db_channels:
            tab.add_row(
                [
                    channel.id,
                    channel.service,
                    channel.account,
                    channel.enabled,
                    channel.self_url(),
                ]
            )
            channel_mapping[channel.id] = channel
        self.stdout.write(self.style.SUCCESS(tab))

        channel_input = input(
            "Which channels? Input ID, comma-separate for multiple, or 'all' for all of them.\n"
        )
        self.stdout.write(self.style.SUCCESS(channel_input))

        channel_ids = None
        if channel_input == "all":
            channel_ids = list(channel_mapping.keys())
        else:
            channel_ids = list(
                map(int, [s.strip() for s in channel_input.split(",")])
            )

        self.stdout.write(
            self.style.SUCCESS(f"Posting to channels: {channel_ids}")
        )

        post_text = input("What do you want to say? ")

        for chid in channel_ids:
            channel = channel_mapping.get(chid)
            if channel is None:
                raise ValueError(f"No channel {chid}")

            if channel.service == "mastodon":

                self.stdout.write(
                    self.style.SUCCESS(f"Let's toot from {channel.account}!")
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Here's what we're going to say:\n\t{post_text}"
                    )
                )

                m = get_mastodon()
                m.status_post(post_text)
            else:
                raise NotImplementedError(
                    f"Not posting to {channel.service} yet"
                )
