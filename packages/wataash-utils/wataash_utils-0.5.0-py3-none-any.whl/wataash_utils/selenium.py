# SPDX-License-Identifier: Apache-2.0

import re
import typing as t

from selenium.webdriver.remote.webdriver import WebDriver


def switch_to_urls(driver: WebDriver, urls: t.List[re.Pattern]) -> bool:
    # TODO: want to get the active tab...
    # wh_current = driver.current_window_handle  # not the active tab!
    found = False
    for wh in driver.window_handles:
        driver.switch_to.window(wh)
        for url in urls:
            m = url.search(driver.current_url)
            if m is not None:
                driver.switch_to.window(wh)
                break
        else:
            continue
        found = True
        break
    else:
        assert not found
    # driver.switch_to.window(wh_current)
    return found

# TODO: create new tab
# https://stackoverflow.com/questions/17547473/how-to-open-a-new-tab-using-selenium-webdriver
