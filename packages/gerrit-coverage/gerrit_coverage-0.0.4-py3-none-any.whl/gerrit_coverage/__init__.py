from gerrit_coverage.gerrit_coverage import CommentMissingLinesBot
import os

def main():
    import argparse
    parser = argparse.ArgumentParser(description='comment_missing_lines_bot: A bot, that thakes a coverage-run result, checks if any missing lines are in the current diff and commends them in Gerrit.')
    parser.add_argument('repo', type=str, help='URL of the repo.')
    parser.add_argument('--username', type=str, help='The Gerrit-Username for the user that creates the comments, e.g. gerritadmin. If not set the environment-variable GERRIT_USER is used')
    parser.add_argument('--password', type=str, help='Users password. If not set, the env variable GERRIT_PASSWORD is used')
    args = parser.parse_args()

    parts = args.repo.split('/')
    project = parts[-1]
    gerrit_domain = '/'.join(parts[:-1])

    bot = CommentMissingLinesBot(
        gerrit_domain, project, 
        args.username or os.environ.get('GERRIT_USER'), 
        args.password or os.environ.get('GERRIT_PASSWORD')) 
    bot.review(change_id=os.environ.get('GERRIT_CHANGE_ID'))