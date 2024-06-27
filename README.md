# PyQuest

PyQuest is a linked list based question and answer platform for your terminal. This acts very similar to quest lines
where each answer correlates to specific paths Ever find yourself in need of a Q&A loop for your program? Here's the
solution! Build out a JSON or YAML file with your questions and answers, choose a display and get back the answers.

## Coming Features
In no particular order here are some addtional features I plan to implement. If you have a feature please request it in the issues section.

- Standard I/O based modules
- New Question and Answer Types:
  - Free Text
  - Select all that apply
  - Optional Questions
- Second Screen for Cruses based modules to print info to
- Encrypted answer templates
- Scored quests
- PyQuest Builder, to aid in mapping your quest
  _I know the current config is messy to make manually, but I plan to make a builder to assist and visualize_  

## Installation

It is highly recommended to install from Pip.

### From pip

```bash
pip install pyquest
```

### Build from source

```bash
git clone https://github.com/causeImCloudy/PyQuest.git
cd PyQuest
python -m build
pip install dist/PyQuest<>.whl
```

## Configuration

The base configuration is a JSON or YAML file.

```json
{
  "first_question": "1",
  "timed": false,
  "scored": false,
  "<ID>": {
    "question": {
      "viewable_text": "What is your name?",
      "next_question": "<NEXT_QUESTION_ID>",
      #
      Null
      means
      disabled
      "previous_question": "<PREV_QUESTION_ID>",
      #
      Null
      means
      disabled
      "validator": {
        #
      This
      is
      only
      used
      with
      some
      printer
      formats
      "type": "REGEX/DIGIT/MATH",
      "regex": "/d"
    }
  },
  "answers": [
    {
      "viewable_text": "John"
    },
    {
      "viewable_text": "Bob",
      "value": 2
    },
    {
      "viewable_text": "Fred",
      "value": 2,
      "validator": {
      }
    }
  ]
},
"<ID2>": {
}
}

```

## Usage

PyQuest can be used in the command line or from within your application.

### Command Line

PyQuest can be used u

```bash
usage: PyQuest.py [-h] [-q QUESTIONS] [-D] -i CONFIG [-t] [-p]

options:
  -h, --help            show this help message and exit
  -q QUESTION, --question QUESTION
                        Question to ask first
  -D, --debug           Enable debug logging of the command line. This is logged to log.txt
  -i CONFIG, --config CONFIG
                        Path to the configuration file.
  -t, --timed           WIP!!! Force timed completion of the quest.
  -p, --scored          WIP!!! Scored completion of the quest.
```


