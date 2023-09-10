from aiogram.types import Message


class SetGetDescriptor:
    """дескриптор данных"""
    def __set_name__(self, owner, name) -> None:
        self.name = name

    def __set__(self, instance, value) -> None:
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner) -> classmethod:
        return instance.__dict__[self.name]


class LinkedMessage(object):
    __linked_messages = {}
    admin_chat_msg_id = SetGetDescriptor()
    first_message_id = SetGetDescriptor()
    first_message_chat_id = SetGetDescriptor()

    def __init__(self, admin_chat_msg_id: int) -> None:
        self.admin_chat_msg_id = admin_chat_msg_id
        self.first_message_id = None
        self.first_message_chat_id = None

        LinkedMessage.add_element(admin_chat_msg_id, self)

    @classmethod
    def add_element(cls, admin_chat_msg_id: int, linked_msg: 'LinkedMessage') -> None:
        """adds an instance of the class to the class dictionary"""
        cls.__linked_messages[admin_chat_msg_id] = linked_msg

    @classmethod
    def get_element(cls, admin_chat_msg_id: int) -> 'LinkedMessage':
        """gets an instance of the class to the class dictionary"""
        return cls.__linked_messages[admin_chat_msg_id]

    def set_first_msg(self, msg: Message) -> None:
        """sets message_id and chat_id to the instance"""
        self.first_message_id = msg.message_id
        self.first_message_chat_id = msg.chat.id

    # def get_first_msg_id(self) -> int:
    #     """gets first message_id """
    #     return self.first_message_id
    #
    # def get_first_chat_id(self) -> int:
    #     """gets first message_id """
    #     return self.first_message_chat_id
