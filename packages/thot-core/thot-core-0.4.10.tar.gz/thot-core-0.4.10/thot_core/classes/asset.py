# coding: utf-8
# Asset

from .resource import Resource


class Asset( Resource ):
    """
    An Asset.
    """

    def __init__( self, **kwargs ):
        """
        Creates a new Asset.

        :param **kwargs: Initial property values.
        """
        defaults = {
            'file':         None,
            'parent':       None,
            'creator':      None,
            'creator_type': None,
        }

        super().__init__( kwargs, defaults )
