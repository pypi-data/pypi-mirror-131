from gerrit_review_robot import GerritReviewRobot
from gerrit_review_robot.helpers import condense
from not_covered_lines import not_covered_lines
from pprint import pprint


class ReportNotCoveredLines(GerritReviewRobot):

    def _do_review(self, review):
        lines = not_covered_lines('.').intersection(self.diff_lines) 
        review = self._add_lines_to_review(review, lines)

        if not review.comments:
            print('Nothing found')
            review.rating = 1
            review.message = 'Checked coverage: Looks good to me'
        else:
            print('Found some not covered lines')
            pprint(review.comments)

        return review

    def _add_lines_to_review(self, review, lines):
        lines = condense(lines)
        review.message = 'test-coverage found some untested files'
        for filename, line_range in lines:
            message = 'These lines are'
            if line_range[0] == line_range[1]:
                message = 'This line is'
            message += ' not covered by any test'
            review.comment(filename, line_range, message)
        return review
