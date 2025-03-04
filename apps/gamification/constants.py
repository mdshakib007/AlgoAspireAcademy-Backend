from django.db import models
from enum import Enum

class Titles(models.TextChoices):
    MERRY_BEGINNER = "Merry Beginner"
    CHEEKY_APPRENTICE = "Cheeky Apprentice"
    JOLLY_JOURNEYMAN = "Jolly Journeyman"
    QUIRKY_CONQUEROR = "Quirky Conqueror"
    WITTY_WARRIOR = "Witty Warrior"
    CLEVER_COMMANDER = "Clever Commander"
    SUPREME_SAGE = "Supreme Sage"
    ULTRA_LEGEND = "Ultra Legend"

    @classmethod
    def choices(cls):
        """Returns a list of tuples suitable for Django model choices."""
        return [(title.name, title.value) for title in cls]


class Badge(Enum):

    ROOKIE_SCHOLAR = "Rookie Scholar"  # Complete your first course
    ENLIGHTENED_MIND = "Enlightened Mind"  # Complete 5 courses
    THE_MENTOR = "The Mentor"  # Answer 50 questions
    THE_CURATOR = "The Curator"  # Write 50 blog posts
    THE_HELPER = "The Helper"  # Upvote 100 notes
    ENGAGEMENT_KING = "Engagement King"  # Have 100 comments on your content
    DAILY_STREAK = "Daily Streak"  # Log in every day for a month
    QUIZ_MASTER = "Quiz Master"  # Get 100% in 10 quizzes
    COMMUNITY_BUILDER = "Community Builder"  # Follow 50 people
    LEARNING_MACHINE = "Learning Machine"  # Complete all courses in a month
    KING_OF_NOTES = "King of Notes"  # Publish 100 public notes
    DIAMOND_LEARNER = "Diamond Learner"  # Earn 1,000,000 Neon
    IMMORTAL_SAGE = "Immortal Sage"  # Earn `Supreme Sage` title
    ALGOASPIRE_OG = "AlgoAspire OG"  # Join in the first month
    INFINITY_SCHOLAR = "Infinity Scholar"  # Unlock all badges

    @classmethod
    def choices(cls):
        """Returns a list of tuples suitable for Django model choices."""
        return [(badge.name, badge.value) for badge in cls]



class Achievement(Enum):
    FIRST_STEPS = "First Steps"  # Enroll in the first course
    MODULE_MASTER = "Module Master"  # Complete 5 modules
    TOPIC_TACKLER = "Topic Tackler"  # Complete 10 topics
    VIDEO_VISIONARY = "Video Visionary"  # Watch 50 course videos
    THE_NOTE_TAKER = "The Note Taker"  # Write 5 public notes
    THE_REVIEWER = "The Reviewer"  # React to 10 notes
    QUESTIONER = "Questioner"  # Ask 5 questions
    PROBLEM_SOLVER = "Problem Solver"  # Answer 5 questions
    ASPIRING_BLOGGER = "Aspiring Blogger"  # Write your first blog post
    TIME_KEEPER = "Time Keeper"  # Complete a course on time
    KNOWLEDGE_COLLECTOR = "Knowledge Collector"  # Complete 3 courses
    LEGENDARY_LEARNER = "Legendary Learner"  # Complete 10 courses
    QUIZ_CHAMPION = "Quiz Champion"  # Score 90%+ on a quiz
    STREAK_STARTER = "Streak Starter"  # Log in for 3 consecutive days
    STREAK_MASTER = "Streak Master"  # Log in for 7 consecutive days
    STREAK_BEAST = "Streak Beast"  # Log in for 30 consecutive days
    DAILY_WARRIOR = "Daily Warrior"  # Earn Neon for 7 days in a row (Login reward not included)
    ULTIMATE_GRINDER = "Ultimate Grinder"  # Earn 10,000+ Neon
    MASTER_OF_NOTES = "Master of Notes"  # Publish 50 public notes
    THE_EDUCATOR = "The Educator"  # Answer 50 questions
    DISCUSSION_STARTER = "Discussion Starter"  # Get 10 comments on your blog
    SOCIAL_BUTTERFLY = "Social Butterfly"  # Follow 10 users
    ELITE_MENTOR = "Elite Mentor"  # Get 100 upvotes on answers
    POPULAR_AUTHOR = "Popular Author"  # Have 50 upvotes on a blog
    CERTIFIED_GENIUS = "Certified Genius"  # Earn 10 badges
    NEON_COLLECTOR = "Neon Collector"  # Earn 100,000 Neon
    HALFWAY_HERO = "Halfway Hero"  # Complete 50% of all available courses
    ENDGAME_SCHOLAR = "Endgame Scholar"  # Complete all available courses
    EXPLORER = "Explorer"  # Try 5 different categories
    MULTI_TALENTED = "Multi-Talented"  # Complete 5 courses from different categories
    THE_PIONEER = "The Pioneer"  # Be one of the first 100 users on the platform
    SEASONED_WARRIOR = "Seasoned Warrior"  # Earn 1,000,000 Neon
    ELITE_SCHOLAR = "Elite Scholar"  # Maintain a 90%+ completion rate in all courses
    GOLDEN_PEN = "Golden Pen"  # Write 100 blogs
    FORUM_KING = "Forum King"  # Start 100 discussions
    COMMUNITY_LEGEND = "Community Legend"  # Upvote 500 notes or blogs
    TIME_TRAVELER = "Time Traveler"  # Spend 500+ hours on the platform
    LIFELONG_LEARNER = "Lifelong Learner"  # Be active for 1 year
    THE_OG = "The OG"  # Join within the first month of launch
    SPEED_RUNNER = "Speed Runner"  # Complete a course in less than 7 days
    NIGHT_OWL = "Night Owl"  # Study between 2 AM - 4 AM for 10 days
    MORNING_WARRIOR = "Morning Warrior"  # Study between 5 AM - 7 AM for 10 days
    THE_PERFECTIONIST = "The Perfectionist"  # Score 100% on a quiz 5 times
    MASTER_OF_MASTERY = "Master of Mastery"  # Unlock all achievements
    THE_ULTIMATE_SAGE = "The Ultimate Sage"  # Earn 10,000,000 Neon

    @classmethod
    def choices(cls):
        """Returns a list of tuples suitable for Django model choices."""
        return [(achievement.name, achievement.value) for achievement in cls]


from enum import Enum

class Activity(Enum):

    JOINED_ALGOASPIRE = "Joined AlgoAspire"  # User joined the platform
    LOGGED_IN = "Logged-In"  # User logged into their account
    FOLLOWED_PERSON = "Followed a Person"  # User followed another person
    ENROLLED_COURSE = "Enrolled in a Course"  # User enrolled in a new course
    COMPLETED_MODULE = "Completed a Module"  # User completed a module
    COMPLETED_LESSON = "Completed a Lesson"  # User completed a lesson
    COMPLETED_TOPIC = "Completed a Topic"  # User completed a topic
    COMPLETED_QUIZ = "Completed a Quiz"  # User completed a quiz
    RETOOK_QUIZ = "Retook a Quiz"  # User retook a quiz
    RETOOK_COURSE = "Retook a Course"  # User retook a course
    UNLOCKED_COURSE = "Unlocked a Course"  # User unlocked a course
    WATCHED_VIDEO = "Watched a Video"  # User watched a course video
    WROTE_NOTE = "Wrote a Note"  # User wrote a public note
    EDITED_NOTE = "Edited a Note"  # User edited an existing note
    DELETED_NOTE = "Deleted a Note"  # User deleted a note
    UPVOTED_NOTE = "Upvoted a Note"  # User upvoted a note
    UPVOTED_BLOG = "Upvoted a Blog"  # User upvoted a blog post
    WROTE_BLOG = "Wrote a Blog"  # User wrote a blog post
    EDITED_BLOG = "Edited a Blog"  # User edited a blog post
    DELETED_BLOG = "Deleted a Blog"  # User deleted a blog post
    ASKED_QUESTION = "Asked a Question"  # User asked a question
    ANSWERED_QUESTION = "Answered a Question"  # User answered a question
    RECEIVED_UPVOTE_ANSWER = "Received an Upvote on Answer"  # User received an upvote on their answer
    COMMENTED_BLOG = "Commented on a Blog"  # User commented on a blog post
    FINISHED_COURSE = "Finished a Course"  # User completed a full course
    FINISHED_COURSE_ON_TIME = "Finished a Course on Time"  # User finished a course within the deadline
    UNLOCKED_ACHIEVEMENT = "Unlocked an Achievement"  # User unlocked an achievement
    UPGRADED_TITLE = "Upgraded a Title"  # User upgraded their title/rank
    EARNED_BADGE = "Earned a Badge"  # User earned a new badge
    MAINTAINED_STREAK = "Maintained a Streak"  # User maintained a login streak    LOST_STREAK = "Lost a Streak"  # User lost their login streak

    @classmethod
    def choices(cls):
        """Returns a list of tuples suitable for Django model choices."""
        return [(activity.name, activity.value) for activity in cls]