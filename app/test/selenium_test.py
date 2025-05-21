import pytest
from .. import create_app
from ..controllers import get_top_score
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "LIVESERVER_PORT": 8005
    })
    yield app

def test_homepage_loads(driver, app):
    driver.get(BASE_URL + "/")
    assert "Trivia Quiz" == driver.title
    start_btn = driver.find_element(By.ID, "start-btn")
    assert start_btn.is_displayed(), "The start button is not displayed"
    leader_board = driver.find_element(By.ID, "start-leader-board")
    assert leader_board.is_displayed(), "The leaderboard is not displayed"
    with app.app_context():
        first_user = get_top_score(top=1)[0]
        first_username_web = driver.find_element(By.CSS_SELECTOR, ".leader-board-usr#usr-0")
        assert first_user.name.strip() == first_username_web.text.strip(), "The name of the first user in the leaderboard is wrong"

def test_click_start(driver):
    driver.get(BASE_URL + "/")
    button_start = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.ID, "start-btn"))
    )
    button_start.click()
    page_title = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "page-title"))
        ).text
    assert page_title == "Question: 1 / 10", "The website title is wrong"
    question = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.ID, f"question-content"))
        )
    assert question.is_displayed(), "The question is not displayed"
    for i in ['a', 'b', 'c', 'd']:
        option = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.ID, f"option_{i}"))
        )
        assert option.is_displayed(), "The option is not displayed"
        if i == 'a':
            option.click()
    button_next = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "next-btn"))
    )
    button_next.click()
    page_title = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "page-title"))
        ).text
    assert page_title == "Question: 2 / 10", "The website title is wrong"

def test_result_page(driver):
    driver.get(BASE_URL + "/")
    button_start = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, "start-btn"))
    )
    button_start.click()
    for i in range(10):
        option = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.ID, f"option_a"))
        )
        option.click()
        button_next = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.ID, "next-btn"))
        )
        button_next.click()
    final_score = WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.ID, "score-result"))
    )
    assert final_score.is_displayed(), "The score is not displayed"
    input_name = WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.ID, "name"))
    )
    assert input_name.is_displayed(), "The input name is not displayed"
    

    




    
    




