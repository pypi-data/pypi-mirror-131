from gerrit_review_robot import GerritReviewRobot
from gerrit_review_robot.helpers import condense
from not_covered_lines import not_covered_lines
from pprint import pprint
from easy_exec import exec


class ReviewStyleGerrit(GerritReviewRobot):

    def _do_review(self, review):
        files = ' '.join(self.diff_files)
        output, stderr, has_error = exec(f'./env/bin/python3 -m pylama {files} --linters=mccabe,pep257,pep8,pyflakes,pylint,isort')
        
        review.message = 'The Style-Checker found some issues'

        for line in output.split('\n'):
            parts = line.split(' ', maxsplit=1)
            if len(parts) < 2:
                continue
            location, message = parts
            filename, linenumber, _position_in_line = location.split(':')
            linenumber = int(linenumber)
            if (filename, linenumber) in self.diff_lines:
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