#!/usr/bin/env python3
"""
Entry point for WhatsApp Profile Changer.
"""

import os
import sys
import argparse
import logging
from whatsapp_profile_changer.profile_changer import ProfileChanger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='WhatsApp Profile Changer - Change your WhatsApp Web profile picture automatically.'
    )
    
    parser.add_argument(
        '-c', '--config',
        help='Path to configuration file',
        default=None
    )
    
    parser.add_argument(
        '-m', '--mode',
        help='Mode: "sequence" or "clock"',
        choices=['sequence', 'clock'],
        default=None
    )
    
    parser.add_argument(
        '-d', '--duration',
        help='Duration in seconds to display each picture',
        type=int,
        default=None
    )
    
    parser.add_argument(
        '-p', '--pics-folder',
        help='Folder containing profile pictures',
        default=None
    )
    
    return parser.parse_args()

def main():
    """Main entry point."""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Create profile changer
        changer = ProfileChanger(config_file=args.config)
        
        # Override settings from command line if provided
        if args.mode:
            changer.mode = args.mode
            logger.info(f"Overriding mode from command line: {args.mode}")
        
        if args.duration:
            changer.duration = args.duration
            logger.info(f"Overriding duration from command line: {args.duration}")
        
        if args.pics_folder:
            changer.pics_folder = args.pics_folder
            logger.info(f"Overriding pics folder from command line: {args.pics_folder}")
        
        # Run the profile changer
        changer.run()
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user.")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())