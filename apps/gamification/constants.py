TITLES = [
    ('Merry Beginner', 'Merry Beginner'), # --> ( neon < 1000)
    ('Cheeky Apprentice', 'Cheeky Apprentice'), # --> ( neon >= 1000 & neon < 3000 )
    ('Jolly Journeyman', 'Jolly Journeyman'), # --> ( neon >= 3000 & neon < 7000 )
    ('Quirky Conqueror', 'Quirky Conqueror'), # --> ( neon >= 7000 & neon < 11,000 )
    ('Witty Warrior', 'Witty Warrior'), # --> ( neon >= 11,000 & neon < 19,000 )
    ('Clever Commander', 'Clever Commander'), # --> ( neon >= 19,000 & neon < 27,000 )
    ('Supreme Sage', 'Supreme Sage'), # --> ( neon >= 27,000 & neon < 1,00,000 )
    ('Ultra Legend', 'Ultra Legend') # --> ( neon >= 1,00,000 )
]

BADGES = [
    ('Rookie Scholar', 'Rookie Scholar'), # --> Complete your first course
    ('Enlightened Mind', 'Enlightened Mind'), # --> Complete 5 courses
    ('The Mentor', 'The Mentor'), # --> Answer 50 questions
    ('The Curator', 'The Curator'), # --> Write 50 blog posts
    ('The Helper', 'The Helper'), # --> Upvote to 100 notes
    ('Engagement King', 'Engagement King'), # --> Have 100 comments on your content
    ('Daily Streak', 'Daily Streak'), # --> Log in every day for a month
    ('Quiz Master', 'Quiz Master'), # --> Get 100% in 10 quizzes
    ('Community Builder', 'Community Builder'), # --> Follow 50 people
    ('Learning Machine', 'Learning Machine'), # --> Complete all courses in a month
    ('King of Notes', 'King of Notes'), # --> Publish 100 public notes
    ('Diamond Learner', 'Diamond Learner'), # --> Earn 1,000,000 Neon
    ('Immortal Sage', 'Immortal Sage'), # --> Earn `Supreme Sage` title
    ('AlgoAspire OG', 'AlgoAspire OG'), # --> Join in the first month
    ('Infinity Scholar', 'Infinity Scholar'), # --> Unlock all badges
]

ACHIEVEMENTS = [
    ('First Steps', 'First Steps'), # --> Enroll in the first course
    ('Module Master', 'Module Master'), # --> Complete 5 modules
    ('Topic Tackler', 'Topic Tackler'), # --> Complete 10 topics
    ('Video Visionary', 'Video Visionary'), # --> Watch 50 course videos
    ('The Note Taker', 'The Note Taker'), # --> Write 5 public notes
    ('The Reviewer', 'The Reviewer'), # --> React to 10 notes
    ('Questioner', 'Questioner'), # --> Ask 5 questions
    ('Problem Solver', 'Problem Solver'), # --> Answer 5 questions
    ('Aspiring Blogger', 'Aspiring Blogger'), # --> Write your first blog post
    ('Time Keeper', 'Time Keeper'), # --> Complete a course on time
    ('Knowledge Collector', 'Knowledge Collector'), # --> Complete 3 courses
    ('Legendary Learner', 'Legendary Learner'), # --> Complete 10 courses
    ('Quiz Champion', 'Quiz Champion'), # --> Score 90%+ on a quiz
    ('Streak Starter', 'Streak Starter'), # --> Log in for 3 consecutive days
    ('Streak Master', 'Streak Master'), # --> Log in for 7 consecutive days
    ('Streak Beast', 'Streak Beast'), # --> Log in for 30 consecutive days
    ('Daily Warrior', 'Daily Warrior'), # --> Earn Neon for 7 days in a row (Login reward will not included.)
    ('Ultimate Grinder', 'Ultimate Grinder'), # --> Earn 10,000+ Neon
    ('Master of Notes', 'Master of Notes'), # --> Publish 50 public notes
    ('The Educator', 'The Educator'), # --> Answer 50 questions
    ('Discussion Starter', 'Discussion Starter'), # --> Get 10 comments on your blog
    ('Social Butterfly', 'Social Butterfly'), # --> Follow 10 users
    ('Elite Mentor', 'Elite Mentor'), # --> Get 100 upvotes on answers
    ('Popular Author', 'Popular Author'), # --> Have 50 upvotes on a blog
    ('Certified Genius', 'Certified Genius'), # --> Earn 10 badges
    ('Neon Collector', 'Neon Collector'), # --> Earn 100,000 Neon
    ('Halfway Hero', 'Halfway Hero'), # --> Complete 50% of all available courses
    ('Endgame Scholar', 'Endgame Scholar'), # --> Complete all available courses
    ('Explorer', 'Explorer'), # --> Try 5 different categories
    ('Multi-Talented', 'Multi-Talented'), # --> Complete 5 courses from different categories
    ('The Pioneer', 'The Pioneer'), # --> Be one of the first 100 users on the platform
    ('Seasoned Warrior', 'Seasoned Warrior'), # --> Earn 1,000,000 Neon
    ('Elite Scholar', 'Elite Scholar'), # --> Maintain a 90%+ completion rate in all courses
    ('Golden Pen', 'Golden Pen'), # --> Write 100 blogs
    ('Forum King', 'Forum King'), # --> Start 100 discussions
    ('Community Legend', 'Community Legend'), # --> Upvote to 500 notes or blogs
    ('Time Traveler', 'Time Traveler'), # --> Spend 500+ hours on the platform
    ('Lifelong Learner', 'Lifelong Learner'), # --> Be active for 1 year
    ('The OG', 'The OG'), # --> Join within the first month of launch
    ('Speed Runner', 'Speed Runner'), # --> Complete a course in less than 7 days
    ('Night Owl', 'Night Owl'), # --> Study between 2 AM - 4 AM for 10 days
    ('Morning Warrior', 'Morning Warrior'), # --> Study between 5 AM - 7 AM for 10 days
    ('The Perfectionist', 'The Perfectionist'), # --> Score 100% on a quiz 5 times
    ('Master of Mastery', 'Master of Mastery'), # --> Unlock all achievements
    ('The Ultimate Sage', 'The Ultimate Sage'), # --> Earn 10,000,000 Neon
]

ACTIVITY_CHOICES = [
    ('Joined AAA', 'Joined AAA'),
    ('Logged-In', 'Logged-In'),
    ('Followed a Person', 'Followed a Person'),
    ('Enrolled in a Course', 'Enrolled in a Course'),
    ('Completed a Module', 'Completed a Module'),
    ('Completed a Lesson', 'Completed a Lesson'),
    ('Completed a Topic', 'Completed a Topic'),
    ('Completed a Quiz', 'Completed a Quiz'),
    ('Retook a Quiz', 'Retook a Quiz'),
    ('Retook a Course', 'Retook a Course'),
    ('Unlocked a Course', 'Unlocked a Course'),
    ('Watched a Video', 'Watched a Video'),
    ('Wrote a Note', 'Wrote a Note'),
    ('Edited a Note', 'Edited a Note'),
    ('Deleted a Note', 'Deleted a Note'),
    ('Upvoted a Note', 'Upvoted a Note'),
    ('Upvoted a Blog', 'Upvoted a Blog'),
    ('Wrote a Blog', 'Wrote a Blog'),
    ('Edited a Blog', 'Edited a Blog'),
    ('Deleted a Blog', 'Deleted a Blog'),
    ('Asked a Question', 'Asked a Question'),
    ('Answered a Question', 'Answered a Question'),
    ('Received an Upvote on Answer', 'Received an Upvote on Answer'),
    ('Commented on a Blog', 'Commented on a Blog'),
    ('Finished a Course', 'Finished a Course'),
    ('Finished a Course on Time', 'Finished a Course on Time'),
    ('Unlocked an Achievement', 'Unlocked an Achievement'),
    ('Upgraded a Title', 'Upgraded a Title'),
    ('Earned a Badge', 'Earned a Badge'),
    ('Maintained a Streak', 'Maintained a Streak'),
    ('Lost a Streak', 'Lost a Streak'),
]
