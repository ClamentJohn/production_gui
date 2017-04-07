class LiveDataFeed(object):
    """ A simple "live data feed" abstraction that allows a reader 
        to read the most recent data and find out whether it was 
        updated since the last read. 
        
        Interface to data writer:
        
        add_data(data):
            Add new data to the feed.
        
        Interface to reader:
        
        read_data():
            Returns the most recent data.
            
        has_new_data:
            A boolean attribute telling the reader whether the
            data was updated since the last read.    
    """
    def __init__(self):
        self.cur_status = None
        self.cur_info = None
        self.has_new_status = False
        self.has_new_info = False
    
    def add_status(self, data):
        self.cur_status = data
        self.has_new_status = True
    
    def read_status(self):
        self.has_new_status = False
        return self.cur_status
    
    def add_info(self, data):
        self.cur_info = data
        self.has_new_info = True
    
    def read_info(self):
        self.has_new_info = False
        return self.cur_info


if __name__ == "__main__":
    pass

