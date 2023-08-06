from collections import defaultdict
import argparse
from gerrit_review_robot.gerrit import Gerrit
import os


class GerritReviewRobot:
    """
    This is a base class for bots that review the code 
    base and create comments in gerrit. Subclasses only
    have to implement `_do_review` (and `_init_args` if 
    whished). The subclass uses argv to configure itself.
    """
    
    def __call__(self):
        self._configure()
        review = Review(change_id=self.change_id, message=self._generate_description())
        self._do_review(review)
        self.gerrit.send_review(review)

    def _init_parser(self, _parser):
        """
        Subclasses can add their args here to the command line-parser
        """
        pass

    def _do_review(self, review):
        raise NotImplementedError()

    @property
    def diff_lines(self):
        if not hasattr(self, '__diff_lines'):
            self.__diff_lines = set()
        return self.__diff_lines

    @property
    def diff_files(self):
        return set([l[0] for l in self.diff_lines])


    def _configure(self):
        parser = argparse.ArgumentParser(description=self._generate_description())
        parser.add_argument('repo', type=str, help='URL of the repo.')
        parser.add_argument('--username', type=str, help='The Gerrit-Username for the user that creates the comments, e.g. gerritadmin. If not set the environment-variable GERRIT_USER is used')
        parser.add_argument('--password', type=str, help='Users password. If not set, the env variable GERRIT_PASSWORD is used')
        self._init_parser(parser)
        self.args = parser.parse_args()

        parts = self.args.repo.split('/')
        project = parts[-1]
        gerrit_domain = '/'.join(parts[:-1])


        self.change_id = os.environ.get('GERRIT_CHANGE_ID') or self.__parse_current_change_id()

        self.gerrit = Gerrit(
                gerrit_domain, 
                project
            ).with_auth(
                self.args.username or os.environ.get('GERRIT_USER'), 
                self.args.password or os.environ.get('GERRIT_PASSWORD'))
        self.is_configured = True

    def __parse_current_change_id(self):
        last_commit_message = self._run('git log -1 --pretty=%B')
        for line in last_commit_message.split('\n'):
            if line.startswith('Change-Id:'):
                return line.replace('Change-Id:', '').strip()

    def _generate_description(self):
        name = self.name if hasattr(self, 'name') else self.__class__.name
        description = self.description if hasattr(self, 'description') else ''
        if description:
            name += ': ' + description
        return name

    

class Review:

    def __init__(self, change_id, message='', revision_id='current'):
        self.message = message
        self.rating = -1
        self._comments = defaultdict(list)
        self.revision_id = revision_id
        self.change_id = change_id

    def comment(self, file, line_range, message):
        '''
        line_range is a tuble with (start, end)
        '''
        if isinstance(line_range, int):
            start_line = line_range
            end_line = line_range
        else:
            start_line = line_range[0]
            end_line = line_range[1]

        self._comments[file].append({
            'message': message,
            'range': {
                'start_line': start_line,
                'end_line': end_line,
                # 'start_character': 0,
                # 'end_character': 20
            },
            'unresolved': True
        })

    @property
    def comments(self):
        return dict(self._comments)
