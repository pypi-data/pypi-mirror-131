from typing import Dict

from conans.cli.api.model import Remote, PackageConfiguration
from conans.cli.conan_app import ConanApp
from conans.model.package_ref import PkgReference
from conans.model.recipe_ref import RecipeReference
from conans.search.search import get_packages_search_info


class ListAPI:
    """
    Get references from the recipes and packages in the cache or a remote
    """

    def __init__(self, conan_api):
        self.conan_api = conan_api

    def recipe_revisions(self, ref: RecipeReference, remote=None):
        assert ref.revision is None, "recipe_revisions: ref already have a revision"
        app = ConanApp(self.conan_api.cache_folder)
        if remote:
            results = app.remote_manager.get_recipe_revisions_references(ref, remote=remote)
        else:
            results = app.cache.get_recipe_revisions_references(ref, only_latest_rrev=False)

        return results

    def package_revisions(self, pref: PkgReference, remote: Remote=None):
        assert pref.ref.revision is not None, "package_revisions requires a recipe revision, " \
                                              "check latest first if needed"
        app = ConanApp(self.conan_api.cache_folder)
        if remote:
            results = app.remote_manager.get_package_revisions_references(pref, remote=remote)
        else:
            refs = app.cache.get_package_revisions_references(pref, only_latest_prev=False)
            results = []
            for ref in refs:
                timestamp = app.cache.get_package_timestamp(ref)
                ref.timestamp = timestamp
                results.append(ref)
        return results

    def packages_configurations(self, ref: RecipeReference,
                                remote=None) -> Dict[PkgReference, PackageConfiguration]:
        assert ref.revision is not None, "packages: ref should have a revision. " \
                                         "Check latest if needed."
        if not remote:
            app = ConanApp(self.conan_api.cache_folder)
            prefs = app.cache.get_package_references(ref)
            packages = get_packages_search_info(app.cache, prefs)
            results = {pref: PackageConfiguration(data) for pref, data in packages.items()}
        else:
            app = ConanApp(self.conan_api.cache_folder)
            packages = app.remote_manager.search_packages(remote, ref)
            results = {pref: PackageConfiguration(data) for pref, data in packages.items()}
        return results
