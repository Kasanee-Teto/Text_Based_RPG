from main import print_header, print_separator
from config import UIConfig

def test_print_header_outputs_text(capsys):
    print_header("HELLO", style="cyan")
    out = capsys.readouterr().out
    assert "HELLO" in out

def test_print_separator_outputs_dashes(capsys):
    print_separator()
    out = capsys.readouterr().out
    assert "-" * UIConfig.SEPARATOR_LENGTH in out