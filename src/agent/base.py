from typing import Protocol, Union


class InsightAgenticCall(Protocol):
    name: str = None

    def daily_insight(self, data: dict) -> str:
        raise NotImplementedError

    def weekly_insight(self, data: list) -> str:
        raise NotImplementedError

    def monthly_insight(self, data: list) -> str:
        raise NotImplementedError

    def yearly_insight(self, data: list) -> str:
        raise NotImplementedError

    def send(self, prompt: str) -> str:
        raise NotImplementedError


def get_insight(type: str, agent: InsightAgenticCall, data: Union[list, dict]):
    strategies = {
        "daily": agent.daily_insight,
        "weekly": agent.weekly_insight,
        "monthly": agent.monthly_insight,
        "yearly": agent.yearly_insight,
    }
    if type not in strategies:
        raise ValueError(f"Unsupported insight type provided: {type}")
    return strategies[type](data)
