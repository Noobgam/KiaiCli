from noobgam.caches.common import set_profile, discard_caches, get_profile
from noobgam.subcommands.subcommand import SubCommand


class ProfileSwitcher(SubCommand):
    def __init__(self):
        self.name = 'profile'

    def do(self, line: str):
        if not line or line == 'show':
            profile, region = get_profile()
            self.kiai.print(f'Using {profile} {region}\n')
            return
        parts = line.split(' ')
        if len(parts) == 2:
            profile, region = parts
        elif len(parts) == 1:
            profile = parts[0]
            region = 'us-east-1'
        else:
            raise ValueError('Unrecognized format')
        set_profile(profile=profile, region=region)
        discard_caches()
        # todo: validate
        self.kiai.print(f'switched to {profile} {region}\n')
        return {
            'profile': profile,
            'region': region
        }

    def complete(self, text, line, start_index, end_index):
        pass
