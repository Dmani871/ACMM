from .factories import MenteeFactory,MentorFactory
def build():
    for x in range(100):
        MenteeFactory()
        MentorFactory()
