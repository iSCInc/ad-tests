"""Library of shortcuts"""

from selenium import webdriver as wd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait

__all__ = ['wd', 'NoSuchElementException', 'EC', 'By', 'Wait']
