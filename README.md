# Crypto-Giveaway-TG-Bot
The bot for assigning tasks and verifying their completion by users with internal points awards

## Setup Bot:
1. Create DB
    - Import sql template [./database/bot-database.sql](./database/bot-database.sql)
1. Create `.env` file (based on `.env.example`) and fill it
1. Install packages: `pip install -r requirements.txt`
1. Run `main.py`

## Database info:
* `users_bot` - table for every users, who inrecated with bot.
* `tasks_bot` - table with each created task for execution by users. Accessible only for bot-admins (command: /admin) or from admin panel.
* `task_tracker_2` - table with tasks that after creation are assigned to each user in the bot (One-To-Many relationship).
* `bundle_shop` - table for creating bundles that users can buy to get more internal points.
* `payment_logs` - table with logs of bundle purchases that can be seen and used by administrators who have access to the admin panel.
* `panel_accounts` - table for creating an admin panel user.

## General Bot Algorithm:
1. The user goes through 5 steps of registration:
   - Captcha (Select Language -> "Join" button -> Captcha)
   - Balance
   - Reaction (Join related channel)
   - Invite_Friend (Bot referral system; 3 negative bot-checks proceed user to the next stage)
   - Wallet (Enter your crypto wallet address)
   - Done (Completed registration/guide stage)
2. After registration user has functionality:
   - Profile
   - Active tasks
   - Buy tokens/points
3. Admin creates new task in admin menu
4. User goes to "My Tasks" and can complete the task by providing a link as the proof of completion
5. Admin verifies the completion of the task and if the task is confirmed, the user receives points

## Detailed Registration Algorithm: 
### Captcha Stage
1. User initiates the first communication with bot by command: /start.
1. Bot recognizes in what language to communicate with the user [RU/ENG].
3. Bot greets the user and sends a "Join" button which will start the registration stage.
4. User clicks "Join" button.
5. Bot sends the user a generated captcha to verify the user's humanity.
6. User must enter the correct captcha otherwise the bot will generate a new one and wait for the user to respond.
7. User enters the correct captcha
### Balance Stage
8. Bot sends a balance message
9. User clicks the "Balance" button
### Reaction Stage
10. Bot sends a link to the channel user need to subscribe to
11. User clicks on the "Subscribed" button
12. Bot verifies through the admin access in this channel if the user is in this telegram channel
### Referral(Invite_Friend) Stage
13. Bot sends the user a link with their referral link (?start=referral_id)
14. User has to click the "Invited a friend" button himself, then the user will run the [bot time based algorithm](./handlers/user_questions.py?plain=1#L110) to verify the friend invitation in the bot
