from .factories import MenteeFactory,MentorFactory
def build(num=10):
    for x in range(num):
        #TODO:Add bulk create
        MenteeFactory()
        MentorFactory()
