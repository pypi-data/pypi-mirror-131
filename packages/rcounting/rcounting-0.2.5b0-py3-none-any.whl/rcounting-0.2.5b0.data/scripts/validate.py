#!python
import pandas as pd
from counting_tools.side_threads import side_threads
from counting_tools.reddit_interface import reddit
from counting_tools.thread_navigation import fetch_comments


if __name__ == "__main__":
    import argparse

    rule_dict = {'default': 'default',
                 'wait2': 'wait 2',
                 'wait3': 'wait 3',
                 'wait9': 'wait 9',
                 'wait10': 'wait 10',
                 'once_per_thread': 'once per thread',
                 'slow': 'slow',
                 'slower': 'slower',
                 'slowestest': 'slowestest',
                 'only_double_counting': 'only double counting'}

    parser = argparse.ArgumentParser(description='Validate the reddit submission which'
                                     ' contains the comment with id `comment_id` according to rule')
    parser.add_argument('comment_id',
                        help='The id of the comment to start logging from')
    parser.add_argument('--rule', choices=rule_dict.keys(),
                        default='default',
                        help='Which rule to apply. Default is no double counting')
    args = parser.parse_args()

    comment = reddit.comment(args.comment_id)
    comments = pd.DataFrame(fetch_comments(comment, use_pushshift=False))
    side_thread = side_threads.get_side_thread(rule_dict[args.rule])
    result = side_thread.is_valid_thread(comments)
    if result[0]:
        print('All counts were valid')
    else:
        print(f'Invalid count found at reddit.com{reddit.comment(result[1]).permalink}!')
