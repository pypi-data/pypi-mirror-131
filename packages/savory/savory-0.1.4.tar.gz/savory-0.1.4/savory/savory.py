from ruamel.yaml import YAML
from savory.exceptions import SavoryException
from os import path, mkdir
from git import Repo


class Savory:
    def __init__(self, repository_file=""):
        self.repository_file = repository_file
        self.repositories = None
        self.repository_destination = None
        self.repository_type = None
        self.repository_file_contents = None

        if repository_file:
            self.load_repository_file()

    def load_repository_file(self):
        try:
            yaml = YAML()
            with open(self.repository_file, "r") as fh:
                content = yaml.load(fh)
        except Exception as err:
            raise SavoryException(str(err))

        defaults = content.get("defaults")
        self.repository_destination = defaults.get("destination", ".")
        self.repository_type = defaults.get("type", "formula")

        self.repositories = content.get("repositories", [])
        self.repository_file_contents = content

    def repo_update_with_tag(self, repository: str, config: dict, repo_obj):
        origin = repo_obj.remotes.origin
        repository_type = config.get("type", self.repository_type)
        alias = config.get("alias", None)
        type_description = f"{repository_type} repo:"
        repo_display = f"{repository}{'(' + alias + ')' if alias else ''}"
        
        tag_exists = config["tag"] in repo_obj.tags
        current_tag = repo_obj.git.tag("--points-at", "HEAD")

        if tag_exists:
            if current_tag != config["tag"]:
                print(f"Switching {type_description} {repo_display} from {current_tag} to {config['tag']}")
                repo_obj.git.checkout(config["tag"])

        else:
            print(f"Updating {type_description} {repo_display} from {current_tag} to {config['tag']}")
            origin.fetch()
            repo_obj.git.checkout(config["tag"])

    def repo_update_with_branch(self, repository: str, config: dict, repo_obj):
        origin = repo_obj.remotes.origin
        repository_type = config.get("type", self.repository_type)
        alias = config.get("alias", None)
        type_display = f"{repository_type} repo:"
        repo_display = f"{repository}{'(' + alias + ')' if alias else ''}"

        repo_obj.git.checkout(config["tag"])
        local_hash = repo_obj.head.object.hexsha
        origin.fetch()
        remote_hash = origin.refs[str(repo_obj.active_branch)].object.hexsha
        changed = remote_hash != local_hash

        if changed:
            print(f"Updating {type_display} {repo_display}")
            repo_obj.git.pull("--ff-only")

    def repo_clone(self, repository: str, config: dict):
        repository_destination = config.get("destination", self.repository_destination)
        repository_type = config.get("type", self.repository_type)
        alias = config.get("alias", None)
        type_display = f"{repository_type} repo:"
        alias_display = f"{' as ' + alias if alias else ''}"

        print(f"Cloning {type_display} {repository} in {repository_destination}{alias_display}")
        repo = Repo.clone_from(config["repo"], f"{repository_destination}/{alias if alias else repository}")
        repo.git.checkout(config["tag"])

    @staticmethod
    def repodir_create(repository_destination):
        try:
            mkdir(repository_destination)
        except Exception as err:
            raise SavoryException(f"failed to create directory {str(err)}")

    def repo_update(self, repository: str, config: dict):
        repository_destination = config.get("destination", self.repository_destination)
        alias = config.get("alias", repository)
        repo_display = f"{repository}{'(' + alias + ')' if alias else ''}"

        try:
            if not path.exists(repository_destination):
                self.repodir_create(repository_destination)

            if path.exists(f"{repository_destination}/{alias}"):
                repo = Repo(f"{repository_destination}/{alias}")
                if repo.head.is_detached:  # handle tag
                    self.repo_update_with_tag(repository=repository, config=config, repo_obj=repo)
                elif str(repo.active_branch) in ['master', 'main'] and config['tag'] not in ['master', 'main']:  # recover from missing tags etc.
                    print(f"Attempting to switch from branch {repo.active_branch} to {config['tag']}")
                    repo.git.checkout(config["tag"])
                else:  # handle branch
                    self.repo_update_with_branch(repository=repository, config=config, repo_obj=repo)
            else:
                self.repo_clone(repository=repository, config=config)

        except KeyError as err:
            raise SavoryException(f"key: {str(err)} missing in repo config of repository: {repository}")
        except Exception as err:
            raise SavoryException(f"failed to fetch repo: {config['repo']} for repository: {repo_display} {str(err)}")

    def update(self):
        for repository in self.repositories:
            repo_config = self.repository_file_contents.get(repository, None)

            if repo_config:
                self.repo_update(repository=repository, config=repo_config)
            else:
                print(f"WARNING: skipping {repository} repo config is missing")
