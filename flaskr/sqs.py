import boto3
import logging

# Currently not used, as we interact with allocation algorithm via an API Gateway, though both can be easily configure
# communicate with queues, if we prefer to have the communication to happen within the application rather than over
# the internet.
class HandleSQS:

    REGION_NAME = 'eu-west-1'
    QUEUE_NAME = 'budyapp-algortihm'
    MAX_QUEUE_MESSAGES = 10
    message_bodies = []

    def send_message(self, body):
        try:
            self._queue.send_message(
                MessageBody=body
            )
        except Exception as e:
            self._log.exception("Could not send message")
            raise e

    def get_all_messages(self):
        while True:
            messages_to_delete = []
            try:
                for message in self._queue.receive_messages(
                        MaxNumberOfMessages=self.MAX_QUEUE_MESSAGES):
                    # process message body
                    body = message.body
                    self.message_bodies.append(body)
                    # add message to delete
                    messages_to_delete.append({
                        'Id': message.message_id,
                        'ReceiptHandle': message.receipt_handle
                    })
            except Exception as e:
                self._log.exception("Could not retrieve messages")
                raise e

            # if you don't receive any notifications the
            # messages_to_delete list will be empty
            if len(messages_to_delete) == 0:
                return self.message_bodies

            # delete messages to remove them from SQS queue
            # handle any errors
            else:
                try:
                    self._queue.delete_messages(Entries=messages_to_delete)
                except Exception as e:
                    self._log.exception("Could not delete queue element")
                    raise e

    def __init__(self):
        try:
            self._log = logging.getLogger(__name__)
            self._sqs = boto3.resource('sqs', region_name=self.REGION_NAME)
            self._queue = self._sqs.get_queue_by_name(
                QueueName=self.QUEUE_NAME)

        except Exception as e:
            self._log.exception("Could not connect to queue")
            raise e
