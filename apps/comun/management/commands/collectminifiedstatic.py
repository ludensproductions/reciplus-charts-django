import json
import os
import re
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.core.management import BaseCommand, CommandError, call_command
from rcssmin import cssmin
from rjsmin import jsmin

from apps.comun.consts import SUPPORTED_TEXT_SUFFIXES
from apps.comun.static_assets import (
    EXTERNAL_ASSET_ROOT,
    build_external_asset_relative_path,
    is_supported_asset_content_type,
    is_supported_embedded_asset_content_type,
    iter_css_nested_asset_urls,
    iter_css_relative_asset_urls,
    iter_external_asset_urls,
    normalize_external_asset_url,
    resolve_relative_css_url,
)


def _minify_static_asset_file(file_path, static_root, keep_originals):
    """Minify a single CSS or JS asset and return the outcome for aggregation."""
    suffix = file_path.suffix.lower()

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        min_content = cssmin(content) if suffix == ".css" else jsmin(content)

        if keep_originals:
            target_file = file_path.with_name(f"{file_path.stem}.min{suffix}")
            target_file.write_text(min_content, encoding="utf-8")
        else:
            temp_file = file_path.with_name(f"{file_path.name}.tmp")
            temp_file.write_text(min_content, encoding="utf-8")
            temp_file.replace(file_path)

        return str(file_path), None
    except OSError as exc:
        rel = file_path.relative_to(static_root)
        return None, f"{rel}: {exc}"
    except Exception as exc:  # Defensive: minifier failures should not be ignored silently.
        rel = file_path.relative_to(static_root)
        return None, f"{rel}: {exc}"


class Command(BaseCommand):
    """Collect static files, download CDN assets, minify, and localize external resources.

    This command orchestrates:
    1. Collection of static files via Django collectstatic
    2. Discovery of external CDN URLs in templates and static files
    3. Download of CDN assets to local storage
    4. Rewriting of references to use local files
    5. Minification of CSS/JS assets
    """

    help = (
        "Collect static files, download CDN assets, minify CSS/JS, "
        "and keep only optimized local files in STATIC_ROOT."
    )

    CDN_URL_REGEX = re.compile(r"(?:(?:https?:)?//)[^\s\"'()<>]+", re.IGNORECASE)

    def add_arguments(self, parser):
        """Add command-line arguments for CDN download configuration.

        Args:
            parser: ArgumentParser instance.
        """
        parser.add_argument(
            "--timeout",
            type=int,
            default=15,
            help="Timeout in seconds for CDN downloads (default: 15).",
        )
        parser.add_argument(
            "--keep-originals",
            action="store_true",
            help="Keep original .css/.js files and also create .min files.",
        )

    def handle(self, *args, **options):
        """Execute the static collection and asset optimization pipeline.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments from CLI (timeout, keep_originals).

        Raises:
            CommandError: If STATIC_ROOT is not configured.
        """
        static_root_value = getattr(settings, "STATIC_ROOT", "")
        if not static_root_value:
            raise CommandError("STATIC_ROOT is not configured.")
        static_root = Path(static_root_value)

        timeout = options["timeout"]
        keep_originals = options["keep_originals"]

        self.stdout.write("Running collectstatic...")
        call_command("collectstatic", interactive=False, verbosity=0, clear=True)

        cdn_urls = self._extract_cdn_urls_from_static_dirs()
        downloaded, cdn_url_map = self._download_cdns(cdn_urls, static_root, timeout)
        embedded_downloaded = self._localize_downloaded_css_assets(static_root, timeout)
        rewritten_references = self._rewrite_cdn_references(static_root, cdn_url_map)

        minified, overwritten, generated_min_files, errors = self._minify_static_assets(static_root, keep_originals)

        if errors:
            raise CommandError(
                "Static optimization completed with minification errors: "
                f"{len(errors)} file(s) failed. First error: {errors[0]}"
            )

        self.stdout.write(self.style.SUCCESS("Static files optimized successfully."))
        self.stdout.write("Summary:")
        self.stdout.write(f"- CDN URLs found: {len(cdn_urls)}")
        self.stdout.write(f"- CDN files downloaded: {downloaded}")
        self.stdout.write(f"- Nested CSS assets downloaded: {embedded_downloaded}")
        self.stdout.write(f"- CDN references rewritten: {rewritten_references}")
        self.stdout.write(f"- CSS/JS files minified: {minified}")
        self.stdout.write(f"- Files overwritten in place: {overwritten}")
        self.stdout.write(f"- New .min files generated: {generated_min_files}")
        self.stdout.write(f"- Output directory: {static_root}")

    def _extract_cdn_urls_from_static_dirs(self):
        urls = set()
        for scan_path in self._get_cdn_scan_paths():
            if isinstance(scan_path, (str, os.PathLike)):
                scan_path_str = str(scan_path)
                if self.CDN_URL_REGEX.fullmatch(scan_path_str):
                    urls.add(normalize_external_asset_url(scan_path_str))
                    continue

            scan_dir_path = Path(scan_path)
            if not scan_dir_path.exists() or not scan_dir_path.is_dir():
                continue

            for file_path in scan_dir_path.rglob("*"):
                if not file_path.is_file():
                    continue
                if file_path.suffix.lower() not in SUPPORTED_TEXT_SUFFIXES:
                    continue

                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue

                for match in iter_external_asset_urls(content, file_path.suffix):
                    urls.add(match)

        return sorted(urls)

    def _get_cdn_scan_paths(self):
        scan_paths = []

        for static_dir in getattr(settings, "STATICFILES_DIRS", []):
            scan_paths.append(static_dir)

        for template_config in getattr(settings, "TEMPLATES", []):
            for template_dir in template_config.get("DIRS", []):
                scan_paths.append(template_dir)

        base_dir = Path(getattr(settings, "BASE_DIR", Path.cwd()))
        apps_dir = base_dir / "apps"
        if apps_dir.exists():
            for template_dir in apps_dir.glob("*/templates"):
                scan_paths.append(template_dir)

        return scan_paths

    def _download_cdns(self, cdn_urls, static_root, timeout):
        if not cdn_urls:
            return 0, {}

        local_cdns_dir = static_root / EXTERNAL_ASSET_ROOT
        local_cdns_dir.mkdir(parents=True, exist_ok=True)

        downloaded = 0
        url_map = {}
        max_workers = min(8, len(cdn_urls))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self._download_single_cdn_asset, url, static_root, timeout) for url in cdn_urls]

            for future in as_completed(futures):
                normalized_url, relative_output, warning_message = future.result()
                if warning_message:
                    self.stderr.write(self.style.WARNING(warning_message))
                    continue

                if not normalized_url or not relative_output:
                    continue

                downloaded += 1
                url_map[normalized_url] = relative_output
                self.stdout.write(f"Downloaded CDN asset: {normalized_url}")

        self._write_manifest(static_root, url_map)

        return downloaded, url_map

    def _download_single_cdn_asset(self, url, static_root, timeout):
        normalized_url = normalize_external_asset_url(url)
        parsed = urlparse(normalized_url)
        if parsed.scheme not in {"http", "https"}:
            return normalized_url, None, None

        try:
            response = requests.get(normalized_url, timeout=timeout)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if not is_supported_asset_content_type(content_type):
                return normalized_url, None, None

            relative_output = build_external_asset_relative_path(normalized_url, content_type)
            output_file = static_root / relative_output
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_bytes(response.content)
            return normalized_url, relative_output, None
        except requests.RequestException as exc:
            return normalized_url, None, f"Failed to download {normalized_url}: {exc}"

    def _write_manifest(self, static_root, url_map):
        manifest_dir = static_root / EXTERNAL_ASSET_ROOT
        manifest_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = manifest_dir / "manifest.json"
        manifest_path.write_text(json.dumps(url_map, indent=2, sort_keys=True), encoding="utf-8")

    def _localize_downloaded_css_assets(self, static_root, timeout):
        localized = 0
        external_root = static_root / EXTERNAL_ASSET_ROOT
        if not external_root.exists():
            return localized

        # Build an inverted manifest so we can look up each CSS file's source URL.
        manifest_path = external_root / "manifest.json"
        inverted_manifest = {}
        if manifest_path.exists():
            try:
                raw = json.loads(manifest_path.read_text(encoding="utf-8"))
                inverted_manifest = {v: k for k, v in raw.items()}
            except (OSError, json.JSONDecodeError):
                pass

        for css_file in external_root.rglob("*.css"):
            try:
                content = css_file.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue

            relative_css_path = css_file.relative_to(static_root).as_posix()
            css_source_url = inverted_manifest.get(relative_css_path, "")

            updated = content

            # Absolute external URLs in CSS (e.g. url(https://...))
            for asset_url in iter_css_nested_asset_urls(content):
                updated, localized = self._fetch_and_rewrite_css_asset(
                    asset_url, updated, static_root, timeout, localized
                )

            # Relative URLs (e.g. url(../webfonts/fa-solid-900.woff2))
            if css_source_url:
                for rel_path in iter_css_relative_asset_urls(content):
                    resolved = resolve_relative_css_url(rel_path, css_source_url)
                    new_content, localized = self._fetch_and_rewrite_css_asset(
                        resolved,
                        updated,
                        static_root,
                        timeout,
                        localized,
                        original_token=rel_path,
                    )
                    updated = new_content

            if updated != content:
                css_file.write_text(updated, encoding="utf-8")

        return localized

    def _fetch_and_rewrite_css_asset(
        self, asset_url, content, static_root, timeout, localized, *, original_token=None
    ):
        try:
            response = requests.get(asset_url, timeout=timeout)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if not is_supported_embedded_asset_content_type(content_type):
                return content, localized

            relative_output = build_external_asset_relative_path(asset_url, content_type)
            output_file = static_root / relative_output
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_bytes(response.content)
            local_url = f"{settings.STATIC_URL.rstrip('/')}/{relative_output}"
            token_to_replace = original_token if original_token else asset_url
            content = content.replace(token_to_replace, local_url)
            localized += 1
        except requests.RequestException as exc:
            self.stderr.write(self.style.WARNING(f"Failed to download nested asset {asset_url}: {exc}"))
        return content, localized

    def _rewrite_cdn_references(self, static_root, cdn_url_map):
        if not cdn_url_map:
            return 0

        rewritten = 0
        text_suffixes = {".css", ".js", ".mjs", ".html", ".htm", ".map"}

        for file_path in static_root.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in text_suffixes:
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue

            def replace_url(match):
                token = match.group(0)
                normalized = normalize_external_asset_url(token)
                relative_path = cdn_url_map.get(normalized)
                if not relative_path:
                    return token
                downloaded_file = static_root / relative_path
                if not downloaded_file.exists():
                    return token
                return f"{settings.STATIC_URL.rstrip('/')}/{relative_path}"

            updated = self.CDN_URL_REGEX.sub(replace_url, content)

            if updated != content:
                file_path.write_text(updated, encoding="utf-8")
                rewritten += 1

        return rewritten

    def _minify_static_assets(self, static_root, keep_originals):
        minified = 0
        overwritten = 0
        generated_min_files = 0
        errors = []

        eligible_files = []

        for file_path in static_root.rglob("*"):
            if not file_path.is_file():
                continue

            suffix = file_path.suffix.lower()
            if suffix not in {".css", ".js", ".mjs"}:
                continue

            if (
                file_path.name.endswith(".min.css")
                or file_path.name.endswith(".min.js")
                or file_path.name.endswith(".min.mjs")
            ):
                continue

            eligible_files.append(file_path)

        if not eligible_files:
            return minified, overwritten, generated_min_files, errors

        max_workers = min(len(eligible_files), os.cpu_count() or 1)

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(_minify_static_asset_file, file_path, static_root, keep_originals)
                for file_path in eligible_files
            ]

            for future in as_completed(futures):
                file_path, error_message = future.result()
                if error_message:
                    errors.append(error_message)
                    continue

                minified += 1
                if keep_originals:
                    generated_min_files += 1
                else:
                    overwritten += 1

        return minified, overwritten, generated_min_files, errors
