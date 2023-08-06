gerrit_review_robot
===================

A framework for writing bots, that review a code base and post 
the review together with comments to Gerrit. To write a bot, 
inherit `GerritReviewRobot`:

```python
class CheckStyle(GerritReviewRobot):
    # these two are optional: for documentation and the command-line
    name = "Check Style" 
    description = "Uses Flake8 to lint the current change"

    def _do_review(self, review):
        # pass self.diff_lines so that we do not have to analyze files that
        # are not part of the current change
        for error in self._find_linting_errors_in_files(self.diff_files)
            # only include lines in current diff
            if (error.file, error.line_number) in self.diff_lines:
                review.add_comment(
                    error.file, # relative path
                    (error.line_number, error.line_number), # from_line, to_line
                    error.message # message shown in the comment
                )

    def _find_linting_errors_in_files(self, files):
        pass # here comes the actual logic

```