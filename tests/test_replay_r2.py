"""Second replay: observe lines carry work= and consistently formatted labels= for resumable sessions."""
import pytest

from conftest import CHECK_KIT, run

OBSERVE = 'step=observe platform=x work=PROJ-12 flow="ticket, code" pain="step C redone" labels={}'


def log(tmp_path, line):
    f = tmp_path / "progress.log"
    f.write_text(f"2026-01-01T00:00:00Z {line}\n", encoding="utf-8")
    return run(CHECK_KIT, "--log", f)


@pytest.mark.parametrize("labels", ["none", "shared=a,b;project=c,d", "project=c", '"shared=kit/(minus list.txt); project=AGENTS.md, bin/x"'])
def test_observe_with_work_and_labels_in_form_passes(tmp_path, labels):
    r = log(tmp_path, OBSERVE.format(labels))
    assert r.returncode == 0, r.stdout


@pytest.mark.parametrize("line", [OBSERVE.replace("work=PROJ-12 ", ""), OBSERVE.replace("work=PROJ-12", "work=")])
def test_observe_without_work_fails_and_says_how(tmp_path, line):
    r = log(tmp_path, line.format("none"))
    assert r.returncode == 1 and "work=" in r.stdout and "S02" in r.stdout


@pytest.mark.parametrize("labels", ["", "a,b", "shared=a,b,project=c", "shared=a;shared=b", "shared=;project=c",
                                    "shared=a,,b", "both=a", "shared=a;"])
def test_observe_with_labels_out_of_form_fails(tmp_path, labels):
    r = log(tmp_path, OBSERVE.format(labels))
    assert r.returncode == 1 and "labels=" in r.stdout and "shared=a,b;project=c,d" in r.stdout


def test_observe_without_labels_fails(tmp_path):
    r = log(tmp_path, OBSERVE.replace(" labels={}", ""))
    assert r.returncode == 1 and "labels=" in r.stdout
