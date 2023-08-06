from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from .enums import InviteTargetType

if TYPE_CHECKING:
    from .user import User
    from ..state import State
    from .channel import TextChannel, VoiceChannel
    from .guild import Guild

__all__ = ("Invite", "PartialInvite")


class InviteBase:
    """The base class for :class:`.Invite` and :class:`.PartialInvite`."""

    _data: Dict[str, Any]

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"<{name} code={self.code!r} url={self.url!r}>"

    @property
    def code(self) -> str:
        """The invite code."""
        return self._data["code"]

    @property
    def url(self) -> str:
        """The invite's URL."""
        return f"https://discord.gg/{self.code}"


class PartialInvite(InviteBase):
    """Represents a partial invite.

    This is a partial invite, which is an invite with limited information.
    """

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def uses(self) -> int:
        """The number of times this invite has been used."""
        return self._data["uses"]


class Invite(InviteBase):
    """Represents an invite."""

    def __init__(self, state: State, data: Dict[str, Any]) -> None:
        self._data = data
        self._state = state

    @property
    def guild(self) -> Optional[Guild]:
        """The guild which the invite belongs to."""
        return self._state.get_guild(self._data.get("guild", {}).get("id", 0))

    @property
    def channel(self) -> Optional[Union[TextChannel, VoiceChannel]]:
        """The channel that the invite leads to."""
        return self._state.get_channel(int(self._data["channel"]["id"]))  # type: ignore

    @property
    def inviter(self) -> Optional[User]:
        """The user which created the invite."""
        return self._state.get_user(self._data.get("inviter", {}).get("id", 0))

    @property
    def uses(self) -> Optional[int]:
        """The number of times this invite has been used."""
        return self._data.get("uses")

    @property
    def max_uses(self) -> Optional[int]:
        """The maximum number of times this invite can be used."""
        return self._data.get("max_uses")

    @property
    def max_age(self) -> Optional[int]:
        """The maximum age of this invite."""
        return self._data.get("max_age")

    @property
    def temporary(self) -> bool:
        """Whether this invite is temporary or not."""
        return self._data.get("temporary", False)

    @property
    def created_at(self) -> Optional[datetime.datetime]:
        """The creation time of this invite."""
        created_at = self._data.get("created_at")
        if created_at:
            return datetime.datetime.fromisoformat(created_at)

        return created_at

    @property
    def target_type(self) -> Optional[InviteTargetType]:
        """The target type of this invite."""
        target_type = self._data.get("target_type")
        if target_type is None:
            return None

        return InviteTargetType(target_type)

    @property
    def target_user(self) -> Optional[User]:
        """The target user of this invite."""
        user = self._data.get("target_user")
        if not user:
            return None

        return User(self._state, user)

    @property
    def approximate_presence_count(self) -> Optional[int]:
        """The approximate number of members in the guild this invite is for."""
        return self._data.get("approximate_presence_count")

    @property
    def approximate_member_count(self) -> Optional[int]:
        """The approximate number of members in the guild this invite is for."""
        return self._data.get("approximate_member_count")

    async def delete(self) -> None:
        """Deletes this invite.

        Raises
        ------
        :exc:`.HTTPException`
            Something went wrong while making the request.

        :exc:`.Forbidden`
            Your client doesn't have permissions to delete this invite.
        """
        await self._state.http.delete_invite(self.code)
