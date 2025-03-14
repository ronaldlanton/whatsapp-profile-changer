"""
Browser module for WhatsApp Profile Changer.
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logger = logging.getLogger(__name__)

class Browser:
    """Browser handler for WhatsApp Web automation."""
    
    def __init__(self):
        """Initialize the browser handler."""
        self.driver = None
    
    def setup(self):
        """Set up the browser instance."""
        logger.info("Setting up the browser...")
        options = webdriver.ChromeOptions()
        # Add options to make browser more stable for automation
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://web.whatsapp.com/")
        logger.info("WhatsApp Web opened. Please scan the QR code.")
    
    def wait_for_login(self, timeout=300):
        """
        Wait for user to scan the QR code and log in.
        
        Args:
            timeout (int): Timeout in seconds to wait for login.
            
        Returns:
            bool: True if login successful, False otherwise.
        """
        logger.info(f"Waiting for QR code scan. You have {timeout} seconds to authenticate.")
        try:
            # Wait for the main chat list to appear which indicates successful login
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='side']"))
            )
            logger.info("Successfully logged in to WhatsApp Web.")
            return True
        except TimeoutException:
            logger.error(f"Login timeout after {timeout} seconds. QR code was not scanned.")
            return False
    
    def open_profile_pane(self):
        """
        Open the profile pane.
        
        Returns:
            bool: True if profile pane opened successfully, False otherwise.
        """
        logger.info("Opening profile pane...")
        try:
            # 1. Click profile picture using exact tracked selector
            profile_selector = "img.x1n2onr6.x1lliihq.xh8yej3.x5yr21d.x6ikm8r.x10wlt62.x14yjl9h.xudhj91.x18nykt9.xww2gxu.xl1xv1r.x115dhu7.x17vty23.x1hc1fzr._ao3e"
            
            try:
                profile_pic = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, profile_selector))
                )
                profile_pic.click()
                logger.info("Clicked profile picture")
                time.sleep(0.5)

                # 2. Click the intermediate div
                intermediate_selector = "div.x10l6tqk.x13vifvy.x17qophe.x1vjfegm.xh8yej3.x5yr21d"
                intermediate_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, intermediate_selector))
                )
                intermediate_button.click()
                logger.info("Clicked intermediate button")
                time.sleep(0.5)

                # 3. Click edit area
                edit_selector = "div.x10l6tqk.x13vifvy.x17qophe.xfo81ep.x9f619.x78zum5.xdt5ytf.x6s0dn4.xl56j7k.xh8yej3.x5yr21d.x1nxh6w3.x1u7k74.x1j16vfr.xtvhhri.x146q241.x14yjl9h.xudhj91.x18nykt9.xww2gxu.xqy66fx"
                edit_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, edit_selector))
                )
                edit_button.click()
                logger.info("Clicked edit area")
                time.sleep(0.5)
                return True

            except Exception as e:
                logger.error(f"Error clicking elements: {str(e)}")
                return False

        except Exception as e:
            logger.error(f"Error opening profile pane: {str(e)}")
            return False
    
    def check_for_upload_option(self):
        """
        Check if the upload photo option is visible.
        
        Returns:
            bool: True if upload option is visible, False otherwise.
        """
        try:
            upload_selectors = [
                "//li[@value='0'][@role='button'][contains(text(), 'Upload photo')]",
                "//li[contains(@class, '_aj-r')][contains(text(), 'Upload photo')]",
                "//div[contains(text(), 'Upload photo')]",
                "//span[contains(text(), 'Upload photo')]"
            ]
            
            for selector in upload_selectors:
                try:
                    WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    return True
                except Exception:
                    continue
            
            return False
        except Exception:
            return False
    
    def upload_profile_picture(self, image_path):
        """
        Upload a new profile picture.
        
        Args:
            image_path (str): Path to the image file.
            
        Returns:
            bool: True if upload successful, False otherwise.
        """
        try:
            # Find and use the file input
            file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_input.send_keys(image_path)
            logger.info(f"Uploaded image: {image_path}")
            
            # Wait for image to be processed
            time.sleep(2)

            # Click the save button using the specific class selector
            save_selector = "div.x78zum5.x6s0dn4.xl56j7k.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1f6kntn.xk50ysn.x7o08j2.xtvhhri.x1rluvsa.x14yjl9h.xudhj91.x18nykt9.xww2gxu.xu306ak.x12s1jxh.xkdsq27.xwwtwea.x1gfkgh9.x1247r65.xng8ra[role='button']"
            
            try:
                save_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, save_selector))
                )
                save_button.click()
                logger.info("Clicked save button")
                time.sleep(1)
                return True

            except Exception as e:
                logger.error(f"Error clicking save button: {str(e)}")
                return False

        except Exception as e:
            logger.error(f"Error uploading profile picture: {str(e)}")
            return False
    
    def cleanup(self):
        """Clean up browser resources."""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")