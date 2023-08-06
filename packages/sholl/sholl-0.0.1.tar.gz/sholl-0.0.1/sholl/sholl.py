#!/usr/bin/env python

""" brewzilla

Invoked like "" for some package foo **which is presently
installed in sys.path**, determines which packages foo and its dependents
depend on, downloads them from pypi and computes their checksums, and
spits out Homebrew resource stanzas.
"""

from __future__ import print_function
import argparse
import codecs
from collections import OrderedDict
from contextlib import closing
from hashlib import sha256
import json
import logging
import os
import sys
import warnings

import pkg_resources
import re
from typing import Any, Optional

from .templates import FORMULA_TEMPLATE, RESOURCE_TEMPLATE
from .version import __version__

from urllib.request import urlopen

# Show warnings and greater by default
logging.basicConfig(level=int(os.environ.get("sholl_DEBUG", 30)))


class PackageNotInstalledWarning(UserWarning):
    pass


class PackageVersionNotFoundWarning(UserWarning):
    pass


class ConflictingDependencyWarning(UserWarning):
    pass

def write_output_to_file(text: str, path: str):
    try:
        file=open(path, "w+")
        print(text, file=file)
    except:
        raise FileNotFoundError("File %s does not exist" % path)

def print_output(text: str):
    print(text)

def parse_homebrew_formula_description(text: str) -> str:
    x = re.search("(?<=desc \").*?(?=\")", text)
    if x:
        return x.group()
    else:
        return None

def parse_homebrew_formula_homepage(text: str) -> str:
    x = re.search("(?<=homepage \").*?(?=\")", text)
    if x:
        return x.group()
    else:
        return None

def parse_homebrew_formula_test(text: str) -> str:
    x = re.search("(?<=test do\n    ).*?(?=\n  end)", text, flags=re.DOTALL)
    if x:
        return x.group()
    else:
        return None

def parse_homebrew_formula(path: str) -> tuple[str, str, str]:
    try:
        file = open(path, "r")
    except:
        raise FileNotFoundError("File %s does not exist" % path)
    text = file.read()
    description = parse_homebrew_formula_description(text)
    homepage = parse_homebrew_formula_homepage(text)
    test = parse_homebrew_formula_test(text)
    return description, homepage, test


def recursive_dependencies(package):
    if not isinstance(package, pkg_resources.Requirement):
        raise TypeError("Expected a Requirement; got a %s" % type(package))

    discovered = {package.project_name.lower()}
    visited = set()

    def walk(package):
        if not isinstance(package, pkg_resources.Requirement):
            raise TypeError("Expected a Requirement; got a %s" % type(package))
        if package in visited:
            return
        visited.add(package)
        extras = package.extras
        if package == "requests":
            extras += ("security",)
        try:
            reqs = pkg_resources.get_distribution(package).requires(extras)
        except pkg_resources.DistributionNotFound:
            return
        discovered.update(req.project_name.lower() for req in reqs)
        for req in reqs:
            walk(req)

    walk(package)
    return sorted(discovered)


def research_package(name, version=None):
    with closing(urlopen("https://pypi.io/pypi/{}/json".format(name))) as f:
        reader = codecs.getreader("utf-8")
        pkg_data = json.load(reader(f))
    d = {}
    d['name'] = pkg_data['info']['name']
    d['homepage'] = pkg_data['info'].get('home_page', '')
    artefact = None
    if version:
        for pypi_version in pkg_data['releases']:
            if pkg_resources.safe_version(pypi_version) == version:
                for version_artefact in pkg_data['releases'][pypi_version]:
                    if version_artefact['packagetype'] == 'sdist':
                        artefact = version_artefact
                        break
        if artefact is None:
            warnings.warn("Could not find an exact version match for "
                          "{} version {}; using newest instead".
                          format(name, version), PackageVersionNotFoundWarning)

    if artefact is None:  # no version given or exact match not found
        for url in pkg_data['urls']:
            if url['packagetype'] == 'sdist':
                artefact = url
                break

    if artefact:
        d['url'] = artefact['url']
        if 'digests' in artefact and 'sha256' in artefact['digests']:
            logging.debug("Using provided checksum for %s", name)
            d['checksum'] = artefact['digests']['sha256']
        else:
            logging.debug("Fetching sdist to compute checksum for %s", name)
            with closing(urlopen(artefact['url'])) as f:
                d['checksum'] = sha256(f.read()).hexdigest()
            logging.debug("Done fetching %s", name)
    else:  # no sdist found
        d['url'] = ''
        d['checksum'] = ''
        warnings.warn("No sdist found for %s" % name)
    d['checksum_type'] = 'sha256'
    return d


def make_graph(pkg):
    """Returns a dictionary of information about pkg & its recursive deps.

    Given a string, which can be parsed as a requirement specifier, return a
    dictionary where each key is the name of pkg or one of its recursive
    dependencies, and each value is a dictionary returned by research_package.
    (No, it's not really a graph.)
    """
    ignore = ['argparse', 'pip', 'setuptools', 'wsgiref']
    pkg_deps = recursive_dependencies(pkg_resources.Requirement.parse(pkg))

    dependencies = {key: {} for key in pkg_deps if key not in ignore}
    installed_packages = pkg_resources.working_set
    versions = {package.key: package.version for package in installed_packages}
    for package in dependencies:
        try:
            dependencies[package]['version'] = versions[package]
        except KeyError:
            warnings.warn("{} is not installed so we cannot compute "
                          "resources for its dependencies.".format(package),
                          PackageNotInstalledWarning)
            dependencies[package]['version'] = None

    for package in dependencies:
        package_data = research_package(package, dependencies[package]['version'])
        dependencies[package].update(package_data)

    return OrderedDict(
        [(package, dependencies[package]) for package in sorted(dependencies.keys())]
    )


def formula_for(package, description: Optional[str] = None, homepage: Optional[str] = None, test: Optional[str] = None,  also=None):
    also = also or []
    req = pkg_resources.Requirement.parse(package)
    package_name = req.project_name
    nodes = merge_graphs(make_graph(p) for p in [package] + also)
    resources = [value for key, value in nodes.items()
                 if key.lower() != package_name.lower()]

    if package_name in nodes:
        root = nodes[package_name]
    elif package_name.lower() in nodes:
        root = nodes[package_name.lower()]
    else:
        raise Exception("Could not find package {} in nodes {}".format(package, nodes.keys()))
    root["test"] = "false"
    root["description"] = "Shiny new formula"
    if description:
        root["description"] = description
    if homepage:
        root["homepage"] = homepage
    if test:
        root["test"] = test
    python = "python" if sys.version_info.major == 2 else "python3"
    return FORMULA_TEMPLATE.render(package=root,
                                   resources=resources,
                                   python=python,
                                   ResourceTemplate=RESOURCE_TEMPLATE)
    
def updated_formula_for(package: Any, path: Optional[str] = None, description: Optional[str] = None, homepage: Optional[str] = None, test: Optional[str] = None,  also=None):
    also = also or []

    req = pkg_resources.Requirement.parse(package)
    package_name = req.project_name

    nodes = merge_graphs(make_graph(p) for p in [package] + also)
    resources = [value for key, value in nodes.items()
                 if key.lower() != package_name.lower()]

    if package_name in nodes:
        root = nodes[package_name]
    elif package_name.lower() in nodes:
        root = nodes[package_name.lower()]
    else:
        raise Exception("Could not find package {} in nodes {}".format(package, nodes.keys()))
    root["test"] = "false"
    root["description"] = "Shiny new formula"
    previous_description, previous_homepage, previous_test = parse_homebrew_formula(path)
    if previous_description:
        root["description"] = previous_description
    if previous_homepage:
        root["homepage"] = previous_homepage
    if previous_test:
        root["test"] = previous_test
    if description:
        root["description"] = description
    if homepage:
        root["homepage"] = homepage
    if test:
        root["test"] = test
    python = "python" if sys.version_info.major == 2 else "python3"
    return FORMULA_TEMPLATE.render(package=root,
                                   resources=resources,
                                   python=python,
                                   ResourceTemplate=RESOURCE_TEMPLATE)


def resources_for(packages):
    nodes = merge_graphs(make_graph(p) for p in packages)
    return '\n\n'.join([RESOURCE_TEMPLATE.render(resource=node)
                        for node in nodes.values()])


def merge_graphs(graphs):
    result = {}
    for g in graphs:
        for key in g:
            if key not in result:
                result[key] = g[key]
            elif result[key] == g[key]:
                pass
            else:
                warnings.warn(
                    "Merge conflict: {l.name} {l.version} and "
                    "{r.name} {r.version}; using the former.".
                    format(l=result[key], r=g[key]),
                    ConflictingDependencyWarning)
    return OrderedDict([k, result[k]] for k in sorted(result.keys()))


def main():
    parser = argparse.ArgumentParser(
        description='Generate Homebrew resource stanzas for pypi packages '
                    'and their dependencies.')
    parser.add_argument(
        '--update', '-u', action="store", type=str,
        help='Generate a resource stanza for one or more packages, '
             'without considering dependencies.')
    parser.add_argument(
        '--description', '-d', action="store", type=str,
        help='Generate a resource stanza for one or more packages, '
             'without considering dependencies.')
    parser.add_argument(
        '--homepage', '-p', action="store", type=str,
        help='Generate a resource stanza for one or more packages, '
             'without considering dependencies.')
    parser.add_argument(
        '--test', '-t', action="store", type=str,
        help='Generate a resource stanza for one or more packages, '
             'without considering dependencies.')
    parser.add_argument(
        '--output', '-o', action="store", type=str,
        help='Generate a resource stanza for one or more packages, '
             'without considering dependencies.')
    parser.add_argument('package', help=argparse.SUPPRESS, nargs='?')

    parser.add_argument(
        '-V', '--version', action='version',
        version='sholl {}'.format(__version__))
    args = parser.parse_args()
    if args.update and args.package:
        formula=updated_formula_for(args.package, args.update, description=args.description, homepage=args.homepage, test=args.test, also=args.test)
        if args.output:
            write_output_to_file(formula, args.output)
        else:
            print_output(formula)
    elif args.package:
        formula=formula_for(args.package , description=args.description, homepage=args.homepage, test=args.test, also=args.test)
        if args.output:
            write_output_to_file(formula, args.output)
        else:
            print_output(formula)
    return 0


if __name__ == '__main__':
    sys.exit(main())
