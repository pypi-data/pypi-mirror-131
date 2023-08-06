"""
[Version 1.0.1]

This python library allows you to easily create logs for your code.

Example code:
    Code:
        from bitlogs import Logger
        from bitlogs.message_types.debug_message import DebugMessage

        Logger.log(DebugMessage(), "Hello world!")
    Output:
        [DEBUG] Hello world!

    Code:
        from bitlogs import Logger
        from bitlogs.message_types.critical_message import CriticalMessage


        def add(a, b):
            if (not isinstance(a, float)) or (not isinstance(a, float)):
                Logger.log(CriticalMessage(), "A and B have to be of the type float.")
                # you should probably raise an error here
            return a + b

        add(1, 2)
    Output:
        [CRITICAL] A and B have to be of the type float.

    Code:
        from bitlogs import Logger
        from bitlogs.message_types.debug_message import DebugMessage
        Logger.log_to_file(DebugMessage(), "Hello world!", "example.bitlog")
    Note:
        You can display the content of the file by running:
        "cat example.bitlog" on macOS + Linux and "type example.bitlog" on Windows
"""


from bitlogs.message_type import MessageType
from bitlogs.terminal_colors import TerminalColors


class Logger:
    @staticmethod
    def get_message(message_type: MessageType, text: str):
        """
        Return log message.

        Args:
            message_type (MessageType): Type of the message.
            text (str): Content of the message.

        Returns:
            str: Log message
        """

        return f"{message_type.get_color_code()}[{message_type.get_name()}] {TerminalColors.ENDC}{text}"

    @staticmethod
    def log(message_type: MessageType, text: str):
        """
        Print log message.

        Args:
            message_type (MessageType): Type of the message.
            text (str): Content of the message.
        """

        print(Logger.get_message(message_type, text))

    @staticmethod
    def log_to_file(message_type: MessageType, text: str, filename: str):
        """
        Print (append) log message to a file.

        Args:
            message_type (MessageType): Type of the message.
            text (str): Content of the message.
            filename (str): Name of the file.
        """

        #
        message = Logger.get_message(message_type, text)
        with open(filename, "a") as f:
            f.write(f"{message}\n")
