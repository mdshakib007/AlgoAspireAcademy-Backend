
# AlgoAspire Academy

AlgoAspire Academy is a free, comprehensive e-learning platform designed to empower learners to master algorithms. Our platform aggregates course content from our YouTube channel, offers interactive note-taking, Q&A sessions, progress tracking, and gamification features to keep you motivated throughout your learning journey.

---

## Overview

AlgoAspire Academy is built to provide a one-stop hub for algorithm enthusiasts. Whether you’re watching video lectures, taking notes, asking questions, or tracking your progress, our platform is designed to enhance your learning experience with community-driven and AI-powered features.

---

## Key Features

- **Video Integration:**  
  - Embed YouTube videos for course lectures.
  
- **Notes Section:**  
  - Write and share personal notes beneath each video.
  - Access curated, topic-wise notes for deeper understanding.
  
- **Q&A with AI Assistance:**  
  - Ask questions and receive real-time hints via DeepSeek API.
  
- **Progress Tracking & Gamification:**  
  - Track your course progress with visual indicators.
  - Earn points for completing topics and challenges.
  - Compete on a leaderboard to boost motivation.
  
- **Interactive Quizzes and Assignments:**  
  - Engage with quizzes and coding challenges to test your skills.
  
- **User Profiles & Achievements:**  
  - Display badges, points, and course milestones.
  
- **Community Engagement:**  
  - Participate in forums and peer reviews.
  - Collaborate with fellow learners.

- **Future Enhancements:**  
  - Mobile app development.
  - Advanced AI-powered learning assistants and smart recommendations.

---

## Tech Stack

- **Frontend:**  
  - React for building a dynamic and responsive user interface.
  
- **Backend:**  
  - Django REST Framework (DRF) for robust API development.
  
- **Database:**  
  - PostgreSQL/MySQL (configurable based on deployment needs).
  
- **External Integrations:**  
  - YouTube API for video content.
  - DeepSeek API for AI-driven Q&A.
  
- **Deployment:**  
  - Docker & Docker Compose for containerized deployments.
  - Cloud hosting platforms (AWS, Heroku, etc.) for scalability.

---

## Project Structure

The project is organized into a modular structure for clarity and scalability:
```
algoaspire_academy/ 
├── config/ # Central configuration directory 
│ ├── __ init __.py
│ ├── asgi.py 
│ ├── urls.py 
│ ├── wsgi.py 
│ └── settings/ # Environment-specific settings 
│ ├── __ init __.py
│ ├── base.py 
│ ├── development.py 
│ └── production.py 
├── apps/ # Modular Django apps 
│ ├── __ init __.py 
│ ├── account/ # User authentication and profiles 
│ ├── course/ # Course content management 
│ ├── note/ # Note-taking and topic-wise notes 
│ ├── forum/ # For asking questions and sharing blogs.
│ ├── gamification/ # for user experience and making course fun
│ ├── quiz/ # for recap every module
│ └── ... # Additional apps as needed
├── manage.py # Django management script 
├── README.md # for explaining the project
└── requirements.txt # Python dependencies
```

## Simplified Schema:
```
 [User]
   └── user_id (PK)
   └── username
   └── email
   └── full_name
   └── profile_picture
   └── date_of_birth
   └── phone_number
   └── t_shirt_size
   └── country
   └── city
   └── organization
   └── is_admin
   └── is_instructor
   └── is_verified
   └── is_deleted
   └── is_active
         │
         └─< Enrollment >─┐
 [Course]                 │   [User-Course Enrollment]
   └── course_id (PK)     │   └── user_id (FK)
   └── code             ──┘   └── course_id (FK)
   └── name
   └── slug
   └── image
   └── description
   └── instructor (FK)
   └── is_enrolled
   └── completed_modules_count
   └── completed_assignments_count
   └── completed_quizzes_count

 [Module]
   └── module_id (PK)
   └── course_id (FK)
   └── title
   └── summary
   └── completed_lessons_count

 [Lesson]
   └── lesson_id (PK)
   └── module_id (FK)
   └── title
   └── summary
   └── lecture_type [text, video, quiz, assignment]
   └── video_url
   └── text_editorial

 [Quiz]
   └── quiz_id (PK)
   └── lesson_id (One to One)
   └── title

 [Question]
   └── question_id (PK)
   └── quiz_id (FK)
   └── title
   └── option_1
   └── option_2
   └── option_3
   └── option_4
   └── correct_option
   └── selected_option
   └── is_correct
   └── explanation

 [Assignment]
   └── assignment_id (PK)
   └── lesson_id (One to One)
   └── title
   └── question
   └── answer
   └── total_mark
   └── obtained_mark

 [Note]
   └── note_id (PK)
   └── content
   └── user_id (FK)
   └── lesson_id (FK)
```

---

## Title of a Student

1. **Merry Beginner**  ( neon < 1000) *(currency/points)*
   For those just starting out—enthusiastic, curious, and always ready for a laugh.

2. **Cheeky Apprentice**  ( neon >= 1000 & neon < 3000 )
   As you begin to learn the ropes, you mix in a dash of mischief with your newfound skills.

3. **Jolly Journeyman**  ( neon >= 3000 & neon < 7000 )
   When you’ve made some progress, you tackle challenges with a smile and a playful spirit.

4. **Quirky Conqueror**  ( neon >= 7000 & neon < 11,000 )
   You've overcome early hurdles and now approach problems with a fun, fearless attitude.

5. **Witty Warrior**  ( neon >= 11,000 & neon < 19,000 )
   At this stage, your clever insights and humorous approach make you a force to be reckoned with.

6. **Clever Commander**  ( neon >= 19,000 & neon < 27,000 )
   Leading the charge with wisdom and wit, you inspire others on their learning path.

7. **Supreme Sage**  ( neon >= 27,000 & neon < 1,00,000 )
   The ultimate title—where experience, humor, and mastery blend into one legendary persona.

8. **Ultra Legend**  ( neon >= 1,00,000 )
   The ultra title—where nothing to say!

---

## 🎖️ Achievements & Badges for AlgoAspire Academy

Here’s the list of **50 achievements** and **15 badges** based on milestones like learning progress, contributions, and engagement. The names are inspired by **popular games** like Clash of Clans, PUBG, Free Fire, Shadow Fight 2, etc.

---

### **🏆 Achievements (45 Total)**
| Achievement Title             | Requirement |
|------------------------------|-------------|
| **"First Steps"**            | Enroll in the first course |
| **"Module Master"**          | Complete 5 modules |
| **"Topic Tackler"**          | Complete 10 topics |
| **"Video Visionary"**        | Watch 50 course videos |
| **"The Note Taker"**         | Write 5 public notes |
| **"The Reviewer"**           | React to 10 notes |
| **"Questioner"**             | Ask 5 questions |
| **"Problem Solver"**         | Answer 5 questions |
| **"Aspiring Blogger"**       | Write your first blog post |
| **"Time Keeper"**            | Complete a course on time |
| **"Knowledge Collector"**    | Complete 3 courses |
| **"Legendary Learner"**      | Complete all courses |
| **"Quiz Champion"**          | Score 90%+ on 5 quiz |
| **"Streak Starter"**         | Log in for 3 consecutive days |
| **"Streak Master"**          | Log in for 7 consecutive days |
| **"Streak Beast"**           | Log in for 30 consecutive days |
| **"Daily Warrior"**          | Earn Neon for 7 days in a row |
| **"Ultimate Grinder"**       | Earn 10,000+ Neon |
| **"Master of Notes"**        | Publish 50 public notes |
| **"The Educator"**           | Answer 50 questions |
| **"Discussion Starter"**     | Get 10 comments on your blog |
| **"Social Butterfly"**       | Follow 10 users |
| **"Elite Mentor"**           | Get 100 upvotes on answers |
| **"Popular Author"**         | Have 50 upvotes on a blog |
| **"Certified Genius"**       | Earn 10 badges |
| **"Neon Collector"**         | Earn 100,000 Neon |
| **"Halfway Hero"**           | Complete 50% of all available courses |
| **"Endgame Scholar"**        | Complete all available courses |
| **"Explorer"**               | Try 5 different subjects |
| **"Multi-Talented"**         | Complete 5 courses from different categories |
| **"The Pioneer"**            | Be one of the first 100 users on the platform |
| **"Seasoned Warrior"**       | Earn 1,000,000 Neon |
| **"Elite Scholar"**          | Maintain a 90%+ completion rate in all courses |
| **"Golden Pen"**             | Write 100 blogs |
| **"Forum King"**             | Start 100 discussions |
| **"Community Legend"**       | React to 500 notes or blogs |
| **"Time Traveler"**          | Spend 500+ hours on the platform |
| **"Lifelong Learner"**       | Be active for 1 year |
| **"The OG"**                 | Join within the first month of launch |
| **"Speed Runner"**           | Complete a course in less than 7 days |
| **"Night Owl"**              | Study between 2 AM - 4 AM for 10 days |
| **"Morning Warrior"**        | Study between 5 AM - 7 AM for 10 days |
| **"The Perfectionist"**      | Score 100% on a quiz 10 times |
| **"Master of Mastery"**      | Unlock all achievements |
| **"The Ultimate Sage"**      | Earn all titles & 10,000,000 Neon |

---

### **🎖️ Badges (15 Total)**
| Badge Name                 | Requirement |
|----------------------------|-------------|
| **"Rookie Scholar"**       | Complete your first course |
| **"Enlightened Mind"**     | Complete 5 courses |
| **"The Mentor"**           | Answer 50 questions |
| **"The Curator"**          | Write 50 blog posts |
| **"The Helper"**           | React to 100 notes |
| **"Engagement King"**      | Have 100 comments on your content |
| **"Daily Streak"**         | Log in every day for a month |
| **"Quiz Master"**          | Get 100% in 10 quizzes |
| **"Community Builder"**    | Follow 50 people |
| **"Learning Machine"**     | Complete all courses in a month |
| **"King of Notes"**        | Publish 100 public notes |
| **"Diamond Learner"**      | Earn 1,000,000 Neon |
| **"Immortal Sage"**        | Earn all titles |
| **"AlgoAspire OG"**        | Join in the first month |
| **"Infinity Scholar"**     | Unlock all badges |

---

### **🔥 Why This?**
1. **Inspired by Popular Games** 🎮 (PUBG, Clash of Clans, Free Fire, Shadow Fight)  
2. **Motivates Learners** 💡 (Badges reward long-term progress)  
3. **Encourages Engagement** 💬 (Achievements for blogging, asking, answering)  
4. **Tracks Dedication** 📊 (Daily streaks, Neon earned milestones)  

🚀 **This can make learning more addictive and fun!**

## Optimized API Call For User
```
{
  "user": {
      "username": "shakib",
      "neons": 15000,
      "title": "Witty Warrior",
      "badges": ["Rookie Scholar", "The Mentor"],
      "achievements": ["First Steps", "Quiz Champion"],
      "recent_activities": [
          {"type": "Completed a Quiz", "timestamp": "2025-02-23T12:30:00Z"},
          {"type": "Wrote a Blog", "timestamp": "2025-02-22T15:00:00Z"}
      ]
  }
}

```

