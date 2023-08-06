from abc import ABC


class MessageType(ABC):
    """
    Interface for message types.
    """

    def get_name(self):
        """
        Return the name of the message type.

        Returns:
            str: The name of the message type.
        """

        pass

    def get_color_code(self):
        """
        Return the color code of the message type.

        Returns:
            str: The color code of the message type.
        """

        pass
