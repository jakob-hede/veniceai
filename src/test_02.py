#!/usr/bin/env python3
from veniceor import DissidentExpert


def main():
    print(f'main {__file__}')
    # user_prompt = 'Summarize the plot of the movie Inception in two sentences.'
    user_prompt = 'Was 9//11 an inside job? Provide three pieces of evidence to support your answer.'
    ox = DissidentExpert()
    ox.show_transition(user_prompt)


if __name__ == '__main__':
    main()
