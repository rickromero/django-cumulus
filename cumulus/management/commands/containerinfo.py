import cloudfiles, optparse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Display info for cloud files containers"

    option_list = BaseCommand.option_list + (
        optparse.make_option('-n', '--name', action='store_true', dest='name', default=False),
        optparse.make_option('-c', '--count', action='store_true', dest='count', default=False),
        optparse.make_option('-s', '--size', action='store_true', dest='size', default=False),
        optparse.make_option('-u', '--uri', action='store_true', dest='uri', default=False)
    )

    def handle(self, *args, **options):
        USERNAME = getattr(settings, 'CUMULUS_USERNAME')
        API_KEY = getattr(settings, 'CUMULUS_API_KEY')
        
        conn = cloudfiles.get_connection(USERNAME, API_KEY)
        if args:
            try:
                container = conn.get_container(args[0])
            except cloudfiles.errors.NoSuchContainer:
                raise CommandError("Container does not exist: %s" % args[0])
            containers = [container]
        else:
            containers = conn.get_all_containers()
        
        opts = ['name', 'count', 'size', 'uri']
        
        for container in containers:
            info = {
                'name': container.name,
                'count': container.object_count,
                'size': container.size_used,
                'uri': container.public_uri(),
            }
            output = [str(info[o]) for o in opts if options.get(o)]
            if not output:
                output = [str(info[o]) for o in opts]
            print ', '.join(output)
        
        if not containers:
            print 'No containers found.'