import platform

import pytest
from qtpy.QtWidgets import QPushButton, QToolTip

from qthandy.filter import InstantTooltipEventFilter


@pytest.mark.skipif(platform.system() == 'Darwin', reason="Cannot run on Darwin")
def test_instant_tooltip(qtbot):
    btn = QPushButton('Button')
    qtbot.addWidget(btn)
    btn.show()

    btn.setToolTip('Test button')
    btn.installEventFilter(InstantTooltipEventFilter(btn))
    qtbot.mouseMove(btn)

    assert QToolTip.isVisible()
    assert QToolTip.text() == 'Test button'
