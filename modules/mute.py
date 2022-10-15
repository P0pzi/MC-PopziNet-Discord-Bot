from datetime import datetime, timedelta


class MutedPerson:
    def __init__(self, discord_user_id: int) -> None:
        self.discord_user_id = discord_user_id
        self.unmuted_dt = None
        self.seconds_muted = 0

    def unmute(self):
        self.unmuted_dt = None
        self.seconds_muted = 0

    def mute(self, seconds):
        self.unmuted_dt = datetime.now() + timedelta(seconds=seconds)
        self.seconds_muted = seconds

    @property
    def is_muted(self):
        return self.unmuted_dt and self.unmuted_dt > datetime.now()


class MuteModule:
    muted_people = {}

    def mute(self, discord_user_id: int, seconds: int) -> None:
        muted_person = self.get(discord_user_id)
        muted_person.mute(seconds)

    def unmute(self, discord_user_id: int) -> None:
        muted_person = self.get(discord_user_id)
        muted_person.unmute()

    def get(self, discord_user_id: int) -> MutedPerson:
        person = MuteModule.muted_people.get(discord_user_id, MutedPerson(discord_user_id))
        self.muted_people[discord_user_id] = person
        return person
