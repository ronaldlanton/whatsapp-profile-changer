from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
import glob
import logging
from PIL import Image, ImageDraw
from datetime import datetime
import pytz
import math

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WhatsAppProfileChanger:
    def __init__(self, pics_folder="pics", duration=5, mode="sequence"):
        """
        Initialize the WhatsApp profile picture changer.
        
        Args:
            pics_folder (str): Folder containing the profile pictures
            duration (int): Duration in seconds to display each picture
            mode (str): Either "sequence" or "clock" mode
        """
        self.pics_folder = pics_folder
        self.duration = duration
        self.mode = mode
        self.driver = None
        
        if mode == "sequence":
            # Check if pics folder exists
            if not os.path.exists(pics_folder):
                logger.error(f"Folder '{pics_folder}' not found.")
                raise FileNotFoundError(f"Folder '{pics_folder}' not found.")
                
            # Get the list of image files
            self.image_files = self._get_sorted_image_files()
            if not self.image_files:
                logger.error(f"No image files found in '{pics_folder}' folder.")
                raise FileNotFoundError(f"No image files found in '{pics_folder}' folder.")
            
            logger.info(f"Found {len(self.image_files)} images in the folder.")
        else:
            # Create temp folder for clock images if it doesn't exist
            self.temp_folder = "temp_clock"
            if not os.path.exists(self.temp_folder):
                os.makedirs(self.temp_folder)
        
    def _get_sorted_image_files(self):
        """Get a sorted list of image files from the pics folder."""
        # Get all common image file types
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(self.pics_folder, ext)))
        
        # Sort the files numerically if they have numeric names
        try:
            image_files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
        except ValueError:
            # If files can't be sorted numerically, sort them alphabetically
            image_files.sort()
            
        return image_files
    
    def setup_browser(self):
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
        """Wait for user to scan the QR code and log in."""
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
        """Open the profile pane."""
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
    
    def _check_for_upload_option(self):
        """Check if the upload photo option is visible."""
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
        """Upload a new profile picture."""
        try:
            # Find and use the file input
            file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_input.send_keys(os.path.abspath(image_path))
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
    
    def create_clock_image(self):
        """Create a clock image showing current India time."""
        # Get current time in India
        india_tz = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(india_tz)
        hour = current_time.hour % 12
        minute = current_time.minute
        second = current_time.second

        # Create a square image with white background (256x256)
        size = 256
        image = Image.new('RGB', (size, size), 'white')
        draw = ImageDraw.Draw(image)

        # Calculate center and radius
        center = (size/2, size/2)
        radius = size/2 - 10  # Slightly larger radius since we removed markers

        # Draw hour hand
        hour_angle = (hour + minute/60) * 30 * math.pi / 180
        hour_length = radius * 0.5
        hour_end = (center[0] + hour_length * math.sin(hour_angle),
                   center[1] - hour_length * math.cos(hour_angle))
        draw.line([center, hour_end], fill='black', width=8)  # Thicker hour hand

        # Draw minute hand
        minute_angle = minute * 6 * math.pi / 180
        minute_length = radius * 0.7
        minute_end = (center[0] + minute_length * math.sin(minute_angle),
                     center[1] - minute_length * math.cos(minute_angle))
        draw.line([center, minute_end], fill='black', width=4)  # Thicker minute hand

        # Draw second hand
        second_angle = second * 6 * math.pi / 180
        second_length = radius * 0.9  # Longer than minute hand
        second_end = (center[0] + second_length * math.sin(second_angle),
                     center[1] - second_length * math.cos(second_angle))
        draw.line([center, second_end], fill='red', width=2)  # Thin red second hand

        # Draw center dot
        dot_radius = 8
        draw.ellipse([center[0]-dot_radius, center[1]-dot_radius,
                     center[0]+dot_radius, center[1]+dot_radius],
                     fill='black')

        # Save the image
        filename = os.path.join(self.temp_folder, "clock.png")
        image.save(filename)
        return filename

    def run(self):
        """Run the profile picture changing process."""
        try:
            self.setup_browser()
            
            if not self.wait_for_login():
                logger.error("Login failed. Exiting.")
                self.cleanup()
                return
            
            # Main loop for changing profile pictures
            current_index = 0
            
            while True:
                try:
                    # Open profile pane
                    if not self.open_profile_pane():
                        logger.error("Failed to open profile pane. Retrying in 5 seconds...")
                        time.sleep(5)
                        continue
                    
                    # Check if upload option is available
                    if not self._check_for_upload_option():
                        logger.error("Upload option not found. Retrying in 5 seconds...")
                        time.sleep(5)
                        continue
                    
                    # Get the image to upload
                    if self.mode == "sequence":
                        # Get the next image in sequence
                        image_path = self.image_files[current_index]
                        current_index = (current_index + 1) % len(self.image_files)
                    else:  # clock mode
                        # Create a clock image
                        image_path = self.create_clock_image()
                    
                    # Upload the profile picture
                    if not self.upload_profile_picture(image_path):
                        logger.error("Failed to upload profile picture. Retrying in 5 seconds...")
                        time.sleep(5)
                        continue
                    
                    logger.info(f"Successfully changed profile picture. Waiting {self.duration} seconds before next change.")
                    time.sleep(self.duration)
                    
                except Exception as e:
                    logger.error(f"Error in main loop: {str(e)}")
                    logger.info("Retrying in 5 seconds...")
                    time.sleep(5)
                    
        except KeyboardInterrupt:
            logger.info("Process interrupted by user.")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up resources...")
        if self.driver:
            self.driver.quit()
        
        # Remove temporary clock images if in clock mode
        if self.mode == "clock" and os.path.exists(self.temp_folder):
            try:
                for file in os.listdir(self.temp_folder):
                    file_path = os.path.join(self.temp_folder, file)
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                os.rmdir(self.temp_folder)
                logger.info(f"Removed temporary folder: {self.temp_folder}")
            except Exception as e:
                logger.error(f"Error cleaning up temp folder: {str(e)}")

if __name__ == "__main__":
    # Create and run the WhatsApp profile changer
    # You can customize these parameters
    changer = WhatsAppProfileChanger(
        pics_folder="pics",  # Folder containing profile pictures
        duration=5,          # Duration in seconds to display each picture
        mode="sequence"      # Either "sequence" or "clock"
    )
    changer.run()