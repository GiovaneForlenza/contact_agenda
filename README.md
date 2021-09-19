# Contact Agenda
A simple way to store information about your contacts

This project was developed in 3 days using only Python, Tkinter for the GUI and SQLite for the DB

# Contact Information
Every contact has the following information
- First Name
- Last Name
- Phone Number
- Email
- Address
- City
- Province
- Zip Code

# After adding a contact
A list with all the contacts will be displayed in the main window. If there are no contacts in the DB, a 'No contacts were found' label will appear instead
The user can Update or Delete each contact by clicking in the 'Update a Contact' button

# How to Update or Delete a contact
- Click on the 'Update a Contact' button in the main window
- In the promp window insert the ID of the contact you wish to Update/Delete
-   Don't know the ID of the contact? No worries, just take a peak at the list created in the main window and look for the first column named 'ID'
- Click 'Ok'
- A new window will be created with all the fields already filled with the selected contact information
- If you just wish to delete the contact, press the 'Delete Contact' button, and press 'Yes' to confirm your choice
- If you wish to update any or all the information from the contact, simply update the information in the text box and press 'Update Contact', and press 'Yes' to confirm your choice
- After pressing 'Yes' the window will be closed and the list of contacts in the main window will be updated

# BE CAREFUL
IF YOU PRESS THE 'DELETE ALL' BUTTON, THE DB WILL BE ERASED


