import json
import logging

import yaml

import Question


def data_from_file( fileString: str):
    logging.debug(f"Reading data from {fileString}")
    with open(fileString, 'r') as f:

        # Try to load JSON from file
        try:
            data = json.load(f)
            logging.debug(f"JSON data loaded.")

        except ValueError:
            # If JSON fails then it is passed to the YAML handler
            try:
                data = yaml.full_load(f)
                logging.debug(f"YAML data loaded.")

            except yaml.YAMLError:
                pass
        else:  # Success Block
            return data

        raise ValueError(f"Invalid data in {fileString}. Please make sure it is valid JSON or YAML. ")


def data_from_dict(data_dict: dict):

    try:
        logging.debug(msg=data_dict)
        questions = {ID: Question.Question(ID, question) for ID, question in data_dict.items()}

        return questions

    except Exception as e:
        raise ValueError(f"Invalid data in configuration. {e}. ")
