from playwright.sync_api import Page
import pytest

URL = "https://the-internet.herokuapp.com"

def test_titulo_pagina_login(page: Page):
    page.goto(f"{URL}/login")
    assert page.title() == "The Internet"

def test_login_exitoso(page: Page):
    page.goto(f"{URL}/login")
    page.fill("input#username", "tomsmith")
    page.fill("input#password", "SuperSecretPassword!")
    page.click("button[type='submit']")
    assert "You logged into a secure area!" in page.text_content("#flash")

def test_login_fallido(page: Page):
    page.goto(f"{URL}/login")
    page.fill("input#username", "tomsmith")
    page.fill("input#password", "WrongPassword")
    page.click("button[type='submit']")
    assert "Your password is invalid!" in page.text_content("#flash")
