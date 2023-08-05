from AppKit import NSColorWell, NSColorPanel
from vanilla.vanillaBase import VanillaBaseObject


class ColorWell(VanillaBaseObject):

    """
    A control that allows for showing and choosing a color value.

    .. image:: /_images/ColorWell.png

    ColorWell objects handle `NSColor`_ objects.

    ::

        from AppKit import NSColor
        from vanilla import Window, ColorWell

        class ColorWellDemo:

            def __init__(self):
                self.w = Window((100, 50))
                self.w.colorWell = ColorWell((10, 10, -10, -10),
                                    callback=self.colorWellEdit,
                                    color=NSColor.redColor())
                self.w.open()

            def colorWellEdit(self, sender):
                print("color well edit!", sender.get())

        ColorWellDemo()

    **posSize** Tuple of form *(left, top, width, height)* or *"auto"*
    representing the position and size of the color well.

    **callback** The method to be caled when the user selects a new color.

    **color** A `NSColor`_ object. If *None* is given, the color shown will
    be white.

    .. _NSColor: https://developer.apple.com/documentation/appkit/nscolor?language=objc
    """

    nsColorWellClass = NSColorWell

    def __init__(self, posSize, callback=None, color=None):
        self._setupView(self.nsColorWellClass, posSize, callback=callback)
        if color is not None:
            self._nsObject.setColor_(color)
        colorPanel = NSColorPanel.sharedColorPanel()
        colorPanel.setShowsAlpha_(True)

    def getNSColorWell(self):
        """
        Return the `NSColorWell`_ that this object wraps.

        .. _NSColorWell: https://developer.apple.com/documentation/appkit/nscolorwell?language=objc
        """
        return self._nsObject

    def get(self):
        """
        Get the `NSColor`_ object representing the current color in
        the color well.

        .. _NSColor: https://developer.apple.com/documentation/appkit/nscolor?language=objc
        """
        return self._nsObject.color()

    def set(self, color):
        """
        Set the color in the color well.

        **color** A `NSColor`_ object representing the color to be displayed
        in the color well.
        """
        return self._nsObject.setColor_(color)
