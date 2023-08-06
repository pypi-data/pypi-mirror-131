class DealWebhook(object):
    def __init__(self):
        pass

    def stage_change(self):
        pass

    def field_change(self):
        pass


class PersonWebhook(object):
    def __init__(self):
        pass

    def assign_owner(self):
        pass

    def get_source(self):
        pass


class Webhook(object):
    def __init__(self):
        self.auth()
        self.parse()

    def auth(self):
        pass

    def parse(self):
        '''

        :return:
        if the object is either deal or person webhook
        '''
        pass

