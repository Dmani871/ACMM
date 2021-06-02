from .factories import MenteeFactory,MentorFactory
def build(num=10):
    for x in range(num):
        MenteeFactory()
        MentorFactory()
