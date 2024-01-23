# Demonstration

The purpose of the Notion Recurring Tasks software is to detect tasks in your Notion which are marked for recurrance and update them according to the task properties. In the below demonstration you will see a set of images showing how these tasks are updated when running the software.

![Recurring Task](assets/img/demonstration-1.PNG)

The above task is done and marked to recur with all properties set. The Status is reset to 'Not started' and the Due Date is set to the new date accoring to the recur properties. The available units are: Days, Weeks, Months and Years.

![Recurring Task Without Due Date](assets/img/demonstration-2.PNG)

Tasks do not *need* a Due Date to recur. Here the Status is simply reset to 'Not started'. This is useful if you have tasks that are dependant on something else than a Due Date.

![Incomplete Recurring Task](assets/img/demonstration-3.PNG)

If a recurring task is missing one of the recur properties, it resets the Status but keeps the old Due Date.

![Archived Task](assets/img/demonstration-4.PNG)

If a task is marked as Archived it is ignored and does not recur.
