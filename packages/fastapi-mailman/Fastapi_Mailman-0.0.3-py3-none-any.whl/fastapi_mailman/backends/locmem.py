"""
Backend for test environment.
"""
from fastapi_mailman.backends.base import BaseEmailBackend


class EmailBackend(BaseEmailBackend):
    """
    An email backend for use during test sessions.

    The test connection stores email messages in a dummy outbox,
    rather than sending them out on the wire.

    The dummy outbox is accessible through the outbox instance attribute.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self.mailman, 'outbox'):
            self.mailman.outbox = []

    async def send_messages(self, messages):
        """Redirect messages to the dummy outbox"""
        msg_count = 0
        for message in messages:  # .message() triggers header validation
            message.message()
            self.mailman.outbox.append(message)
            msg_count += 1
        return msg_count
