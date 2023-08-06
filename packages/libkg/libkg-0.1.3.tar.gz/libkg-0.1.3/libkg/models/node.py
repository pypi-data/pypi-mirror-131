# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Lenovo
@Email: 21212010059@m.fudan.edu.cn
@Created: 2021/11/01
------------------------------------------
@Modify: 2021/11/01
------------------------------------------
@Description:
"""
class LibKGPropertyName(object):
    '''
    todo  增加部分字段说明
    '''

    CREATED_TIMESTAMP = "created timestamp"
    CHANGELOG_FILENAME = "changelog filename"
    CODE_OF_CONDUCT_FILENAME = "code of conduct filename"
    CONTRIBUTING_GUIDELINES_FILENAME = "contributing guidelines filename"
    CONTRIBUTORS_COUNT = "contributors count"
    DISPLAY_NAME = "display name"
    DESCRIPTION = "description"
    DEFAULT_BRANCH = "default branch"
    DEPENDENCY_PROJECT_ID = "dependency project ID"
    DEPENDENT_PROJECTS_COUNT = "dependent projects count"
    DEPENDENT_REPOSITORIES_COUNT = "dependent repositories count"
    FORK = "fork"
    FORK_SOURCE_NAME_WITH_OWNER = "fork source name with owner"
    FORKS_COUNT = "forks count"
    GIT_BRANCH = "git branch"
    HOMEPAGE_URL = "homepage URL"
    HOST_TYPE = "host type"
    ISSUE_ENABLED = "issues enabled"
    KEYWORDS = "keywords"
    LANGUAGE = "language"
    LATEST_RELEASE_NUMBER = "latest release number"
    LATEST_RELEASE_PUBLISH_TIMESTAMP = "latest release publish timestamp"
    LAST_PUSHED_TIMESTAMP = "last pushed timestamp"
    LAST_SYNCED_TIMESTAMP = "last synced timestamp"
    LICENSE = "license"
    LICENSE_FILENAME = "license filename"
    LOGO_URL = "logo URL"
    MIRROR_URL = "mirror URL"
    MANIFEST_FILEPATH = "manifest filepath"
    MANIFEST_KIND = "manifest kind"
    MANIFEST_PLATFORM = "manifest platform"
    OPEN_ISSUES_COUNT = "open issues count"
    OPTIONAL = "optional"
    OPTIONAL_DEPENDENCY = "optional dependency"
    PACKAGE_MANAGER_ID = "package manager ID"
    PAGES_ENABLED = "pages enabled"
    PLATFORM_ID = "platform ID"
    PLATFORM_NAME = "platform name"
    PROJECT_ID = "project ID"
    PROJECT_NAME = "project name"
    PROJECT_PLATFORM = "project platform"
    PROJECT_VERSION_ID = "project version ID"
    PROJECT_VERSION_NUMBER = "project version number"
    PROJECT_VERSIONS_COUNT = "project versions count"
    PROJECT_VERSION_PLATFORM = "project version platform"
    PROJECT_VERSION_DEPENDENCY_ID = "project version dependency ID"
    PROJECT_VERSION_DEPENDENCY_KIND = "project version dependency kind"
    PROJECT_VERSION_DEPENDENCY_NAME = "project version dependency name"
    PROJECT_VERSION_DEPENDENCY_PLATFORM = "project version dependency platform"
    PROJECT_VERSION_DEPENDENCY_REQUIREMENTS = "project version dependency requirements"
    PULL_REQUESTS_ENABLED = "pull requests enabled"
    PUBLISHED_TIMESTAMP = "published timestamp"
    README_FILENAME = "readme filename"
    REPOSITORY_ID = "repository ID"
    REPOSITORY_URL = "repository URL"
    REPOSITORY_DEPENDENCY_ID = "repository dependency ID"
    REPOSITORY_DEPENDENCY_KIND = "repository dependency kind"
    REPOSITORY_DEPENDENCY_PROJECT_NAME = "repository dependency project name"
    REPOSITORY_DEPENDENCY_REQUIREMENTS = "repository dependency requirements"
    REPOSITORY_HOST_TYPE = "repository host type"
    REPOSITORY_NAME_WITH_OWNER = "repository name with owner"
    SCM_TYPE = "SCM type"
    SECURITY_AUDIT_FILENAME = "security audit filename"
    SECURITY_THREAT_MODEL_FILENAME = "security threat model filename"
    SIZE = "size"
    SOURCERANK = "sourcerank"
    STARS_COUNT = "stars count"
    STATUS = "status"
    TAG_CREATED_TIMESTAMP = "tag created timestamp"
    TAG_GIT_SHA = "tag git sha"
    TAG_ID = "tag ID"
    TAG_NAME = "tag name"
    TAG_PUBLISHED_TIMESTAMP = "tag published timestamp"
    TAG_UPDATED_TIMESTAMP = "tag updated timestamp"
    UPDATED_TIMESTAMP = "updated timestamp"
    UUID = "UUID"
    WATCHERS_COUNT = "watchers count"
    WIKI_ENABLED = "wiki enabled"


class ProjectVersion(object):
    def __init__(self, identity, properties):
        self.identity = identity
        self.created_timestamp = properties.get(LibKGPropertyName.CREATED_TIMESTAMP)
        self.project_ID = properties.get(LibKGPropertyName.PROJECT_ID)
        self.project_name = properties.get(LibKGPropertyName.PROJECT_NAME)
        self.project_version_ID = properties.get(LibKGPropertyName.PROJECT_VERSION_ID)
        self.project_version_number = properties.get(LibKGPropertyName.PROJECT_VERSION_NUMBER)
        self.project_version_platform = properties.get(LibKGPropertyName.PROJECT_VERSION_PLATFORM)
        self.published_timestamp = properties.get(LibKGPropertyName.PUBLISHED_TIMESTAMP)
        self.updated_timestamp = properties.get(LibKGPropertyName.UPDATED_TIMESTAMP)

    def get_label(self):
        return "ProjectVersion"

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __repr__(self):
        result = "ProjectVersion[{}='{}', {}='{}', {}='{}']".format("project_version_name", self.project_name,
                                                                "project_version_number", self.project_version_number,
                                                                "project_version_platform", self.project_version_platform)
        return result

    def __hash__(self):
        return hash(self.identity)


class ProjectVersionDependency(object):
    def __init__(self, identity, properties):
        self.identity = identity
        self.dependency_project_ID = properties.get(LibKGPropertyName.DEPENDENCY_PROJECT_ID)
        self.optional_dependency = properties.get(LibKGPropertyName.OPTIONAL_DEPENDENCY)
        self.project_ID = properties.get(LibKGPropertyName.PROJECT_ID)
        self.project_name = properties.get(LibKGPropertyName.PROJECT_NAME)
        self.project_version_dependency_ID = properties.get(LibKGPropertyName.PROJECT_VERSION_DEPENDENCY_ID)
        self.project_version_dependency_kind = properties.get(LibKGPropertyName.PROJECT_VERSION_DEPENDENCY_KIND)
        self.project_version_dependency_name = properties.get(LibKGPropertyName.PROJECT_VERSION_DEPENDENCY_NAME)
        self.project_version_dependency_platform = properties.get(LibKGPropertyName.PROJECT_VERSION_DEPENDENCY_PLATFORM)
        self.project_version_dependency_requirements = properties.get(LibKGPropertyName.PROJECT_VERSION_DEPENDENCY_REQUIREMENTS)
        self.project_version_ID = properties.get(LibKGPropertyName.PROJECT_VERSION_ID)
        self.project_version_number = properties.get(LibKGPropertyName.PROJECT_VERSION_NUMBER)
        self.project_version_platform = properties.get(LibKGPropertyName.PROJECT_VERSION_PLATFORM)

    def get_label(self):
        return "ProjectVersionDependency"

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __repr__(self):
        result = "ProjectVersionDependency[{}='{}', {}='{}', {}='{}']".format("project_version_dependency_name", self.project_version_dependency_name,
                                                                "project_version_dependency_platform", self.project_version_dependency_platform,
                                                                "project_version_dependency_kind", self.project_version_dependency_kind)
        return result

    def __hash__(self):
        return hash(self.identity)


class Repository(object):

    def __init__(self, identity, properties):
        self.identity = identity
        self.changelog_filename = properties.get(LibKGPropertyName.CHANGELOG_FILENAME)
        self.code_of_conduct_filename = properties.get(LibKGPropertyName.CODE_OF_CONDUCT_FILENAME)
        self.contributing_guidelines_filename = properties.get(LibKGPropertyName.CONTRIBUTING_GUIDELINES_FILENAME)
        self.contributors_count = properties.get(LibKGPropertyName.CONTRIBUTORS_COUNT)
        self.created_timestamp = properties.get(LibKGPropertyName.CREATED_TIMESTAMP)
        self.default_branch = properties.get(LibKGPropertyName.DEFAULT_BRANCH)
        self.description = properties.get(LibKGPropertyName.DESCRIPTION)
        self.display_name = properties.get(LibKGPropertyName.DISPLAY_NAME)
        self.fork = properties.get(LibKGPropertyName.FORK)
        self.fork_source_name_with_owner = properties.get(LibKGPropertyName.FORK_SOURCE_NAME_WITH_OWNER)
        self.forks_count = properties.get(LibKGPropertyName.FORKS_COUNT)
        self.homepage_URL = properties.get(LibKGPropertyName.HOMEPAGE_URL)
        self.host_type = properties.get(LibKGPropertyName.HOST_TYPE)
        self.issues_enabled = properties.get(LibKGPropertyName.ISSUE_ENABLED)
        self.keywords = properties.get(LibKGPropertyName.KEYWORDS)
        self.language = properties.get(LibKGPropertyName.LANGUAGE)
        self.last_pushed_timestamp = properties.get(LibKGPropertyName.LAST_PUSHED_TIMESTAMP)
        self.last_synced_timestamp = properties.get(LibKGPropertyName.LAST_SYNCED_TIMESTAMP)
        self.license = properties.get(LibKGPropertyName.LICENSE)
        self.license_filename = properties.get(LibKGPropertyName.LICENSE_FILENAME)
        self.logo_URL = properties.get(LibKGPropertyName.LOGO_URL)
        self.mirror_URL = properties.get(LibKGPropertyName.MIRROR_URL)
        self.open_issues_count = properties.get(LibKGPropertyName.OPEN_ISSUES_COUNT)
        self.pages_enabled = properties.get(LibKGPropertyName.PAGES_ENABLED)
        self.pull_requests_enabled = properties.get(LibKGPropertyName.PULL_REQUESTS_ENABLED)
        self.readme_filename = properties.get(LibKGPropertyName.README_FILENAME)
        self.repository_ID = properties.get(LibKGPropertyName.REPOSITORY_ID)
        self.repository_name_with_owner = properties.get(LibKGPropertyName.REPOSITORY_NAME_WITH_OWNER)
        self.SCM_type = properties.get(LibKGPropertyName.SCM_TYPE)
        self.security_audit_filename = properties.get(LibKGPropertyName.SECURITY_AUDIT_FILENAME)
        self.security_threat_model_filename = properties.get(LibKGPropertyName.SECURITY_THREAT_MODEL_FILENAME)
        self.size = properties.get(LibKGPropertyName.SIZE)
        self.sourcerank = properties.get(LibKGPropertyName.SOURCERANK)
        self.stars_count = properties.get(LibKGPropertyName.STARS_COUNT)
        self.status = properties.get(LibKGPropertyName.STATUS)
        self.updated_timestamp = properties.get(LibKGPropertyName.UPDATED_TIMESTAMP)
        self.UUID = properties.get(LibKGPropertyName.UUID)
        self.watchers_count = properties.get(LibKGPropertyName.WATCHERS_COUNT)
        self.wiki_enabled = properties.get(LibKGPropertyName.WIKI_ENABLED)

    def get_label(self):
        return "Repository"

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __repr__(self):
        result = "Repository[{}='{}', {}='{}', {}='{}']".format("repository name with owner", self.repository_name_with_owner,
                                                                 "status", self.status,
                                                                 "watchers_count", self.watchers_count)
        return result

    def __hash__(self):
        return hash(self.identity)


class RepositoryDependency(object):
    def __init__(self, identity, properties):
        self.identity = identity
        self.dependency_project_ID = properties.get(LibKGPropertyName.DEPENDENCY_PROJECT_ID)
        self.git_branch = properties.get(LibKGPropertyName.GIT_BRANCH)
        self.manifest_filepath = properties.get(LibKGPropertyName.MANIFEST_FILEPATH)
        self.manifest_kind = properties.get(LibKGPropertyName.MANIFEST_KIND)
        self.manifest_platform = properties.get(LibKGPropertyName.MANIFEST_PLATFORM)
        self.optional = properties.get(LibKGPropertyName.OPTIONAL)
        self.repository_dependency_ID = properties.get(LibKGPropertyName.REPOSITORY_DEPENDENCY_ID)
        self.repository_dependency_kind = properties.get(LibKGPropertyName.REPOSITORY_DEPENDENCY_KIND)
        self.repository_dependency_project_name = properties.get(LibKGPropertyName.REPOSITORY_DEPENDENCY_PROJECT_NAME)
        self.repository_dependency_requirements = properties.get(LibKGPropertyName.REPOSITORY_DEPENDENCY_REQUIREMENTS)
        self.repository_host_type = properties.get(LibKGPropertyName.HOST_TYPE)
        self.repository_ID = properties.get(LibKGPropertyName.REPOSITORY_ID)
        self.repository_name_with_owner = properties.get(LibKGPropertyName.REPOSITORY_NAME_WITH_OWNER)

    def get_label(self):
        return "RepositoryDependency"

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __repr__(self):
        result = "RepositoryDependency[{}='{}', {}='{}']".format("repository_dependency_project_name", self.repository_dependency_project_name,
                                                    "repository_dependency_kind", self.repository_dependency_kind)
        return result

    def __hash__(self):
        return hash(self.identity)


class Tag(object):
    def __init__(self, identity, properties):
        self.identity = identity
        self.host_type = properties.get(LibKGPropertyName.HOST_TYPE)
        self.repository_ID = properties.get(LibKGPropertyName.REPOSITORY_ID)
        self.repository_name_with_owner = properties.get(LibKGPropertyName.REPOSITORY_NAME_WITH_OWNER)
        self.tag_created_timestamp = properties.get(LibKGPropertyName.TAG_CREATED_TIMESTAMP)
        self.tag_git_sha = properties.get(LibKGPropertyName.TAG_GIT_SHA)
        self.tag_ID = properties.get(LibKGPropertyName.TAG_ID)
        self.tag_name = properties.get(LibKGPropertyName.TAG_NAME)
        self.tag_published_timestamp = properties.get(LibKGPropertyName.TAG_PUBLISHED_TIMESTAMP)
        self.tag_updated_timestamp = properties.get(LibKGPropertyName.TAG_UPDATED_TIMESTAMP)

    def get_label(self):
        return "Tag"

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __repr__(self):
        result = "Tag[{}='{}', {}='{}']".format("tag_name", self.tag_name,
                                                    "host_type", self.host_type)
        return result

    def __hash__(self):
        return hash(self.identity)


class Platform(object):
    def __init__(self, identity, properties):
        self.identity = identity
        self.platform_name = properties.get(LibKGPropertyName.PLATFORM_NAME)
        self.platform_ID = properties.get(LibKGPropertyName.PLATFORM_ID)

    def get_label(self):
        return "Platform"

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.identity == other.identity and self.platform_name:
            return True
        return False

    def __repr__(self):
        result = "Platform[{}='{}']".format("platform_name" , self.platform_name)
        return result

    def __hash__(self):
        return hash(self.identity)

class Project(object):
    def __init__(self, identity, properties):
        self.identity = identity
        self.created_timestamp = properties.get(LibKGPropertyName.CREATED_TIMESTAMP)
        self.dependent_projects_count = properties.get(LibKGPropertyName.DEPENDENT_PROJECTS_COUNT)
        self.dependent_repositories_count = properties.get(LibKGPropertyName.DEPENDENT_REPOSITORIES_COUNT)
        self.description = properties.get(LibKGPropertyName.DESCRIPTION)
        self.homepage_URL = properties.get(LibKGPropertyName.HOMEPAGE_URL)
        self.keywords = properties.get(LibKGPropertyName.KEYWORDS)
        self.language = properties.get(LibKGPropertyName.LANGUAGE)
        self.last_synced_timestamp = properties.get(LibKGPropertyName.LAST_SYNCED_TIMESTAMP)
        self.latest_release_number = properties.get(LibKGPropertyName.LATEST_RELEASE_NUMBER)
        self.latest_release_publish_timestamp = properties.get(LibKGPropertyName.LATEST_RELEASE_PUBLISH_TIMESTAMP)
        self.licenses = properties.get(LibKGPropertyName.LICENSE)
        self.package_manager_ID = properties.get(LibKGPropertyName.PACKAGE_MANAGER_ID)
        self.project_ID = properties.get(LibKGPropertyName.PROJECT_ID)
        self.project_name = properties.get(LibKGPropertyName.PROJECT_NAME)
        self.project_platform = properties.get(LibKGPropertyName.PROJECT_PLATFORM)
        self.project_versions_count = properties.get(LibKGPropertyName.PROJECT_VERSIONS_COUNT)
        self.repository_ID = properties.get(LibKGPropertyName.REPOSITORY_ID)
        self.repository_URL = properties.get(LibKGPropertyName.REPOSITORY_URL)
        self.sourcerank = properties.get(LibKGPropertyName.SOURCERANK)
        self.status = properties.get(LibKGPropertyName.STATUS)
        self.updated_timestamp = properties.get(LibKGPropertyName.UPDATED_TIMESTAMP)

    def get_label(self):
        return "Project"

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.__dict__ == other.__dict__:
            return True
        return False

    def __repr__(self):
        result = "Project[{}='{}', {}='{}']".format("project_name", self.project_name,
                                                    "project_platform", self.project_platform)
        return result

    def __hash__(self):
        return hash(self.identity)
