"""
Configuration module for WhatsApp Profile Changer.
"""

import os
import configparser
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Config:
    """Configuration handler for WhatsApp Profile Changer."""
    
    def __init__(self, config_file=None):
        """
        Initialize configuration.
        
        Args:
            config_file (str, optional): Path to the configuration file. If None, 
                                         will look for config.ini in the current directory.
        """
        self.config = configparser.ConfigParser()
        
        # Default configuration
        self.pics_folder = "pics"
        self.duration = 5
        self.mode = "sequence"
        self.timeout = 300
        self.temp_folder = "temp_clock"
        
        # Try to load configuration from file
        if config_file is None:
            # Look for config.ini in the current directory and parent directory
            possible_locations = [
                "config.ini",
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini"),
                os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.ini")
            ]
            
            for location in possible_locations:
                if os.path.exists(location):
                    config_file = location
                    break
        
        if config_file and os.path.exists(config_file):
            self._load_config(config_file)
            logger.info(f"Loaded configuration from {config_file}")
        else:
            logger.info("No configuration file found, using default settings")
    
    def _load_config(self, config_file):
        """
        Load configuration from file.
        
        Args:
            config_file (str): Path to the configuration file.
        """
        try:
            self.config.read(config_file)
            
            # Get settings from config file
            if 'Settings' in self.config:
                settings = self.config['Settings']
                self.pics_folder = settings.get('pics_folder', self.pics_folder)
                self.duration = settings.getint('duration', self.duration)
                self.mode = settings.get('mode', self.mode)
                self.timeout = settings.getint('timeout', self.timeout)
                self.temp_folder = settings.get('temp_folder', self.temp_folder)
                
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            logger.info("Using default settings")
    
    def get_settings(self):
        """
        Get all settings as a dictionary.
        
        Returns:
            dict: Dictionary containing all settings.
        """
        return {
            'pics_folder': self.pics_folder,
            'duration': self.duration,
            'mode': self.mode,
            'timeout': self.timeout,
            'temp_folder': self.temp_folder
        }