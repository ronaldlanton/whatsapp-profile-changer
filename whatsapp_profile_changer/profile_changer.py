"""
Main profile changer module for WhatsApp Profile Changer.
"""

import os
import time
import logging
from .browser import Browser
from .image_handler import ImageHandler
from .config import Config

# Configure logging
logger = logging.getLogger(__name__)

class ProfileChanger:
    """Main class for WhatsApp Profile Changer."""
    
    def __init__(self, config_file=None):
        """
        Initialize the profile changer.
        
        Args:
            config_file (str, optional): Path to the configuration file.
        """
        # Load configuration
        self.config = Config(config_file)
        settings = self.config.get_settings()
        
        self.pics_folder = settings['pics_folder']
        self.duration = settings['duration']
        self.mode = settings['mode']
        self.timeout = settings['timeout']
        self.temp_folder = settings['temp_folder']
        
        # Initialize components
        self.browser = Browser()
        self.image_handler = None
        
        logger.info(f"Initialized ProfileChanger with mode: {self.mode}, duration: {self.duration}s")
    
    def setup(self):
        """Set up the profile changer."""
        try:
            # Set up image handler
            self.image_handler = ImageHandler(
                pics_folder=self.pics_folder,
                temp_folder=self.temp_folder
            )
            
            # If in sequence mode, get the image files
            if self.mode == "sequence":
                self.image_files = self.image_handler.get_sorted_image_files()
            
            # Set up browser
            self.browser.setup()
            
            return True
        except Exception as e:
            logger.error(f"Error setting up profile changer: {str(e)}")
            return False
    
    def run(self):
        """Run the profile picture changing process."""
        try:
            # Set up components
            if not self.setup():
                logger.error("Setup failed. Exiting.")
                self.cleanup()
                return
            
            # Wait for login
            if not self.browser.wait_for_login(timeout=self.timeout):
                logger.error("Login failed. Exiting.")
                self.cleanup()
                return
            
            # Main loop for changing profile pictures
            current_index = 0
            
            while True:
                try:
                    # Open profile pane
                    if not self.browser.open_profile_pane():
                        logger.error("Failed to open profile pane. Retrying in 5 seconds...")
                        time.sleep(5)
                        continue
                    
                    # Check if upload option is available
                    if not self.browser.check_for_upload_option():
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
                        image_path = self.image_handler.create_clock_image()
                    
                    # Upload the profile picture
                    if not self.browser.upload_profile_picture(image_path):
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
        
        # Clean up browser
        if hasattr(self, 'browser') and self.browser:
            self.browser.cleanup()
        
        # Clean up image handler
        if hasattr(self, 'image_handler') and self.image_handler:
            self.image_handler.cleanup()