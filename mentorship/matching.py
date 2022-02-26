from collections import defaultdict
import numpy as np
import pandas as pd


def apply_matches_weights(mentors, mentees):
    mentee_preferences = defaultdict(dict)
    for mentee in mentees:
        rankings = defaultdict(dict)
        for mentor in mentors:
            ranking = 10
            # if both the mentee and mentor applied at the same stage(grad or post-18) double ranking
            if mentor.year_applied == mentee.year_applied:
                ranking *= 2
            # if the sex are not the same decrease ranking by 20%
            if mentor.sex != mentee.sex:
                ranking *= 0.8
            # counts the overlapping area_of_support for both the mentee and mentor
            support_factor = len(np.intersect1d(mentor.area_of_support, mentee.area_of_support))
            # counts how much interview experience the mentor had as it possible mentee hasn't had any yet
            interview_factor = len(mentor.interview_experience)
            # TODO:Check if mentees would have exam experience already
            # counts the overlapping exam experience
            exam_factor = len(np.intersect1d(mentor.entrance_exam_experience, mentee.entrance_exam_experience))

            # ensures the mentor can support the mentee based on their experiences
            if ('EE' in mentee.area_of_support and exam_factor == 0) or (
                    'I' in mentee.area_of_support and interview_factor == 0):
                support_factor = 0.01
            # amplifies the exam factor if they need support for entrance exams
            if 'EE' in mentee.area_of_support:
                exam_factor *= 10
            # amplifies the interview factor if they need support for interviews
            if 'I' in mentee.area_of_support:
                interview_factor *= 10
            # calculates the mentor factor
            mentor_factor = 1 + ((exam_factor + interview_factor) * 5)
            # calculates the overall ranking
            ranking = ranking * support_factor * mentor_factor
            # if the mentor can be of use add to the ranking with score
            if ranking > 0:
                rankings[mentor.id] = ranking
            mentee_preferences[mentee.id] = rankings
    return mentee_preferences


def stable_matching(mentee_preferences):
    matches_df = pd.DataFrame(mentee_preferences).fillna(-1)
    # mentee preferences
    mentee_pref_df = matches_df
    mentor_list = matches_df.index.tolist()
    # tracks proposals of every mentor
    mentor_dict = dict.fromkeys(mentor_list, 0)
    # list containing all proposals per a mentee
    waiting_dict = defaultdict(list)

    # while there are still proposals to be still be made by a mentor
    while bool(mentor_dict):
        rejected_mentors_list = []
        for k, v in mentor_dict.items():
            try:
                # mentor highest choice propose to mentee by adding to its proposal list
                waiting_dict[mentee_pref_df.loc[k].nlargest().index[v]].append(k)
                # increment proposal counter
                mentor_dict[k] += 1
            except IndexError:
                # mentor has proposed to all of it choices without being accepted
                rejected_mentors_list.append(k)
        # remove mentors from mentor_dict
        rejected_mentors = set(rejected_mentors_list) - set(mentor_dict)
        for rejected_mentor in rejected_mentors:
            del mentor_dict[rejected_mentor]
        new_mentor_dict = defaultdict(int)
        for k, mentors in waiting_dict.items():
            # if one mentee has multiple proposals
            if len(mentors) > 1:
                # order the list of mentors by ranking
                ordered_mentors = mentee_pref_df[k].filter(items=mentors).sort_values(ascending=False).index.tolist()
                for rejected_mentor in ordered_mentors[1:]:
                    new_mentor_dict[rejected_mentor] = mentor_dict[rejected_mentor]
                # only keeps the top weighted mentor for the mentee
                waiting_dict[k] = ordered_mentors[:1]
        mentor_dict = new_mentor_dict
    return waiting_dict


def generate_matches(mentors, mentees):
    mentee_preferences = apply_matches_weights(mentors, mentees)
    return stable_matching(mentee_preferences)
