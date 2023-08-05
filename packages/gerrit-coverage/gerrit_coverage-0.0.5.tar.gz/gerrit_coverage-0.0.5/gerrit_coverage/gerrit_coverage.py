from missing_diff_lines.missing_diff_lines import missing_diff_lines, Changes
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
        

    def review(self, change_id=None):
        if not change_id:
            change_id = self.__parse_current_change_id()
        review = self._do_review()
        print(review.message)
        print(review.comments)
        #self._send_review(change_id, review)

    def _do_review(self):
        raise NotImplementedError

    def _send_review(self, change_id, review):
        self.gerrit.send_review(change_id, review)

    def __parse_current_change_id(self):
        last_commit_message = self._run('git log -1 --pretty=%B')
        for line in last_commit_message.split('\n'):
            if line.startswith('Change-Id:'):
                return line.replace('Change-Id:', '').strip()
        

    def _run(self, command, cwd='.'):
        return subprocess.run(command.split(), cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False).stdout.decode()


class CommentMissingLinesBot(ReviewBot):

    def _do_review(self):
        lines = missing_diff_lines()
        condensed_lines = condense(lines)
        review = self._condensed_lines_to_review(condensed_lines)

        if not review.comments:
            print('Nothing found')
            review.rating = 1
            review.message = 'Checked coverage: Looks good to me'
        else:
            print('found')
            pprint(review.comments)

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

class CodeStyleBot(ReviewBot):

    def _do_review(self):
        changes = Changes()
        changed_files = changes.changed_files
        changed_lines = changes.changed_lines_lut

        files = ' '.join(changed_files)
        output = self._run(f'pylama {files} --linters=mccabe,pep257,pep8,pyflakes,pylint,isort')
        
        review = Review('The Style-Checker found some issues')

        for line in output.split('\n'):
            parts = line.split(' ', maxsplit=1)
            if len(parts) < 2:
                continue
            location, message = parts
            filename, linenumber, _position_in_line = location.split(':')
            linenumber = int(linenumber)
            if (filename, linenumber) in changed_lines:
                review.comment(filename, (linenumber, linenumber), message)
        
        if not review.comments:
            print('Nothing found')
            review.rating = 1
            review.message = 'Checked Style: Looks good to me'
        else:
            print('Found some style issues')
            review.rating = -1
            pprint(review.comments)

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