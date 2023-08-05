from missing_diff_lines import missing_diff_lines
from gerrit_coverage.condense import condense
from gerrit_robo import Review, Gerrit
import subprocess
from pprint import pprint

class ReviewBot:
    
    def __init__(self, gerrit_url, gerrit_project, username, http_credentials):
        self.gerrit_url = gerrit_url
        self.gerrit_project = gerrit_project
        self.username = username
        self.http_credentials = http_credentials
        self.gerrit = Gerrit(gerrit_url, gerrit_project).with_auth(username, http_credentials)
        

    def review(self, path='.', change_id=None):
        if not change_id:
            change_id = self.__parse_current_change_id(path)
        review = self._do_review(path)
        if not review.comments:
            print('Nothing found')
            review.rating = 1
            review.message = 'Checked coverage: Looks good to me'
        else:
            print('found')
            pprint(review.comments)

        self._send_review(change_id, review)

    def _do_review(self, path):
        raise NotImplementedError

    def _send_review(self, change_id, review):
        self.gerrit.send_review(change_id, review)

    def __parse_current_change_id(self, cwd):
        last_commit_message = self.__run('git log -1 --pretty=%B', cwd='.')
        for line in last_commit_message.split('\n'):
            if line.startswith('Change-Id:'):
                return line.replace('Change-Id:', '').strip()
        

    def __run(self, command, cwd):
        return subprocess.check_output(command.split(), cwd=cwd).decode()


class CommentMissingLinesBot(ReviewBot):

    def _do_review(self, path): # TODO: remove path arg
        lines = missing_diff_lines()
        condensed_lines = condense(lines)
        review = self._condensed_lines_to_review(condensed_lines)
        return review

    def _condensed_lines_to_review(self, lines):
        review = Review('test-coverage found some untested files')
        for filename, line_range in lines:
            message = 'These lines are'
            if line_range[0] == line_range[1]:
                message = 'This line is'
            message += ' not covered by any test'
            review.comment(filename, line_range, message)
        return review


def condensed_lines_to_review(lines):
    review = Review('test-coverage found some untested files')
    for filename, line_range in lines:
        message = 'These lines are'
        if line_range[0] == line_range[1]:
            message = 'This line is'
        message += ' not covered by any test'
        review.comment(filename, line_range)

# lines = missing_diff_lines()
# condensed_lines = condense(lines)
# review = condensed_lines_to_review(condensed_lines)