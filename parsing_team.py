""

import re
from playwright.sync_api import sync_playwright, Page
from global_vars import WIKI_SOURCE_URL

def parse_team_links() -> set:
    teams_url = f"{WIKI_SOURCE_URL}/leagueoflegends/Portal:Teams"

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)

        page = browser.new_page()
        page.goto(teams_url)

        # Ждём загрузку ссылок
        page.wait_for_selector("div.panel-box-body")

        team_links = set()

        # Получаем все ссылки
        league_panels = page.query_selector_all("div.panel-box")

        for league_panel in league_panels:
            team_league = league_panel.query_selector(
                "div.panel-box-heading"
            ).query_selector("a").inner_text()
            print(team_league)
            team_names = league_panel.query_selector_all("span.team-template-text")
            for team_name in team_names:
                link = team_name.query_selector("a[href^='/leagueoflegends/']")
                href = link.get_attribute("href")
                team_links.add(href)

        print(f"Найдено {len(team_links)} ссылок на команды.")
        for href in sorted(team_links)[:10]:
            # print(base_url + href)
            pass
        print(len(team_links))

        browser.close()

        return team_links, page

def parse_team_info(brows_page: Page, url):
    "Функция для получения подробной информации о команде"

    brows_page.goto(WIKI_SOURCE_URL + url)
    brows_page.wait_for_selector("div.fo-nttax-infobox-wrapper")


    # Название команды
    name = brows_page.query_selector("div.infobox-header").inner_text()
    name = re.sub(r"\s+", " ", re.sub(r"\[.*?\]", "", name)).strip()

    # Дата создания команды
    section_counter = 1
    created_date_box = ''
    while created_date_box != 'History':
        created_date_box = brows_page.query_selector(
            f"div.fo-nttax-infobox > div:nth-of-type({section_counter}) > div"
        ).inner_text()
        section_counter += 1

    created_date_box = brows_page.query_selector(
        f"div.fo-nttax-infobox > div:nth-of-type({section_counter}) > div:nth-of-type(2)"
    ).inner_text()[-10:].replace("??", "01")

    # Дата расформирования команды
    disbanded_date = None
    try:
        disbanded_date = brows_page.query_selector(
            f"div.fo-nttax-infobox > div:nth-of-type({section_counter + 1}) > div:nth-of-type(2)"
        ).inner_text()[-10:].replace("??", "01")
    except AttributeError:
        pass

    print(name, created_date_box, disbanded_date)


if __name__ == "__main__":
    team_links, pw_page = parse_team_links()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()


        cntr = 0
        # ! dev
        team_links = (
            '/leagueoflegends/CompLexity_Gaming',
            '/leagueoflegends/T1',
            '/leagueoflegends/Gambit_Esports'
        )
        for team_link in team_links:
            cntr += 1
            if not cntr % 5:
                print(cntr)
            parse_team_info(page, team_link)


    