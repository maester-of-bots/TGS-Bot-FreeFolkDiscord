import praw
import os
from dotenv import load_dotenv

# New lines
x = {"caraxes-bot": {
        "keywords": ["caraxes"],
        "quotes": [
            '*EEEEEeeeeEeeEeEEeeeeeee*',
            '**EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE**',
            '*Eeeeee.  Eeeeeee eee eeeee ee eeeeee, eee eeeee.*',
            '*eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee*',
            '**EEEEEEEEEEEEEEEEEEE EEEEEEE EEEEEEEEEEE**'
        ]
    }
}



load_dotenv()
reddit = praw.Reddit(
                    client_id=os.getenv("vizzy_client_id"),
                    client_secret=os.getenv("vizzy_client_secret"),
                    password=os.getenv("vizzy_password"),
                    user_agent=os.getenv("vizzy_user_agent"),
                    username=os.getenv("vizzy_username"))

reference = 'https://www.reddit.com/r/freefolk/comments/byko9d/is_there_a_full_list_of_current_and_disabled_bots/?utm_source=share&utm_medium=android_app&utm_name=androidcss&utm_term=1&utm_content=share_button'



to_clone = {}
username_list = [
]


for bot in username_list:
    try:
        print(f"Cloning {bot}")
        to_clone[bot] = []
        for comment in reddit.redditor(bot).comments.top(time_filter='all'):
            to_clone[bot].append(comment.body)

        final = "\n".join(to_clone[bot])

        with open(f'{bot}.txt','w', encoding='UTF-8') as file:
            file.writelines(final)
    except Exception as e:
        print(e)