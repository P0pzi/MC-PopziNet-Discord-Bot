STRIKES_TIMEOUT = 3  # warnings before mute
MUTE_SECONDS_INCREMENTS = 300  # Seconds increments between each mute, 1st mute = x1, 2nd mute = x2.. etc


class Strike:
    def __init__(self, discord_user_id: int) -> None:
        self.discord_user_id = discord_user_id
        self.strikes = 0
        self.mutes = 0

    def strike(self) -> bool:
        self.strikes += 1
        return self.strikes > STRIKES_TIMEOUT

    @property
    def next_mute_time(self):
        return (self.mutes + 1) * MUTE_SECONDS_INCREMENTS


class StrikeModule:
    strikes = {}

    def strike(self, discord_user_id) -> bool:
        person = self.get(discord_user_id)
        self.strikes[discord_user_id] = person
        should_mute = person.strike()

        if should_mute:
            person.mutes += 1
            person.strikes = 0
            return True
        return False

    def get(self, discord_user_id):
        return self.strikes.get(discord_user_id, Strike(discord_user_id))
