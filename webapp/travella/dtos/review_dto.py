class ReviewDTO:
    def __init__(self, id=None, content='', account_name='', created_at=None):
        self.id = id
        self.content = content
        self.account_name = account_name
        self.created_at = created_at