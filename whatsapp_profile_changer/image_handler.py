"""
Image handler module for WhatsApp Profile Changer.
"""

import os
import glob
import logging
import math
from datetime import datetime
import pytz
from PIL import Image, ImageDraw

# Configure logging
logger = logging.getLogger(__name__)

class ImageHandler:
    """Handler for image operations."""
    
    def __init__(self, pics_folder="pics", temp_folder="temp_clock"):
        """
        Initialize the image handler.
        
        Args:
            pics_folder (str): Folder containing profile pictures.
            temp_folder (str): Folder for temporary clock images.
        """
        self.pics_folder = pics_folder
        self.temp_folder = temp_folder
        self.image_files = []
        
        # Ensure the pics folder exists
        if not os.path.exists(pics_folder):
            logger.error(f"Folder '{pics_folder}' not found.")
            raise FileNotFoundError(f"Folder '{pics_folder}' not found.")
        
        # Create temp folder for clock images if it doesn't exist
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
            logger.info(f"Created temporary folder: {temp_folder}")
    
    def get_sorted_image_files(self):
        """
        Get a sorted list of image files from the pics folder.
        
        Returns:
            list: Sorted list of image file paths.
        """
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
        
        if not image_files:
            logger.error(f"No image files found in '{self.pics_folder}' folder.")
            raise FileNotFoundError(f"No image files found in '{self.pics_folder}' folder.")
        
        logger.info(f"Found {len(image_files)} images in the folder.")
        self.image_files = image_files
        return image_files
    
    def create_clock_image(self, timezone='Asia/Kolkata'):
        """
        Create a clock image showing current time in the specified timezone.
        
        Args:
            timezone (str): Timezone to use for the clock.
            
        Returns:
            str: Path to the created clock image.
        """
        # Get current time in the specified timezone
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
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
        logger.info(f"Created clock image: {filename}")
        return os.path.abspath(filename)
    
    def cleanup(self):
        """Clean up temporary files."""
        if os.path.exists(self.temp_folder):
            try:
                for file in os.listdir(self.temp_folder):
                    file_path = os.path.join(self.temp_folder, file)
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                os.rmdir(self.temp_folder)
                logger.info(f"Removed temporary folder: {self.temp_folder}")
            except Exception as e:
                logger.error(f"Error cleaning up temp folder: {str(e)}")