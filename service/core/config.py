import os

from starlette.datastructures import CommaSeparatedStrings

ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv('ALLOWED_HOSTS', ''))
PROJECT_NAME = 'madlib'
WORDS_URL = 'https://reminiscent-steady-albertosaurus.glitch.me/'
RESPONSE_TEMPLATE = 'It was a {adjective} day. I went downstairs to see if I could {verb} dinner. ' \
                    'I asked, "Does the stew need fresh {noun}?"'
