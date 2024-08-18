Inspiration

The project was inspired by the desire to create an engaging and interactive web application where users can test their knowledge through quizzes, earn points, and redeem vouchers. The goal was to build a platform that not only educates but also rewards users for their participation. This is to curb the harsh impacts of fast fashion that has arised in the recent years. It alows users to understand and internalise the severity of the issue and what they can do to contribute

What it does

The web application allows users to register and log in to their accounts. Once logged in, users can participate in various quizzes, accumulate points based on their performance, and view their standing on a leaderboard. Users can also redeem points for vouchers from selected brands.

How it’s built

The application is built using Flask along with HTML and CSS . User data is stored in a CSV file, and the application logic handles tasks like user authentication, quiz management, points accumulation, and voucher redemption. Sessions are used to manage user states across different pages.

Challenges encountered

One of the main challenges was managing user data effectively using CSV files, especially when handling updates to user scores and completed quizzes. Ensuring that the application correctly reads and writes to the CSV files without data loss or corruption was crucial. Another challenge was ensuring that users could not retake quizzes and accurately deducting points during voucher redemption.

Accomplishments that I’m proud of

Successfully implementing the quiz system, where users can take quizzes and receive immediate feedback based on their answers, was a significant accomplishment. Additionally, building the points-based reward system and integrating it with a voucher redemption feature added a meaningful incentive for users to participate actively.

What I learned

Through this project, I learned how to manage user sessions in Flask, work with CSV files for data storage, and implement features like a leaderboard and a point redemption system. I also deepened my understanding of web development concepts, including routing, form handling, and template rendering in Flask.

What’s next for 

The next steps include transitioning from CSV file storage to a more robust database solution like SQLite or PostgreSQL, enhancing the interface of the application, and adding more quizzes with varied difficulty levels. Additionally, expanding the voucher system to include more brands and creating a more dynamic leaderboard.
