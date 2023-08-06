#! /usr/bin/env python
# Copyright (C) 2016 Alain Leufroy
#
# Author: Alain Leufroy <alain@leufroy.fr>
# Licence: WTFPL, grab your copy here: http://sam.zoy.org/wtfpl/
"""Main UI widgets for lairucrem."""

from __future__ import absolute_import, unicode_literals

import urwid
from urwid.canvas import CompositeCanvas
from urwid.command_map import CURSOR_LEFT, CURSOR_RIGHT
from urwid.widget import GIVEN, PACK, WEIGHT, delegate_to_widget_mixin

from .. import config
from ..utils import apply_mixin
from .utils import ANY, get_original_widget


class popuplauncher(urwid.PopUpLauncher):
    """
    Main widget that allows to display a popup using the `open_pop_up` method.

    Usage:
    ======

    >>> content = urwid.Filler(urwid.Text('Foo'))
    >>> launcher = popuplauncher(content)
    >>> popup = urwid.Filler(urwid.Text('Bar'))
    >>> launcher.open_pop_up(popup)
    """

    def __init__(self, *args, **kwargs):
        self._screen = None
        self._height = None
        self._pop_up_widgets = []
        super(popuplauncher, self).__init__(*args, **kwargs)

    def open_pop_up(self, widget):
        self._pop_up_widgets.append(widget)
        if getattr(widget, 'signals', None) and 'close' in widget.signals:
            urwid.connect_signal(
                widget, 'close', lambda *a: self.close_pop_up(widget))
        self._invalidate()

    def close_pop_up(self, widget):
        # actual popup could be a newer one
        if widget in self._pop_up_widgets:
            self._pop_up_widgets.remove(widget)
        self._invalidate()

    def render(self, size, focus=False):
        canv = self._original_widget.render(size, focus)
        if self._pop_up_widgets:
            widget = self._pop_up_widgets[-1]
            canv = CompositeCanvas(canv)
            cols, rows = size
            height = rows - 4
            if getattr(widget, 'get_rows', None):
                height = min(height, widget.get_rows())
            top = int((rows - height) / 2)
            canv.set_pop_up(widget,
                            left=2, overlay_width=cols - 4,
                            top=top, overlay_height=height)
        return canv


class mainwidget(urwid.Pile):
    """Main widget with help"""
    _help = "[enter] actions  [/] filter  [left,right] details  [?] help"

    signals = ['open_popup']

    def __init__(self, widget):
        head = urwid.AttrWrap(
            urwid.Filler(urwid.Text(self._help)),
            'highlight',
        )
        super(mainwidget, self).__init__(
            [(1, head), widget],
            focus_item=widget,
        )


class thehelp(urwid.Pile):
    """Help dialog content"""

    @staticmethod
    def get_rows():
        """prefered height"""
        return 20

    def __init__(self):

        def key(keys, help):
            key = ' '.join(keys).rjust(16)
            text = [('ui.keyword', key), (None, '  '), help]
            return urwid.Text(text)

        def title(text):
            return urwid.Text([('ui.title', text)])

        super(thehelp, self).__init__([
            title('Global keys\n'),
            key(['<Tab>'], 'Switch pane'),
            key(['<Esc>'], 'Close dialog box'),
            key(['?'], 'This help'),
            key(['q', 'Q'], 'Quit the application'),
            key(['G'], ('Grep: Search revision history '
                        'for a regular expression')),

            title('\nTREE pane keys\n'),
            key(['<Up>', '<Down>'], 'Goto the previous/next changeset'),
            key(['<Alt Up>', '<Alt Down>'], 'Goto the previous child/parent'),
            key(['ctrl f'], 'Filter the revision tree with a revset'),
            key(['<enter>'], 'Actions related to the selected changset'),
            key(['<ctrl r>'], 'Refresh view content'),

            title('\nPATCH pane keys\n'),
            key(['<Up>', '<Down>'], 'Scroll Up, Down'),
            key(['/'], 'Search pattern in the patch content'),
            key(['n', 'N'], 'Jump to the next/previous matched line'),
            key(['<ctrl r>'], 'Refresh view content'),
        ])


class _maximizable_contenxt_base:

    _maximized = False

    @property
    def _focused_options(self):
        raise NotImplementedError

    @property
    def _unfocused_options(self):
        raise NotImplementedError

    def toggle_maximize(self, value=None):
        if value is None:
            self._maximized = not(self._maximized)
        else:
            self._maximized = value
        self._modified()

    def __iter__(self):
        if self._maximized:
            for i, (widget, options) in enumerate(super().__iter__()):
                if i == self._focus:
                    yield (widget, self._focused_options)
                else:
                    yield (widget, self._unfocused_options)
            return
        for v in super().__iter__():
            yield v


class maximizable_columns_contents_mixin(_maximizable_contenxt_base):

    _focused_options = (WEIGHT, 1, False)
    _unfocused_options = (GIVEN, 0, False)


class maximizable_pile_contents_mixin(_maximizable_contenxt_base):

    _focused_options = (WEIGHT, 1)
    _unfocused_options = (GIVEN, 0)


class packer(delegate_to_widget_mixin('_original_widget')):
    """Pack the given widgets horizontally (Columns)or vertically (Pile)
    depending on the screen size.
    """

    def selectable(self):
        return True

    def __init__(self, widgets):
        self._orientation = None
        if config.DEFAULT_MAIN_VIEW in (config.HORIZONTAL, config.VERTICAL):
            self._orientation = config.DEFAULT_MAIN_VIEW
        self._widgets = widgets
        self._original_widget = None
        self._column_widget = None
        self._pile_widget = None
        self._previous_size = None
        self._initialize_containers()
        if self._orientation:
            self._previous_size = ANY
            self._update_container()
        if config.DEFAULT_MAIN_VIEW in (config.TREE, config.DETAILS):
            self._set_focus_position(0 if config.DEFAULT_MAIN_VIEW == config.TREE else 1)
            self._toggle_miximize(True)

    def render(self, size, focus):
        """render the widget"""
        if self._previous_size != size:
            self._guess_orientation(size)
            self._update_container()
        self._previous_size = size
        return super(packer, self).render(size, focus)

    def _initialize_containers(self):
        self._column_widget = urwid.Columns(self._widgets)
        apply_mixin(self._column_widget.contents, maximizable_columns_contents_mixin)
        self._pile_widget = urwid.Pile(self._widgets)
        apply_mixin(self._pile_widget.contents, maximizable_pile_contents_mixin)

    def _update_container(self):
        """update the main container depending on the given size"""
        assert self._orientation
        if self._orientation == config.HORIZONTAL:
            self._original_widget = self._column_widget
        elif self._orientation == config.VERTICAL:
            self._original_widget = self._pile_widget
        self._invalidate()

    def _set_focus_position(self, num):
        self._column_widget.focus_position = num
        self._pile_widget.focus_position = num

    def _toggle_miximize(self, value=None):
        self._column_widget.contents.toggle_maximize(value)
        self._pile_widget.contents.toggle_maximize(value)

    def _guess_orientation(self, size):
        old_cols = self._previous_size[0] if self._previous_size else ANY
        cols = size[0]
        # Note: `not (x <= y)` because of Any which always answers True
        if cols > 160 and cols > old_cols:
            self._orientation = config.HORIZONTAL
        if cols <= 160 and cols < old_cols:
            self._orientation = config.VERTICAL

    def keypress(self, size, key):
        """Process pressed key"""
        key = self._keypress_next_packed(size, key)
        key = super(packer, self).keypress(size, key)
        command = self._command_map[key]
        if command == config.CMD_MAXIMALIZE:
            self._toggle_miximize()
        if command == config.CMD_SPLIT_HORIZONTALLY:
            self._orientation = config.VERTICAL
            self._update_container()
            return
        if command == config.CMD_SPLIT_VERTICALLY:
            self._orientation = config.HORIZONTAL
            self._update_container()
            return
        if command == CURSOR_LEFT:
            self._set_focus_position(max(0, self._original_widget.focus_position - 1))
            return
        if command == CURSOR_RIGHT:
            self._set_focus_position(
                min(len(self._widgets) - 1, self._original_widget.focus_position + 1))
            return
        if command in (config.CMD_NEXT_SELECTABLE, config.CMD_PREV_SELECTABLE):
            self._set_focus_position(self._get_next_widget_position())
            return
        return key

    def _keypress_next_packed(self, size, key):
        """Send few keys to the next packed widget."""
        newkey = self._next_packed_key_convert.get(self._command_map[key])
        if not newkey:
            return key
        nextwidget = self._widgets[self._get_next_widget_position()]
        return nextwidget.keypress(size, newkey)

    def _get_next_widget_position(self):
        return (self._original_widget.focus_position + 1) % len(self._widgets)

    _next_packed_key_convert = {
        config.CURSOR_UP_NEXT_PACKED: config.CURSOR_UP,
        config.CURSOR_DOWN_NEXT_PACKED: config.CURSOR_DOWN,
        config.CURSOR_PAGE_UP_NEXT_PACKED: config.CURSOR_PAGE_UP,
        config.CURSOR_PAGE_DOWN_NEXT_PACKED: config.CURSOR_PAGE_DOWN,
        config.CURSOR_MAX_LEFT_NEXT_PACKED: config.CURSOR_MAX_LEFT,
        config.CURSOR_MAX_RIGHT_NEXT_PACKED: config.CURSOR_MAX_RIGHT,
        config.CMD_NEXT_MATCH_NEXT_PACKED: config.CMD_NEXT_MATCH,
        config.CMD_PREV_MATCH_NEXT_PACKED: config.CMD_PREV_MATCH,
    }



class pane(urwid.LineBox):
    """
    A LineBox that changes surrounding chars accordingly to the focus
    state.
    """

    # pylint: disable=super-init-not-called
    def __init__(self, original_widget, title=""):
        """
        Draw a line around original_widget.

        Use 'title' to set an initial title text with will be centered
        on top of the box.

        You can also override the widgets used for the lines/corners:
            tline: top line
            bline: bottom line
            lline: left line
            rline: right line
            tlcorner: top left corner
            trcorner: top right corner
            blcorner: bottom left corner
            brcorner: bottom right corner

        """
        self.tline = urwid.Divider(' ')
        self.bline = urwid.Divider(' ')
        self.lline = urwid.SolidFill(' ')
        self.rline = urwid.SolidFill(' ')
        (tlcorner, trcorner, blcorner, brcorner,
         self.fill_char_focus, self.fill_char, self.div_char_focus, self.div_char) = config.BORDERS

        self.title_widget = urwid.Text(self.format_title(title))
        self.tline_widget = urwid.Columns([
            self.tline,
            ('flow', self.title_widget),
            self.tline,
        ])

        top = urwid.Columns([
            ('fixed', 1, urwid.Text(tlcorner)),
            self.tline_widget,
            ('fixed', 1, urwid.Text(trcorner))
        ])

        middle = urwid.Columns([
            ('fixed', 1, self.lline),
            original_widget,
            ('fixed', 1, self.rline),
        ], box_columns=[0, 2], focus_column=1)

        bottom = urwid.Columns([
            ('fixed', 1, urwid.Text(blcorner)), self.bline, ('fixed', 1, urwid.Text(brcorner))
        ])

        pile = urwid.Pile(
            [('flow', top), middle, ('flow', bottom)], focus_item=1)

        urwid.WidgetDecoration.__init__(self, original_widget)
        urwid.WidgetWrap.__init__(self, pile)

    def render(self, size, focus=False):
        """Return the canvas that renders the widget content."""
        self.lline.fill_char = self.rline.fill_char = self.fill_char_focus if focus else self.fill_char
        self.tline.div_char = self.bline.div_char = self.div_char_focus if focus else self.div_char
        self.lline._invalidate()
        self.rline._invalidate()
        self.tline._invalidate()
        self.bline._invalidate()
        try:
            return super(pane, self).render(size, focus=True)
        except IndexError:
            # the content is empty, we can't force focus
            return super(pane, self).render(size, focus=False)

    def keypress(self, size, key):
        key = super().keypress(size, key)
        # Prevent moving the cursor out from the current pane after
        # the last selectable widget is reached.
        command = self._command_map[key]
        return key if command not in self._non_propagated_commands else None

    _non_propagated_commands = (
        config.CURSOR_DOWN, config.CURSOR_UP,
        config.CURSOR_PAGE_DOWN, config.CURSOR_PAGE_UP,
        config.CURSOR_MAX_LEFT, config.CURSOR_MAX_RIGHT
    )
