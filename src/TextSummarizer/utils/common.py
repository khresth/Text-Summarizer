import os
import yaml
from box import ConfigBox
from pathlib import Path
from textSummarizer.logging import logger
from box.exceptions import BoxValueError
from typing import List
from ensure import ensure_annotations

class DirectoryCreationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:

    if not path_to_yaml.exists():
        raise ValueError(f"YAML file {path_to_yaml} does not exist.")

    try:
   
        with open(path_to_yaml, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
        
  
        if not content:
            raise ValueError("YAML file is empty.")
        

        logger.info(f"YAML file {path_to_yaml} loaded successfully.")
        
      
        return ConfigBox(content)

    except yaml.YAMLError as e:
        logger.error(f"YAML parsing error: {str(e)}")
        raise ValueError(f"Error parsing YAML file: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise e


@ensure_annotations
def create_directories(path_to_directories: List[Path], verbose: bool = True) -> None:

    for path in path_to_directories:
        try:

            path.mkdir(parents=True, exist_ok=True)
            
            if verbose:
                logger.info(f"Directory created at: {path}")
        except PermissionError:
            logger.error(f"Permission denied: {path}")
            raise ValueError(f"Permission denied while creating directory: {path}")
        except Exception as e:
            logger.error(f"Failed to create directory {path}: {str(e)}")
            raise ValueError(f"Error creating directory {path}: {str(e)}")


@ensure_annotations
def get_size(path: Path) -> str:

    try:

        if not path.exists():
            raise ValueError(f"File {path} does not exist.")
        

        size_in_kb = round(os.path.getsize(path) / 1024, 2)
        
        logger.info(f"File {path} size: ~ {size_in_kb} KB")
        return f"~ {size_in_kb} KB"
    
    except Exception as e:
        logger.error(f"Error getting file size for {path}: {str(e)}")
        raise ValueError(f"Error getting file size for {path}: {str(e)}")
