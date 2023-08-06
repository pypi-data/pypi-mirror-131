import requests
import json 


class Gerrit:

    def __init__(self, base_url, project_name, branch='master'):
        self.base_url = base_url
        self.project_name = project_name
        self.branch = branch
        self.use_auth = False

    def with_auth(self, username, http_password):
        """
        On how to create the http_password:
        https://stackoverflow.com/questions/35361276/gerrit-authentication-required
        or the README.md
        """
        self.username = username
        self.password = http_password
        self.use_auth = True
        return self

    ### 

    def send_review(self, review):
        path = f'/a/changes/{review.change_id}/revisions/{review.revision_id}/review'
        params = {
            'tag': 'jenkins',
            'message': review.message,
            'labels': {
                'Code-Review': review.rating
            },
            'comments': review.comments
        }
        return self._post(path, params)

    ###

    def _post(self, path, params):
        url = self.base_url + path
        res = requests.post(
            url=url,
            json=params,
            auth=(self.username, self.password) if self.use_auth else None,
            headers={'Accept': 'application/json'}
        )
        res = res.content.decode()
        # see https://gerrit-review.googlesource.com/Documentation/rest-api.html#output
        XSSI_prefix = ")]}'\n"
        res = res[len(XSSI_prefix):]
        res = json.loads(res)
        return res

    def _put(self, path, params):
        url = self.base_url + path
        res = requests.put(
            url=url,
            json=params,
            auth=(self.username, self.password) if self.use_auth else None,
            headers={'Accept': 'application/json'}
        )
        res = res.content.decode()
        # see https://gerrit-review.googlesource.com/Documentation/rest-api.html#output
        XSSI_prefix = ")]}'\n"
        res = res[len(XSSI_prefix):]
        res = json.loads(res)
        return res

    def _get(self, path):
        url = self.base_url + path
        res = requests.get(
            url=url,
            auth=(self.username, self.password) if self.use_auth else None,
            headers={'Accept': 'application/json'},
        )
        res = res.content.decode()
        # see https://gerrit-review.googlesource.com/Documentation/rest-api.html#output
        XSSI_prefix = ")]}'\n"
        res = res[len(XSSI_prefix):]
        res = json.loads(res)
        return res

class GerritFake:

    def __init__(self):
        self.reviews = []

    def send_review(self, review):
        self.reviews.append(review)