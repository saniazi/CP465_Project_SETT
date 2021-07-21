# CP465_Project_SETT

SETT (student employee time tracker) is a web application which allows WLU student employees to complete their timesheet entry form online and allows supervisors to review timesheet entries. Data tables are stored on a live postgresql database using AWS RDS and static data is stored using an AWS S3 bucket.

## Demo
A demo can be found at https://saniazi-sett.herokuapp.com

### Logging in
The demo has 5 students and 5 supervisors registered. Their login credentials and respective IDs are listed below.<br/><br/>
Students:
- john@example.com, ID: 100001
- jane@example.com, ID: 100002
- smith@example.com, ID: 100003
- greg@example.com, ID: 100004
- rr@example.com, ID: 100005

Supervisors:
- schmoe@example.com, ID: 120001
- oo@example.com, ID: 120002
- ll@example.com, ID: 120003
- bloggs@example.com, ID: 120004
- foo@example.com, ID: 120005

Password: qqqqqqq1

### Jobs
If there are no jobs assigned to a student, you can log in as a supervisor and create one on the Positions page. While creating a new position, you'll have the option of assigning a student to the job. After creating a position, log in as the student you asigned the job to. You will now be able to add timesheet entries using the newly created position.

## Screenshots
### Login Page
![Screen Shot 2021-07-20 at 8 28 23 PM](https://user-images.githubusercontent.com/59815152/126411712-5a04d3d8-3868-481a-9429-b6b356874f8e.png)

### Student Dashboard
![Screen Shot 2021-07-20 at 8 23 17 PM](https://user-images.githubusercontent.com/59815152/126411928-b89238bb-1047-42b6-99af-ea25a075374a.png)

### Supervisor Dashboard
![Screen Shot 2021-07-20 at 8 31 35 PM](https://user-images.githubusercontent.com/59815152/126411971-216151b1-86fe-4d79-8369-8b6f72296b3f.png)

### Positions Page
![Screen Shot 2021-07-20 at 8 33 41 PM](https://user-images.githubusercontent.com/59815152/126412187-64a12196-a234-4e4d-a334-2026daca9d1e.png)

### Profile Page
![Screen Shot 2021-07-20 at 8 38 21 PM](https://user-images.githubusercontent.com/59815152/126412456-c2115bff-4124-4015-bbff-90717d6c2230.png)
