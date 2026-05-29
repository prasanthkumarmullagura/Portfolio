"""
=============================================================================
  Portfolio Website — Comprehensive Test Suite
  Tests every button, link, section, nav item, contact card, project card,
  and interactive element in the portfolio.

  Requirements:
      pip install pytest requests beautifulsoup4

  Run:
      pytest test_portfolio.py -v
=============================================================================
"""

import pytest
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://127.0.0.1:8080"


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def page():
    """Fetch the page once and share it across all tests."""
    try:
        resp = requests.get(BASE_URL, timeout=5)
    except requests.ConnectionError:
        pytest.exit(
            "❌  Flask server is not running. Start it with:  python app.py",
            returncode=1,
        )
    return resp


@pytest.fixture(scope="session")
def soup(page):
    """Return a BeautifulSoup object of the homepage."""
    return BeautifulSoup(page.text, "html.parser")


# =============================================================================
#  1. SERVER & HTTP
# =============================================================================

class TestServer:
    """Basic server health checks."""

    def test_server_is_running(self, page):
        """TC-S01: Server responds with HTTP 200."""
        assert page.status_code == 200, f"Expected 200, got {page.status_code}"

    def test_content_type_is_html(self, page):
        """TC-S02: Response content-type is text/html."""
        assert "text/html" in page.headers.get("Content-Type", "")

    def test_static_css_loads(self):
        """TC-S03: main.css is served successfully."""
        resp = requests.get(f"{BASE_URL}/static/css/main.css", timeout=5)
        assert resp.status_code == 200, "main.css not found"

    def test_static_js_loads(self):
        """TC-S04: main.js is served successfully."""
        resp = requests.get(f"{BASE_URL}/static/js/main.js", timeout=5)
        assert resp.status_code == 200, "main.js not found"


# =============================================================================
#  2. PAGE META & TITLE
# =============================================================================

class TestPageMeta:
    """Page-level meta and head tags."""

    def test_page_title_contains_name(self, soup):
        """TC-M01: Title contains 'Prasanth Kumar Mullagura'."""
        title = soup.find("title").get_text()
        assert "Prasanth Kumar Mullagura" in title

    def test_page_title_contains_role(self, soup):
        """TC-M02: Title contains 'Python & AI Developer'."""
        title = soup.find("title").get_text()
        assert "Python" in title and "AI Developer" in title

    def test_page_title_no_ece_engineer(self, soup):
        """TC-M03: Title does NOT contain 'ECE Engineer'."""
        title = soup.find("title").get_text()
        assert "ECE Engineer" not in title

    def test_meta_description_exists(self, soup):
        """TC-M04: <meta name='description'> tag is present."""
        meta = soup.find("meta", attrs={"name": "description"})
        assert meta is not None and meta.get("content")

    def test_meta_viewport_exists(self, soup):
        """TC-M05: Viewport meta tag present (responsive design)."""
        meta = soup.find("meta", attrs={"name": "viewport"})
        assert meta is not None

    def test_charset_utf8(self, soup):
        """TC-M06: Charset is UTF-8."""
        meta = soup.find("meta", attrs={"charset": True})
        assert meta is not None
        assert meta["charset"].upper() == "UTF-8"

    def test_lang_attribute(self, soup):
        """TC-M07: <html> lang attribute is 'en'."""
        html_tag = soup.find("html")
        assert html_tag.get("lang") == "en"

    def test_css_link_in_head(self, soup):
        """TC-M08: CSS <link> points to main.css."""
        links = soup.find_all("link", rel="stylesheet")
        hrefs = [l.get("href", "") for l in links]
        assert any("main.css" in h for h in hrefs)

    def test_js_script_in_body(self, soup):
        """TC-M09: main.js <script> tag is present."""
        scripts = soup.find_all("script", src=True)
        srcs = [s.get("src", "") for s in scripts]
        assert any("main.js" in s for s in srcs)


# =============================================================================
#  3. NAVIGATION BAR
# =============================================================================

class TestNavigation:
    """All nav links and their targets."""

    def test_navbar_exists(self, soup):
        """TC-N01: <nav id='navbar'> is present."""
        assert soup.find("nav", id="navbar") is not None

    def test_logo_link(self, soup):
        """TC-N02: Logo 'PK.' links to #home."""
        logo = soup.find("a", class_="logo")
        assert logo is not None
        assert logo.get("href") == "#home"
        assert "PK" in logo.get_text()

    def test_nav_about_link(self, soup):
        """TC-N03: 'About' nav link points to #about."""
        link = soup.find("a", id="nav-about")
        assert link is not None
        assert link.get("href") == "#about"
        assert "About" in link.get_text()

    def test_nav_education_link(self, soup):
        """TC-N04: 'Education' nav link points to #education."""
        link = soup.find("a", id="nav-education")
        assert link is not None
        assert link.get("href") == "#education"

    def test_nav_skills_link(self, soup):
        """TC-N05: 'Skills' nav link points to #skills."""
        link = soup.find("a", id="nav-skills")
        assert link is not None
        assert link.get("href") == "#skills"

    def test_nav_projects_link(self, soup):
        """TC-N06: 'Work' nav link points to #projects."""
        link = soup.find("a", id="nav-projects")
        assert link is not None
        assert link.get("href") == "#projects"

    def test_nav_contact_button(self, soup):
        """TC-N07: 'Let's Talk' button points to #contact."""
        btn = soup.find("a", id="nav-contact")
        assert btn is not None
        assert btn.get("href") == "#contact"
        assert "Talk" in btn.get_text()

    def test_all_nav_sections_exist(self, soup):
        """TC-N08: All nav target section IDs exist in page."""
        targets = ["home", "about", "education", "skills", "projects", "contact"]
        for tid in targets:
            el = soup.find(id=tid)
            assert el is not None, f"Section #{tid} not found in page"


# =============================================================================
#  4. HERO SECTION
# =============================================================================

class TestHeroSection:
    """Hero section content and buttons."""

    def test_hero_section_exists(self, soup):
        """TC-H01: Hero section with id='home' exists."""
        assert soup.find("section", id="home") is not None

    def test_hero_h1_contains_name(self, soup):
        """TC-H02: <h1> contains 'Prasanth'."""
        h1 = soup.find("h1")
        assert "Prasanth" in h1.get_text()

    def test_hero_title_is_python_ai_developer(self, soup):
        """TC-H03: Hero title contains 'Python' and 'AI Developer'."""
        h1 = soup.find("h1")
        text = h1.get_text()
        assert "Python" in text and "AI Developer" in text

    def test_hero_no_ece_engineer(self, soup):
        """TC-H04: 'ECE Engineer' is NOT in hero title (removed as requested)."""
        h1 = soup.find("h1")
        assert "ECE Engineer" not in h1.get_text()

    def test_hero_status_badge_removed(self, soup):
        """TC-H05: 'Open to Opportunities' status badge is REMOVED."""
        badge = soup.find(class_="status-badge")
        assert badge is None or "Open to Opportunities" not in badge.get_text()

    def test_hero_view_featured_work_btn(self, soup):
        """TC-H06: 'View Featured Work' button links to #projects."""
        hero = soup.find("section", id="home")
        links = hero.find_all("a", href="#projects")
        assert len(links) >= 1
        assert any("Featured Work" in l.get_text() for l in links)

    def test_hero_github_button(self, soup):
        """TC-H07: GitHub button links to correct GitHub profile URL."""
        hero = soup.find("section", id="home")
        links = hero.find_all("a", target="_blank")
        github_links = [l for l in links if "github.com/prasanthkumarmullagura" in l.get("href", "")]
        assert len(github_links) >= 1

    def test_hero_linkedin_button(self, soup):
        """TC-H08: LinkedIn button links to correct LinkedIn URL."""
        hero = soup.find("section", id="home")
        links = hero.find_all("a", target="_blank")
        li_links = [l for l in links if "linkedin.com/in/prasanthkumarmullagura" in l.get("href", "")]
        assert len(li_links) >= 1

    def test_hero_email_button(self, soup):
        """TC-H09: Email button uses mailto: for correct address."""
        hero = soup.find("section", id="home")
        mail = hero.find("a", href="mailto:prasanthkumarmullagura@gmail.com")
        assert mail is not None

    def test_hero_desc_paragraph(self, soup):
        """TC-H10: Hero description paragraph is present."""
        hero = soup.find("section", id="home")
        desc = hero.find(class_="hero-desc")
        assert desc is not None
        assert len(desc.get_text(strip=True)) > 20


# =============================================================================
#  5. STATS BANNER
# =============================================================================

class TestStatsBanner:
    """Stats banner numbers."""

    def test_stats_banner_exists(self, soup):
        """TC-ST01: Stats banner exists on page."""
        banner = soup.find(class_="stats-banner")
        assert banner is not None

    def test_stats_show_projects(self, soup):
        """TC-ST02: Stats banner shows project count."""
        banner = soup.find(class_="stats-banner")
        assert "Projects" in banner.get_text()

    def test_stats_show_certifications(self, soup):
        """TC-ST03: Stats banner shows certifications."""
        banner = soup.find(class_="stats-banner")
        assert "Certifications" in banner.get_text()

    def test_stats_show_languages(self, soup):
        """TC-ST04: Stats banner shows languages known."""
        banner = soup.find(class_="stats-banner")
        assert "Languages" in banner.get_text()


# =============================================================================
#  6. ABOUT SECTION
# =============================================================================

class TestAboutSection:
    """About section content; ensures chips are removed."""

    def test_about_section_exists(self, soup):
        """TC-A01: About section with id='about' exists."""
        assert soup.find("section", id="about") is not None

    def test_about_contains_full_name(self, soup):
        """TC-A02: About section contains full name."""
        section = soup.find("section", id="about")
        assert "Prasanth Kumar Mullagura" in section.get_text()

    def test_about_mentions_python_ai(self, soup):
        """TC-A03: About section mentions Python & AI Developer."""
        section = soup.find("section", id="about")
        text = section.get_text()
        assert "Python" in text and "AI" in text

    def test_about_mentions_vel_tech(self, soup):
        """TC-A04: About section mentions Vel Tech University."""
        section = soup.find("section", id="about")
        assert "Vel Tech University" in section.get_text()

    def test_about_no_location_chip(self, soup):
        """TC-A05: Location chip ('Chennai, Tamil Nadu, India') is REMOVED from About."""
        about = soup.find("section", id="about")
        chips = about.find_all(class_="about-info-chip")
        chip_texts = [c.get_text(strip=True) for c in chips]
        assert not any("Chennai, Tamil Nadu" in t for t in chip_texts)

    def test_about_no_phone_chip(self, soup):
        """TC-A06: Phone chip is REMOVED from About section."""
        about = soup.find("section", id="about")
        chips = about.find_all(class_="about-info-chip")
        chip_texts = [c.get_text(strip=True) for c in chips]
        assert not any("8074284387" in t for t in chip_texts)

    def test_about_no_email_chip(self, soup):
        """TC-A07: Email chip is REMOVED from About section."""
        about = soup.find("section", id="about")
        chips = about.find_all(class_="about-info-chip")
        chip_texts = [c.get_text(strip=True) for c in chips]
        assert not any("prasanthkumarmullagura@gmail.com" in t for t in chip_texts)

    def test_about_no_linkedin_chip(self, soup):
        """TC-A08: LinkedIn chip ('prasanth-kumar') is REMOVED from About."""
        about = soup.find("section", id="about")
        chips = about.find_all(class_="about-info-chip")
        assert len(chips) == 0, "No chips should remain in About section"

    def test_about_tech_pills_present(self, soup):
        """TC-A09: Tech pills (Python, Flask, etc.) are shown in About."""
        about = soup.find("section", id="about")
        pills = about.find_all(class_="tech-pill")
        assert len(pills) >= 4

    def test_about_tech_pill_python(self, soup):
        """TC-A10: 'Python' tech pill exists in About."""
        about = soup.find("section", id="about")
        pills = [p.get_text(strip=True) for p in about.find_all(class_="tech-pill")]
        assert "Python" in pills

    def test_about_tech_pill_flask(self, soup):
        """TC-A11: 'Flask' tech pill exists in About."""
        about = soup.find("section", id="about")
        pills = [p.get_text(strip=True) for p in about.find_all(class_="tech-pill")]
        assert "Flask" in pills


# =============================================================================
#  7. EDUCATION SECTION
# =============================================================================

class TestEducationSection:
    """Education timeline and certifications."""

    def test_education_section_exists(self, soup):
        """TC-E01: Education section with id='education' exists."""
        assert soup.find("section", id="education") is not None

    def test_education_veltech(self, soup):
        """TC-E02: Vel Tech University entry is present."""
        section = soup.find("section", id="education")
        assert "Vel Tech University" in section.get_text()

    def test_education_sri_chaitanya_removed(self, soup):
        """TC-E03: Sri Chaitanya Junior College entry is REMOVED."""
        section = soup.find("section", id="education")
        items = section.find_all(class_="edu-item")
        texts = [i.get_text() for i in items]
        assert not any("Sri Chaitanya" in t for t in texts)

    def test_education_keshava_reddy_removed(self, soup):
        """TC-E04: Keshava Reddy School entry is REMOVED."""
        section = soup.find("section", id="education")
        items = section.find_all(class_="edu-item")
        texts = [i.get_text() for i in items]
        assert not any("Keshava Reddy" in t for t in texts)

    def test_education_no_cgpa_shown(self, soup):
        """TC-E05: No CGPA numbers shown in education timeline."""
        section = soup.find("section", id="education")
        items = section.find_all(class_="edu-item")
        for item in items:
            text = item.get_text()
            assert "CGPA" not in text, f"CGPA still present in: {text[:80]}"

    def test_education_cgpa_82_removed(self, soup):
        """TC-E06: CGPA 8.2 (12th) is NOT shown."""
        section = soup.find("section", id="education")
        assert "8.2" not in section.get_text()

    def test_education_cgpa_98_removed(self, soup):
        """TC-E07: CGPA 9.8 (10th) is NOT shown."""
        section = soup.find("section", id="education")
        assert "9.8" not in section.get_text()

    def test_certifications_tcs_ion(self, soup):
        """TC-E08: TCS iON Career Edge certification shown."""
        section = soup.find("section", id="education")
        assert "TCS iON" in section.get_text()

    def test_certifications_generative_ai(self, soup):
        """TC-E09: Generative AI certification shown."""
        section = soup.find("section", id="education")
        assert "Generative AI" in section.get_text()

    def test_certifications_iot_embedded(self, soup):
        """TC-E10: IoT & Embedded training shown."""
        section = soup.find("section", id="education")
        assert "IoT" in section.get_text()

    def test_certifications_hackathon(self, soup):
        """TC-E11: Hackathon participation shown."""
        section = soup.find("section", id="education")
        assert "Hackathon" in section.get_text()

    def test_edu_timeline_has_one_item(self, soup):
        """TC-E12: Education timeline has exactly 1 item (B.Tech only)."""
        section = soup.find("section", id="education")
        items = section.find_all(class_="edu-item")
        assert len(items) == 1, f"Expected 1 edu item, found {len(items)}"

    def test_edu_btech_year_badge(self, soup):
        """TC-E13: Year badge 2022–2026 present for B.Tech."""
        section = soup.find("section", id="education")
        text = section.get_text()
        assert "2022" in text and "2026" in text

    def test_edu_old_years_removed(self, soup):
        """TC-E14: Old year badges 2020–2022 and 2019–2020 are REMOVED."""
        section = soup.find("section", id="education")
        items = section.find_all(class_="edu-item")
        badge_texts = [i.find(class_="edu-year-badge").get_text() for i in items]
        assert not any("2020–2022" in b for b in badge_texts)
        assert not any("2019–2020" in b for b in badge_texts)


# =============================================================================
#  8. SKILLS SECTION
# =============================================================================

class TestSkillsSection:
    """Skills section — all categories and pills."""

    def test_skills_section_exists(self, soup):
        """TC-SK01: Skills section with id='skills' exists."""
        assert soup.find("section", id="skills") is not None

    def test_skills_has_heading(self, soup):
        """TC-SK02: Skills section has a heading."""
        section = soup.find("section", id="skills")
        assert section.find(["h2", "h3"]) is not None

    def test_skills_has_six_categories(self, soup):
        """TC-SK03: 6 skill category cards are present."""
        section = soup.find("section", id="skills")
        cards = section.find_all(class_="skill-category-card")
        assert len(cards) == 6

    def test_skills_programming_category(self, soup):
        """TC-SK04: 'Programming Languages' category exists."""
        section = soup.find("section", id="skills")
        assert "Programming" in section.get_text()

    def test_skills_python_pill(self, soup):
        """TC-SK05: 'Python' pill is in Skills."""
        section = soup.find("section", id="skills")
        pills = [p.get_text(strip=True) for p in section.find_all(class_="skill-pill-sm")]
        assert "Python" in pills

    def test_skills_sql_pill(self, soup):
        """TC-SK06: 'SQL' pill is in Skills."""
        section = soup.find("section", id="skills")
        pills = [p.get_text(strip=True) for p in section.find_all(class_="skill-pill-sm")]
        assert "SQL" in pills

    def test_skills_ml_category(self, soup):
        """TC-SK07: 'AI & Machine Learning' category exists."""
        section = soup.find("section", id="skills")
        assert "Machine Learning" in section.get_text()

    def test_skills_tensorflow_pill(self, soup):
        """TC-SK08: 'TensorFlow' pill is in Skills."""
        section = soup.find("section", id="skills")
        pills = [p.get_text(strip=True) for p in section.find_all(class_="skill-pill-sm")]
        assert "TensorFlow" in pills

    def test_skills_tools_category(self, soup):
        """TC-SK09: Tools & Platforms category exists."""
        section = soup.find("section", id="skills")
        assert "Git" in section.get_text() or "GitHub" in section.get_text()

    def test_skills_soft_skills_category(self, soup):
        """TC-SK10: Soft Skills category exists."""
        section = soup.find("section", id="skills")
        assert "Communication" in section.get_text()

    def test_skills_languages_category(self, soup):
        """TC-SK11: Languages Known category shows all languages."""
        section = soup.find("section", id="skills")
        text = section.get_text()
        for lang in ["English", "Hindi", "Telugu", "Spanish", "German"]:
            assert lang in text, f"Language '{lang}' missing from Skills"

    def test_skills_minimum_pills_count(self, soup):
        """TC-SK12: At least 20 skill pills total."""
        section = soup.find("section", id="skills")
        pills = section.find_all(class_="skill-pill-sm")
        assert len(pills) >= 20


# =============================================================================
#  9. PROJECTS SECTION
# =============================================================================

class TestProjectsSection:
    """All 5 project cards and their content."""

    def test_projects_section_exists(self, soup):
        """TC-P01: Projects section with id='projects' exists."""
        assert soup.find("section", id="projects") is not None

    def test_projects_has_five_cards(self, soup):
        """TC-P02: Exactly 5 project cards are present."""
        section = soup.find("section", id="projects")
        cards = section.find_all(class_="project-card")
        assert len(cards) == 5, f"Expected 5 project cards, found {len(cards)}"

    def test_project_retail_analytics_exists(self, soup):
        """TC-P03: 'Retail Store Analytics System' project card exists."""
        section = soup.find("section", id="projects")
        assert "Retail Store Analytics" in section.get_text()

    def test_project_retail_tags(self, soup):
        """TC-P04: Retail project shows Python, Pandas, SQL tags."""
        section = soup.find("section", id="projects")
        text = section.get_text()
        assert "Pandas" in text
        assert "SQL" in text

    def test_project_doctor_portal_exists(self, soup):
        """TC-P05: 'Doctor Management Portal' project card exists."""
        section = soup.find("section", id="projects")
        assert "Doctor Management Portal" in section.get_text()

    def test_project_doctor_tags(self, soup):
        """TC-P06: Doctor Portal shows Flask and SQLite tags."""
        section = soup.find("section", id="projects")
        text = section.get_text()
        assert "Flask" in text
        assert "SQLite" in text

    def test_project_ai_chatbot_exists(self, soup):
        """TC-P07: 'AI ChatGPT Frontend' project card exists."""
        section = soup.find("section", id="projects")
        assert "AI ChatGPT Frontend" in section.get_text()

    def test_project_traffic_sign_exists(self, soup):
        """TC-P08: 'Traffic Sign Recognition' project card exists."""
        section = soup.find("section", id="projects")
        assert "Traffic Sign Recognition" in section.get_text()

    def test_project_mini_ups_exists(self, soup):
        """TC-P09: 'Smart Mini WiFi UPS' project card exists."""
        section = soup.find("section", id="projects")
        assert "WiFi UPS" in section.get_text()

    def test_all_project_view_source_links(self, soup):
        """TC-P10: All project cards have 'View Source Code' links."""
        section = soup.find("section", id="projects")
        cards = section.find_all(class_="project-card")
        for i, card in enumerate(cards, 1):
            links = card.find_all("a")
            assert len(links) >= 1, f"Project card {i} has no link"

    def test_all_project_links_point_to_github(self, soup):
        """TC-P11: All project 'View Source Code' links point to GitHub."""
        section = soup.find("section", id="projects")
        project_links = [
            a for a in section.find_all("a", class_="project-link")
        ]
        assert len(project_links) == 5
        for link in project_links:
            href = link.get("href", "")
            assert "github.com" in href, f"Project link doesn't go to GitHub: {href}"

    def test_all_project_links_open_new_tab(self, soup):
        """TC-P12: All project links open in new tab (target='_blank')."""
        section = soup.find("section", id="projects")
        project_links = section.find_all("a", class_="project-link")
        for link in project_links:
            assert link.get("target") == "_blank", \
                f"Link '{link.get_text(strip=True)}' doesn't open in new tab"

    def test_project_cards_have_tags(self, soup):
        """TC-P13: Every project card has at least one tech tag."""
        section = soup.find("section", id="projects")
        cards = section.find_all(class_="project-card")
        for i, card in enumerate(cards, 1):
            tags = card.find_all(class_="project-tag")
            assert len(tags) >= 1, f"Project card {i} has no tech tags"

    def test_project_cards_have_descriptions(self, soup):
        """TC-P14: Every project card has a description paragraph."""
        section = soup.find("section", id="projects")
        cards = section.find_all(class_="project-card")
        for i, card in enumerate(cards, 1):
            content = card.find(class_="project-content")
            assert content is not None
            p = content.find("p")
            assert p is not None and len(p.get_text(strip=True)) > 20, \
                f"Project card {i} description is empty or missing"


# =============================================================================
#  10. CONTACT SECTION (Let's Connect)
# =============================================================================

class TestContactSection:
    """Redesigned contact section with 4 clickable contact cards."""

    def test_contact_section_exists(self, soup):
        """TC-C01: Contact section with id='contact' exists."""
        assert soup.find("section", id="contact") is not None

    def test_contact_heading(self, soup):
        """TC-C02: Contact section has a heading containing 'Connect'."""
        section = soup.find("section", id="contact")
        headings = section.find_all(["h1", "h2", "h3"])
        text = " ".join(h.get_text() for h in headings)
        assert "Connect" in text

    def test_contact_has_four_cards(self, soup):
        """TC-C03: Exactly 4 contact cards are present."""
        section = soup.find("section", id="contact")
        cards = section.find_all(class_="contact-card")
        assert len(cards) == 4, f"Expected 4 contact cards, found {len(cards)}"

    def test_contact_email_card(self, soup):
        """TC-C04: Email contact card exists with correct mailto link."""
        card = soup.find("a", id="contact-email")
        assert card is not None
        assert card.get("href") == "mailto:prasanthkumarmullagura@gmail.com"

    def test_contact_email_card_label(self, soup):
        """TC-C05: Email card shows label 'Email'."""
        card = soup.find("a", id="contact-email")
        assert "Email" in card.get_text()

    def test_contact_email_card_address_visible(self, soup):
        """TC-C06: Full email address visible in email card."""
        card = soup.find("a", id="contact-email")
        assert "prasanthkumarmullagura@gmail.com" in card.get_text()

    def test_contact_phone_card(self, soup):
        """TC-C07: Phone contact card exists with tel: link."""
        card = soup.find("a", id="contact-phone")
        assert card is not None
        assert card.get("href") == "tel:+918074284387"

    def test_contact_phone_card_label(self, soup):
        """TC-C08: Phone card shows label 'Phone'."""
        card = soup.find("a", id="contact-phone")
        assert "Phone" in card.get_text()

    def test_contact_phone_number_visible(self, soup):
        """TC-C09: Phone number visible in phone card."""
        card = soup.find("a", id="contact-phone")
        assert "8074284387" in card.get_text()

    def test_contact_linkedin_card(self, soup):
        """TC-C10: LinkedIn contact card exists with correct URL."""
        card = soup.find("a", id="contact-linkedin")
        assert card is not None
        assert "linkedin.com/in/prasanthkumarmullagura" in card.get("href", "")

    def test_contact_linkedin_opens_new_tab(self, soup):
        """TC-C11: LinkedIn card opens in new tab."""
        card = soup.find("a", id="contact-linkedin")
        assert card.get("target") == "_blank"

    def test_contact_linkedin_label(self, soup):
        """TC-C12: LinkedIn card shows 'LinkedIn' label."""
        card = soup.find("a", id="contact-linkedin")
        assert "LinkedIn" in card.get_text()

    def test_contact_github_card(self, soup):
        """TC-C13: GitHub contact card exists with correct URL."""
        card = soup.find("a", id="contact-github")
        assert card is not None
        assert "github.com/prasanthkumarmullagura" in card.get("href", "")

    def test_contact_github_opens_new_tab(self, soup):
        """TC-C14: GitHub card opens in new tab."""
        card = soup.find("a", id="contact-github")
        assert card.get("target") == "_blank"

    def test_contact_github_label(self, soup):
        """TC-C15: GitHub card shows 'GitHub' label."""
        card = soup.find("a", id="contact-github")
        assert "GitHub" in card.get_text()

    def test_no_old_social_btn_class(self, soup):
        """TC-C16: Old social-btn icon buttons are fully replaced (none remain)."""
        section = soup.find("section", id="contact")
        old_btns = section.find_all(class_="social-btn")
        assert len(old_btns) == 0, \
            "Old social-btn icons still present — contact section not fully updated"


# =============================================================================
#  11. FOOTER
# =============================================================================

class TestFooter:
    """Footer content."""

    def test_footer_exists(self, soup):
        """TC-F01: <footer> element exists."""
        assert soup.find("footer") is not None

    def test_footer_contains_name(self, soup):
        """TC-F02: Footer contains 'Prasanth Kumar Mullagura'."""
        footer = soup.find("footer")
        assert "Prasanth Kumar Mullagura" in footer.get_text()

    def test_footer_contains_year(self, soup):
        """TC-F03: Footer contains copyright year 2026."""
        footer = soup.find("footer")
        assert "2026" in footer.get_text()

    def test_footer_contains_role(self, soup):
        """TC-F04: Footer mentions 'Python & AI Developer'."""
        footer = soup.find("footer")
        assert "Python" in footer.get_text() and "AI Developer" in footer.get_text()


# =============================================================================
#  12. ACCESSIBILITY
# =============================================================================

class TestAccessibility:
    """Basic accessibility checks."""

    def test_images_have_alt(self, soup):
        """TC-ACC01: All <img> tags have non-empty alt attributes."""
        images = soup.find_all("img")
        for img in images:
            alt = img.get("alt", "")
            assert alt.strip() != "", f"Image missing alt: {img}"

    def test_nav_links_all_have_href(self, soup):
        """TC-ACC02: All nav links have valid href attributes."""
        nav = soup.find("nav", id="navbar")
        links = nav.find_all("a")
        for link in links:
            href = link.get("href", "")
            assert href != "", f"Nav link missing href: {link}"

    def test_single_h1_on_page(self, soup):
        """TC-ACC03: Only one <h1> tag on the page (SEO best practice)."""
        h1_tags = soup.find_all("h1")
        assert len(h1_tags) == 1, f"Expected 1 <h1>, found {len(h1_tags)}"

    def test_external_links_have_target_blank(self, soup):
        """TC-ACC04: External links (http) have target='_blank'."""
        ext_links = [
            a for a in soup.find_all("a", href=True)
            if a["href"].startswith("http")
        ]
        for link in ext_links:
            assert link.get("target") == "_blank", \
                f"External link missing target='_blank': {link.get('href')}"

    def test_no_broken_hash_links(self, soup):
        """TC-ACC05: All internal #hash links point to existing IDs."""
        hash_links = [
            a for a in soup.find_all("a", href=True)
            if a["href"].startswith("#") and a["href"] != "#"
        ]
        for link in hash_links:
            target_id = link["href"][1:]
            el = soup.find(id=target_id)
            assert el is not None, \
                f"Broken hash link: {link['href']} — no element with id='{target_id}'"

    def test_toast_bar_element_present(self, soup):
        """TC-ACC06: Toast notification bar element present in DOM."""
        toast = soup.find(id="toast-bar")
        assert toast is not None

    def test_scroll_smooth_on_html(self, soup):
        """TC-ACC07: Smooth scroll class on <html> tag."""
        html = soup.find("html")
        assert "scroll-smooth" in html.get("class", [])
