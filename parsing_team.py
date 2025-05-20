from playwright.sync_api import sync_playwright

def main():
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
            team_league = league_panel.query_selector("div.panel-box-heading.a").query_selector("a").inner_text()
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

if __name__ == "__main__":
    main()