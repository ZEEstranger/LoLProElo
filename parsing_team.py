from playwright.sync_api import sync_playwright, Page
import re

def parse_team_links() -> set:
    base_url = "https://liquipedia.net"
    teams_url = base_url + "/leagueoflegends/Portal:Teams"

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
            team_league = league_panel.query_selector("div.panel-box-heading").query_selector("a").inner_text()
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

def parse_team_info(page: Page, url):
    base_url = "https://liquipedia.net"
    page.goto(base_url + url)
    page.wait_for_selector("div.fo-nttax-infobox-wrapper")

    name = None
    region = None
    founded = None
    disbanded = None

    name = page.query_selector("div.infobox-header")
    
    name = name.inner_text()
    cleaned = re.sub(r"\[.*?\]", "", name)
    name = re.sub(r"\s+", " ", cleaned).strip()

    section_counter = 1


    date_box = ''
    while date_box != 'History':
        date_box = page.query_selector(f"div.fo-nttax-infobox > div:nth-of-type({section_counter}) > div")
        date_box = date_box.inner_text()
        section_counter += 1

    date_box = page.query_selector(f"div.fo-nttax-infobox > div:nth-of-type({section_counter}) > div:nth-of-type(2)")
    date_box = date_box.inner_text()[-10:]


    print(name, date_box)


if __name__ == "__main__":
    team_links, pw_page = parse_team_links()
    
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()


        cntr = 0
        for team_link in team_links:
            cntr += 1
            if not cntr % 5:
                print(cntr)
            a = parse_team_info(page, team_link)


    