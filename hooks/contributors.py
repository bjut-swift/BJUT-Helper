import json
import logging
import os

import requests

LOG = logging.getLogger("mkdocs.hooks.contributors")

GITHUB_API = "https://api.github.com"
REPO = "bjut-swift/BJUT-Helper"
BRANCH = "master"
CACHE_FILE = ".cache/contributors.json"

_cache = {}
_token = ""
_rate_limited = False


def on_config(config):
    global _cache, _token
    _token = os.environ.get("MKDOCS_GIT_COMMITTERS_APIKEY", "")
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            _cache = json.load(f)


def on_page_context(context, page, config, nav):
    global _rate_limited
    context["committers"] = []
    context["committers_source"] = "github"

    title = page.meta.get("title", "")
    if not title or not os.path.isdir(title):
        return context

    if title in _cache:
        context["committers"] = _cache[title]
        return context

    if _rate_limited:
        return context

    headers = {}
    if _token:
        headers["Authorization"] = f"token {_token}"

    url = f"{GITHUB_API}/repos/{REPO}/commits"
    params = {"path": title, "sha": BRANCH, "per_page": 100}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        if r.status_code != 200:
            if r.status_code in (401, 403):
                _rate_limited = True
            LOG.warning("contributors: %d for %s", r.status_code, title)
            return context

        authors = []
        seen = set()
        for commit in r.json():
            author = commit.get("author")
            if not author or not author.get("login"):
                continue
            login = author["login"]
            if login in seen:
                continue
            seen.add(login)
            authors.append(
                {
                    "login": login,
                    "name": login,
                    "url": author.get("html_url", ""),
                    "avatar": author.get("avatar_url", ""),
                }
            )

        _cache[title] = authors
        context["committers"] = authors
    except Exception as e:
        LOG.warning("contributors: error for %s: %s", title, e)

    return context


def on_post_build(config):
    if _cache:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, "w") as f:
            json.dump(_cache, f)
