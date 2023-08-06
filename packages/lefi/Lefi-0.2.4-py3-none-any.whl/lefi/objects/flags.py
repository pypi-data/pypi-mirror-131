from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union

__all__ = (
    "Flag",
    "ApplicationFlags",
    "MessageFlags",
    "SystemChannelFlags",
    "UserFlags",
    "Intents",
    "Permissions",
)


class InvalidFlag(TypeError):
    def __init__(self, name: str, flag: Type[Flag]) -> None:
        self.name = name
        self.flag = flag
        self.valid_flags: Tuple[str, ...] = tuple(flag.__members__.keys())

        super().__init__(f"{name!r} is not a valid flag for {flag.__name__}")


FlagT = TypeVar("FlagT", bound="Flag")


class FlagValue(int):
    _name_: str
    _value_: int

    def __new__(cls, name: str, value: int):
        obj = super().__new__(cls, value)

        obj._name_ = name
        obj._value_ = value

        return obj

    def __repr__(self) -> str:
        return f"<FlagValue name={self.name!r} value={self.value}>"

    @property
    def name(self) -> str:
        return self._name_

    @property
    def value(self) -> int:
        return self._value_


class FlagMeta(type):
    __members__: Dict[str, FlagValue]

    def __new__(cls, name: str, bases: Tuple[Type], attrs: Dict[str, Any]):
        members: Dict[str, FlagValue] = {}

        for attr, value in attrs.copy().items():
            is_method = callable(value) or isinstance(value, (staticmethod, classmethod))
            if not attr.startswith(("__", "_")) and not is_method:
                members[attr] = FlagValue(attr, value)  # type: ignore
                del attrs[attr]

        attrs["__members__"] = members
        return super().__new__(cls, name, bases, attrs)

    def __getattr__(cls, name: str) -> FlagValue:
        value = cls.__members__.get(name)
        if not value:
            raise AttributeError(f"{cls.__name__} has no attribute {name!r}")

        return value

    def __iter__(self):
        return iter(self.__members__.values())


class Flag(metaclass=FlagMeta):
    __members__: Dict[str, FlagValue]
    value: int

    def __init__(self, value: int = 0, **kwargs: bool) -> None:
        self.value = value
        cls = type(self)

        for name, value in kwargs.items():
            flag: Optional[FlagValue] = getattr(cls, name, None)
            if not flag:
                raise InvalidFlag(name, cls)

            if self.value & flag:
                continue

            if value is True:
                self.value |= flag
            else:
                self.value &= ~flag

    def __getattr__(self, name: str) -> bool:
        flag = self.__members__.get(name)
        if not flag:
            raise AttributeError(f"{type(self).__name__} has no attribute {name!r}")

        return bool(self.value & flag.value)

    def __setattr__(self, name: str, value: Any) -> None:
        flag = self.__members__.get(name)
        if not flag:
            return super().__setattr__(name, value)

        if self.value & flag:
            return

        if value:
            self.value |= flag
        else:
            self.value &= ~flag

    def __iter__(self):
        return iter(self.__values__.items())

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"<{name} value={self.value}>"

    def __or__(self: FlagT, other: Union[int, FlagT]) -> FlagT:
        if isinstance(other, int):
            return self.__class__(self.value | other)

        return self.__class__(self.value | other.value)

    def __and__(self: FlagT, other: Union[int, FlagT]) -> FlagT:
        if isinstance(other, int):
            return self.__class__(self.value & other)

        return self.__class__(self.value & other.value)

    def __invert__(self: FlagT) -> FlagT:
        return self.__class__(~self.value)

    def __bool__(self) -> bool:
        return bool(self.value)

    def __eq__(self: FlagT, other: FlagT) -> bool:  # type: ignore
        if not isinstance(other, Flag):
            return NotImplemented

        return self.value == other.value

    @property
    def __values__(self) -> Dict[FlagValue, bool]:
        return {flag: bool(self.value & flag.value) for flag in self.__class__}


class ApplicationFlags(Flag):
    gateway_presence = 1 << 12
    gateway_presence_limited = 1 << 13
    gateway_guild_members = 1 << 14
    gateway_guild_members_limited = 1 << 15
    verification_pending_guild_limit = 1 << 16
    embedded = 1 << 17


class MessageFlags(Flag):
    crossposted = 1 << 0
    is_crossposted = 1 << 1
    suppress_embeds = 1 << 2
    source_message_deleted = 1 << 3
    urgent = 1 << 4
    has_thread = 1 << 5
    ephemeral = 1 << 6
    loading = 1 << 7


class SystemChannelFlags(Flag):
    suppress_join_notifications = 1 << 0
    suppress_premium_subscriptions = 1 << 1
    suppress_guild_reminder_notifications = 1 << 2


class UserFlags(Flag):
    none = 0
    employee = 1 << 0
    partnered_server_owner = 1 << 1
    hypersquad_events = 1 << 2
    bug_hunter_level_1 = 1 << 3
    house_bravery = 1 << 6
    house_brilliance = 1 << 7
    house_balance = 1 << 8
    early_supporter = 1 << 9
    team_user = 1 << 10
    bug_hunter_level_2 = 1 << 14
    verified_bot = 1 << 16
    verified_developer = 1 << 17
    certified_moderator = 1 << 18


class Intents(Flag):
    guilds = 1 << 0
    guild_members = 1 << 1
    guild_bans = 1 << 2
    guild_emojis_and_stickers = 1 << 3
    guild_intergrations = 1 << 4
    guild_webhooks = 1 << 5
    guild_invites = 1 << 6
    guild_voice_states = 1 << 7
    guild_presences = 1 << 8
    guild_messages = 1 << 9
    guild_message_reactions = 1 << 10
    guild_message_typing = 1 << 11
    direct_messages = 1 << 12
    direct_message_reactions = 1 << 13
    direct_message_typing = 1 << 14

    @classmethod
    def all(cls):
        kwargs = {flag.name: True for flag in cls}
        return cls(**kwargs)

    @classmethod
    def default(cls):
        self = cls.all()

        self.guild_members = False
        self.guild_presences = False

        return self

    @classmethod
    def none(cls):
        return cls(0)


class Permissions(Flag):
    create_instant_invite = 1 << 0
    kick_members = 1 << 1
    ban_members = 1 << 2
    administrator = 1 << 3
    manage_channels = 1 << 4
    manage_guild = 1 << 5
    add_reactions = 1 << 6
    view_audit_log = 1 << 7
    priority_speaker = 1 << 8
    stream = 1 << 9
    view_channel = 1 << 10
    send_messages = 1 << 11
    send_tts_messages = 1 << 12
    manage_messages = 1 << 13
    embed_links = 1 << 14
    attach_files = 1 << 15
    read_message_history = 1 << 16
    mention_everyone = 1 << 17
    use_external_emojis = 1 << 18
    connect = 1 << 20
    speak = 1 << 21
    mute_members = 1 << 22
    deafen_members = 1 << 23
    move_members = 1 << 24
    use_vad = 1 << 25
    change_nickname = 1 << 26
    manage_nicknames = 1 << 27
    manage_roles = 1 << 28
    manage_webhooks = 1 << 29
    manage_emojis_and_stickers = 1 << 30
    use_application_commands = 1 << 31
    request_to_speak = 1 << 32
    manage_threads = 1 << 34
    create_public_threads = 1 << 35
    create_private_threads = 1 << 36
    use_external_stickers = 1 << 37
    send_messages_in_threads = 1 << 38
    start_embedded_activities = 1 << 39

    @classmethod
    def all(cls):
        kwargs = {flag.name: True for flag in cls}
        return cls(**kwargs)

    @classmethod
    def none(cls):
        return cls(0)

    def to_overwrite_pair(self) -> Tuple[Permissions, Permissions]:
        deny = Permissions.none()
        allow = Permissions.none()

        for flag, value in self:
            if value is True:
                setattr(allow, flag.name, True)
            else:
                setattr(deny, flag.name, True)

        return allow, deny

    @classmethod
    def from_overwrite_pair(cls, allow: Permissions, deny: Permissions) -> Permissions:
        self = cls()

        for flag, value in allow:
            if value is True:
                setattr(self, flag.name, True)

        for flag, value in deny:
            if value is True:
                setattr(self, flag.name, False)

        return self
