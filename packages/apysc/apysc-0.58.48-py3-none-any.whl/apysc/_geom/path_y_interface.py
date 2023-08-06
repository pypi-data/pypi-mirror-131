"""Interface class implementation for the y path data.
"""

from apysc._type.int import Int


class PathYInterface:

    _y: Int

    @property
    def y(self) -> Int:
        """
        Get a y-coordinate of the destination point.

        Returns
        -------
        y : Int
            A y-coordinate of the destination point.
        """
        import apysc as ap
        with ap.DebugInfo(
                callable_='y', locals_=locals(),
                module_name=__name__, class_=PathYInterface):
            return self._y._copy()

    @y.setter
    def y(self, value: Int) -> None:
        """
        Set a y-coordinate of the destination point.

        Parameters
        ----------
        value : Int
            Y-coordinate of the destination point.
        """
        import apysc as ap
        with ap.DebugInfo(
                callable_='y', locals_=locals(),
                module_name=__name__, class_=PathYInterface):
            self._y.value = value
