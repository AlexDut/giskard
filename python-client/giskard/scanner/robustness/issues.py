import pandas as pd
from dataclasses import dataclass

from ..issues import Issue, IssueInfo
from ...models.base import BaseModel
from ...datasets.base import Dataset


@dataclass
class RobustnessIssueInfo(IssueInfo):
    feature: str
    metric: str
    variation_ratio: float
    messages: str


class RobustnessIssue(Issue):
    group = "Robustness"
    info: RobustnessIssueInfo

    def __init__(self, model: BaseModel, dataset: Dataset, level: str, info: RobustnessIssueInfo):
        super().__init__(model, dataset, level, info)

    @property
    def is_major(self) -> bool:
        return self.level == "major"

    @property
    def domain(self) -> str:
        return f"Feature `{self.info.feature}`"

    @property
    def metric(self) -> str:
        return self.info.metric

    @property
    def deviation(self) -> str:
        return f"{self.info.variation_ratio * 100:.2f}% of samples are sensible"

    @property
    def description(self) -> str:
        return ", ".join(self.info.messages)

    def examples(self, n=3) -> pd.DataFrame:
        return pd.DataFrame()

    @property
    def importance(self) -> float:
        return self.info.variation_ratio
