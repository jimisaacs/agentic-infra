from __future__ import annotations

import importlib.machinery
import importlib.util
import os
from pathlib import Path
from unittest.mock import patch
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
DEV_PATH = REPO_ROOT / "dev"


def load_extensionless_module(path: Path, module_name: str):
    loader = importlib.machinery.SourceFileLoader(module_name, str(path))
    spec = importlib.util.spec_from_loader(module_name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


dev_module = load_extensionless_module(DEV_PATH, "baseline_dev")


class DevEntrypointTests(unittest.TestCase):
    def test_core_commands_include_expected_surface(self) -> None:
        for cmd in ("help", "setup", "verify", "fmt", "doctor", "status", "stack"):
            self.assertIn(cmd, dev_module.CORE_COMMANDS)

    def test_required_paths_include_human_baseline_contract(self) -> None:
        self.assertIn("project/README.md", dev_module.REQUIRED_PATHS)
        self.assertIn(".githooks/pre-commit", dev_module.REQUIRED_PATHS)
        self.assertIn("docs/PRINCIPLES.md", dev_module.REQUIRED_PATHS)
        self.assertIn("docs/CONVENTIONS.md", dev_module.REQUIRED_PATHS)
        self.assertIn(".editorconfig", dev_module.REQUIRED_PATHS)

    def test_normalize_text_strips_trailing_whitespace_and_ensures_newline(self) -> None:
        self.assertEqual(dev_module.normalize_text("hello  \nworld\t"), "hello\nworld\n")

    def test_should_skip_link_only_for_external_targets(self) -> None:
        self.assertTrue(dev_module.should_skip_link("https://example.com"))
        self.assertFalse(dev_module.should_skip_link("project/README.md"))


class TerminalTests(unittest.TestCase):
    def test_no_color_env_disables_color(self) -> None:
        with patch.dict(os.environ, {"NO_COLOR": "1"}):
            t = dev_module.Terminal()
            self.assertFalse(t.color)

    def test_clicolor_force_enables_color(self) -> None:
        env = {"CLICOLOR_FORCE": "1"}
        with patch.dict(os.environ, env, clear=False):
            with patch.object(dev_module.sys, "stdout") as mock_stdout:
                mock_stdout.isatty.return_value = False
                t = dev_module.Terminal()
                if "NO_COLOR" not in os.environ:
                    self.assertTrue(t.color)

    def test_term_dumb_disables_color(self) -> None:
        env = {"TERM": "dumb"}
        with patch.dict(os.environ, env, clear=False):
            no_color = os.environ.pop("NO_COLOR", None)
            clicolor = os.environ.pop("CLICOLOR_FORCE", None)
            try:
                with patch.object(dev_module.sys, "stdout") as mock_stdout:
                    mock_stdout.isatty.return_value = True
                    t = dev_module.Terminal()
                    self.assertFalse(t.color)
            finally:
                if no_color is not None:
                    os.environ["NO_COLOR"] = no_color
                if clicolor is not None:
                    os.environ["CLICOLOR_FORCE"] = clicolor

    def test_unicode_detection_with_utf8_lang(self) -> None:
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8", "LC_ALL": ""}):
            with patch.object(dev_module.sys, "stdout") as mock_stdout:
                mock_stdout.isatty.return_value = True
                t = dev_module.Terminal()
                self.assertTrue(t.unicode)

    def test_unicode_disabled_without_tty(self) -> None:
        with patch.object(dev_module.sys, "stdout") as mock_stdout:
            mock_stdout.isatty.return_value = False
            t = dev_module.Terminal()
            self.assertFalse(t.unicode)

    def test_ansi_stripping_when_no_color(self) -> None:
        with patch.dict(os.environ, {"NO_COLOR": "1"}):
            t = dev_module.Terminal()
            self.assertEqual(t.green("hello"), "hello")
            self.assertEqual(t.red("world"), "world")

    def test_symbols_have_fallbacks(self) -> None:
        with patch.object(dev_module.sys, "stdout") as mock_stdout:
            mock_stdout.isatty.return_value = False
            t = dev_module.Terminal()
            self.assertEqual(t.sym_ok, "[ok]")
            self.assertEqual(t.sym_err, "[error]")
            self.assertEqual(t.sym_warn, "[warn]")


class ParserTests(unittest.TestCase):
    def test_stack_up_parses(self) -> None:
        parser = dev_module.build_parser()
        args = parser.parse_args(["stack", "up"])
        self.assertEqual(args.command, "stack")
        self.assertEqual(args.stack_command, "up")
        self.assertTrue(hasattr(args, "func"))

    def test_stack_down_parses(self) -> None:
        parser = dev_module.build_parser()
        args = parser.parse_args(["stack", "down"])
        self.assertEqual(args.stack_command, "down")

    def test_stack_dev_parses(self) -> None:
        parser = dev_module.build_parser()
        args = parser.parse_args(["stack", "dev"])
        self.assertEqual(args.stack_command, "dev")

    def test_stack_no_subcommand(self) -> None:
        parser = dev_module.build_parser()
        args = parser.parse_args(["stack"])
        self.assertIsNone(args.stack_command)

    def test_verify_parses(self) -> None:
        parser = dev_module.build_parser()
        args = parser.parse_args(["verify"])
        self.assertEqual(args.command, "verify")

    def test_fmt_check_flag(self) -> None:
        parser = dev_module.build_parser()
        args = parser.parse_args(["fmt", "--check"])
        self.assertTrue(args.check)


class DockerPreflightTests(unittest.TestCase):
    def test_require_docker_fails_when_missing(self) -> None:
        with patch.object(dev_module.shutil, "which", return_value=None):
            with self.assertRaises(SystemExit) as ctx:
                dev_module._require_docker()
            self.assertEqual(ctx.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
