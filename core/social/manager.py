from __future__ import annotations

from core.social.base import SocialAccount, SocialPost, SocialProvider


class SocialManager:
    def __init__(self) -> None:
        self._providers: dict[str, SocialProvider] = {}
        self._accounts: dict[str, SocialAccount] = {}

    def register(self, provider: SocialProvider) -> None:
        self._providers[provider.name] = provider

    def providers(self) -> list[str]:
        return sorted(self._providers.keys())

    def connect(self, platform: str) -> SocialAccount:
        provider = self._providers[platform]
        account = provider.connect()
        self._accounts[platform] = account
        return account

    def publish(
        self,
        platform: str,
        post: SocialPost,
    ) -> dict[str, object]:
        provider = self._providers[platform]

        if platform not in self._accounts:
            raise PermissionError(
                f"Social account '{platform}' is not connected."
            )

        return provider.publish(post)

    def analytics(self, platform: str) -> dict[str, object]:
        provider = self._providers[platform]

        if platform not in self._accounts:
            raise PermissionError(
                f"Social account '{platform}' is not connected."
            )

        return provider.analytics()
