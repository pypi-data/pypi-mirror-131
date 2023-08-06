from __future__ import annotations

import atexit
import sys
import threading

from toga_winforms.widgets.box import Box


class _WebView2Widget(Box):
    def create(self):
        super().create()

    def set_bounds(self, x: int, y: int, width: int, height: int) -> None:
        super().set_bounds(x, y, width, height)

    def set_on_key_down(self, handler: object) -> None:
        pass

    def set_on_webview_load(self, handler: object) -> None:
        pass

    def set_url(self, value: str) -> None:
        ...

    def set_content(self, root_url: str, content: str) -> None:
        raise NotImplementedError

    def set_user_agent(self, value: str) -> None:
        pass

    async def evaluate_javascript(self, javascript: str) -> None:
        raise NotImplementedError

    def invoke_javascript(self, javascript: str) -> None:
        ...


class Factory:
    WebView = _WebView2Widget
