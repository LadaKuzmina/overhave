from pathlib import Path
from typing import List, Optional

import allure
from _pytest.mark import Mark
from _pytest.nodes import Item
from pytest_bdd.parser import Scenario

from overhave.testing.settings import OverhaveProjectSettings


def get_scenario(item: Item) -> Scenario:
    return item._obj.__scenario__  # type: ignore


def is_pytest_bdd_item(item: Item) -> bool:
    if hasattr(item, "_obj"):
        return hasattr(item._obj, "__scenario__") and isinstance(get_scenario(item), Scenario)  # type: ignore
    return False


def _get_issue_links(scenario: Scenario, keyword: str) -> Optional[List[str]]:
    keyword_with_colon = keyword.title() + ":"
    with Path(scenario.feature.filename).open() as file:
        for line in file:
            if keyword not in line:
                continue
            links_part = line.split(keyword_with_colon)[-1]
            return [x.strip() for x in links_part.split(",")]
    return None


def set_issue_links(scenario: Scenario, keyword: str) -> None:
    links = _get_issue_links(scenario, keyword)
    if links:
        setattr(scenario.feature, "links", links)


def has_issue_links(item: Item) -> bool:
    return is_pytest_bdd_item(item) and hasattr(get_scenario(item).feature, "links")


def add_issue_links_to_report(project_settings: OverhaveProjectSettings, scenario: Scenario) -> None:
    for link in scenario.feature.links:
        allure.dynamic.link(url=project_settings.get_link_url(link), name=link)


def add_scenario_title_to_report(item: Item) -> None:
    item.own_markers.append(Mark(name="allure_display_name", args=(f"{get_scenario(item).name}",), kwargs={},))
