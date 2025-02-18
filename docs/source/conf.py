"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

from typing import Dict

import sphinx_rtd_theme

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "SimLab"
copyright = "2024, Nolwenn Bernard"
author = "Nolwenn Bernard"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
    "autoapi.extension",
    "myst_parser",
    "sphinx_multiversion",
    "sphinxcontrib.redoc",
]

templates_path = ["_templates"]

html_sidebars = {
    "**": [
        "versioning.html",
    ],
}

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_static_path = ["_static"]
html_theme_options: Dict[str, str] = {}

# Auto api
autoapi_type = "python"
autoapi_dirs = ["../../simlab", "../../webapp"]
autoapi_ignore = ["*tests/*"]
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
]
autoapi_python_class_content = "init"


# Redoc OpenAPI
redoc = [
    {
        "name": "SimLab Backend API",
        "page": "webapp/backend_api",
        "spec": "webapp/specs/backend_api_routes.yaml",
        "embed": True,
        "opts": {
            "hide-hostname": True,
        },
    },
    {
        "name": "Conversational Agent API",
        "page": "eval_framework/conversational_agent_api",
        "spec": "eval_framework/specs/conv_agent_api.yaml",
        "embed": True,
        "opts": {
            "hide-hostname": True,
        },
    },
    {
        "name": "User Simulator API",
        "page": "eval_framework/user_simulator_api",
        "spec": "eval_framework/specs/user_simulator_api.yaml",
        "embed": True,
        "opts": {
            "hide-hostname": True,
        },
    },
]
