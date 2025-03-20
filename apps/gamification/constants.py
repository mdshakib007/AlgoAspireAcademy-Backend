from django.db import models

class TitleChoices(models.TextChoices):
    MERRY_BEGINNER = "Merry Beginner", "Merry Beginner"
    CHEEKY_APPRENTICE = "Cheeky Apprentice", "Cheeky Apprentice"
    JOLLY_JOURNEYMAN = "Jolly Journeyman", "Jolly Journeyman"
    QUIRKY_CONQUEROR = "Quirky Conqueror", "Quirky Conqueror"
    WITTY_WARRIOR = "Witty Warrior", "Witty Warrior"
    CLEVER_COMMANDER = "Clever Commander", "Clever Commander"
    SUPREME_SAGE = "Supreme Sage", "Supreme Sage"
    ULTRA_LEGEND = "Ultra Legend", "Ultra Legend"


class BadgeChoices(models.TextChoices):
    ROOKIE_SCHOLAR = "Rookie Scholar",  "Rookie Scholar" # Complete your first course
    ENLIGHTENED_MIND = "Enlightened Mind",  "Enlightened Mind"  # Complete 5 courses
    THE_MENTOR = "The Mentor", "The Mentor"  # Answer 50 questions
    THE_CURATOR = "The Curator", "The Curator"  # Write 50 blog posts
    THE_HELPER = "The Helper", "The Helper"  # Upvote 100 notes
    ENGAGEMENT_KING = "Engagement King", "Engagement King"  # Have 100 comments on your content
    DAILY_STREAK = "Daily Streak", "Daily Streak"  # Log in every day for a month
    QUIZ_MASTER = "Quiz Master", "Quiz Master"  # Get 100% in 10 quizzes
    COMMUNITY_BUILDER = "Community Builder", "Community Builder"  # Follow 50 people
    LEARNING_MACHINE = "Learning Machine", "Learning Machine"  # Complete all courses in a month
    KING_OF_NOTES = "King of Notes", "King of Notes"  # Publish 100 public notes
    DIAMOND_LEARNER = "Diamond Learner", "Diamond Learner"  # Earn 1,000,000 Neon
    IMMORTAL_SAGE = "Immortal Sage", "Immortal Sage"  # Earn `Supreme Sage` title
    ALGOASPIRE_OG = "AlgoAspire OG", "AlgoAspire OG"  # Join in the first month
    INFINITY_SCHOLAR = "Infinity Scholar", "Infinity Scholar"  # Unlock all badges


class AchievementChoices(models.TextChoices):
    FIRST_STEPS = "First Steps","First Steps"  # Enroll in the first course
    MODULE_MASTER = "Module Master","Module Master"  # Complete 5 modules
    TOPIC_TACKLER = "Topic Tackler", "Topic Tackler"  # Complete 10 topics
    VIDEO_VISIONARY = "Video Visionary", "Video Visionary"  # Watch 50 course videos
    THE_NOTE_TAKER = "The Note Taker", "The Note Taker"  # Write 5 public notes
    THE_REVIEWER = "The Reviewer", "The Reviewer" # React to 10 notes
    QUESTIONER = "Questioner", "Questioner"  # Ask 5 questions
    PROBLEM_SOLVER = "Problem Solver", "Problem Solver"  # Answer 5 questions
    ASPIRING_BLOGGER = "Aspiring Blogger", "Aspiring Blogger"  # Write your first blog post
    TIME_KEEPER = "Time Keeper",  "Time Keeper"  # Complete a course on time
    KNOWLEDGE_COLLECTOR = "Knowledge Collector", "Knowledge Collector"  # Complete 3 courses
    LEGENDARY_LEARNER = "Legendary Learner", "Legendary Learner"  # Complete 10 courses
    QUIZ_CHAMPION = "Quiz Champion", "Quiz Champion"  # Score 90%+ on a quiz
    STREAK_STARTER = "Streak Starter", "Streak Starter"  # Log in for 3 consecutive days
    STREAK_MASTER = "Streak Master", "Streak Master"  # Log in for 7 consecutive days
    STREAK_BEAST = "Streak Beast","Streak Beast"  # Log in for 30 consecutive days
    DAILY_WARRIOR = "Daily Warrior", "Daily Warrior"  # Earn Neon for 7 days in a row (Login reward not included)
    ULTIMATE_GRINDER = "Ultimate Grinder", "Ultimate Grinder"  # Earn 10,000+ Neon
    MASTER_OF_NOTES = "Master of Notes", "Master of Notes"  # Publish 50 public notes
    THE_EDUCATOR = "The Educator", "The Educator"  # Answer 50 questions
    DISCUSSION_STARTER = "Discussion Starter", "Discussion Starter"  # Get 10 comments on your blog
    SOCIAL_BUTTERFLY = "Social Butterfly", "Social Butterfly"  # Follow 10 users
    ELITE_MENTOR = "Elite Mentor", "Elite Mentor"  # Get 100 upvotes on answers
    POPULAR_AUTHOR = "Popular Author" , "Popular Author" # Have 50 upvotes on a blog
    CERTIFIED_GENIUS = "Certified Genius", "Certified Genius"  # Earn 10 badges
    NEON_COLLECTOR = "Neon Collector", "Neon Collector"  # Earn 100,000 Neon
    HALFWAY_HERO = "Halfway Hero", "Halfway Hero"  # Complete 50% of all available courses
    ENDGAME_SCHOLAR = "Endgame Scholar", "Endgame Scholar"  # Complete all available courses
    EXPLORER = "Explorer" , "Explorer" # Try 5 different categories
    MULTI_TALENTED = "Multi-Talented" , "Multi-Talented" # Complete 5 courses from different categories
    THE_PIONEER = "The Pioneer", "The Pioneer"  # Be one of the first 100 users on the platform
    SEASONED_WARRIOR = "Seasoned Warrior", "Seasoned Warrior"  # Earn 1,000,000 Neon
    ELITE_SCHOLAR = "Elite Scholar", "Elite Scholar"  # Maintain a 90%+ completion rate in all courses
    GOLDEN_PEN = "Golden Pen", "Golden Pen"  # Write 100 blogs
    FORUM_KING = "Forum King", "Forum King"  # Start 100 discussions
    COMMUNITY_LEGEND = "Community Legend", "Community Legend"  # Upvote 500 notes or blogs
    TIME_TRAVELER = "Time Traveler", "Time Traveler"  # Spend 500+ hours on the platform
    LIFELONG_LEARNER = "Lifelong Learner","Lifelong Learner"   # Be active for 1 year
    THE_OG = "The OG" ,  "The OG" # Join within the first month of launch
    SPEED_RUNNER = "Speed Runner", "Speed Runner"  # Complete a course in less than 7 days
    NIGHT_OWL = "Night Owl", "Night Owl"  # Study between 2 AM - 4 AM for 10 days
    MORNING_WARRIOR = "Morning Warrior", "Morning Warrior"  # Study between 5 AM - 7 AM for 10 days
    THE_PERFECTIONIST = "The Perfectionist", "The Perfectionist"  # Score 100% on a quiz 5 times
    MASTER_OF_MASTERY = "Master of Mastery", "Master of Mastery"  # Unlock all achievements
    THE_ULTIMATE_SAGE = "The Ultimate Sage", "The Ultimate Sage"  # Earn 10,000,000 Neon


class ActivityChoices(models.TextChoices):
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