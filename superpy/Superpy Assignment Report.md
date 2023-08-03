# Superpy Assignment Report

1. Dynamic Date Management
The DateManager class helps manage dates dynamically. It lets the user change the current date forward or backward easily. By storing the date separately and offering methods to adjust it, the system gains flexibility in managing time. This allows users to test different timeframes,  for example check for expiring products or low inventory, or generating reports for specific periods or time.
It loads the date from a text file, allowing the user to set the current date to a specific value. The advance_time method enables users to move the current date forward by a specific number of days. Additionally, the reset_date method restores the original current date, ensuring a seamless transition back to real-time data. In order to make this work, the date (when advanced or reset to current) is written in a separate CSV file and then read throughout the program as the "current date" by specifying the date the program will operate on from the DateManager class.

        current_date = self.date_manager
        
2. Simple Report Generation
The ReportCreation class, includes separate methods for each type of report, exporting the data in a separate CSV file. For example, the print_low_inventory method identifies products with stock quantities below a certain threshold and generates a report for them. This approach not only reduces code duplication but also simplifies report creation, like generating a report for low inventory items or expired products. This makes it easy to add or modify reports.

3. Data Backup and Recovery
The BackupData class addresses the critical issue of data loss due to accidents or system failures. It creates CSV files with all backed up data and it saves these backups in separate files, which enables the user for easy safekeeping of the data. The backups are organized by using the date and time in their filenames, making it easy to find and restore specific data when needed. This adds an extra layer of protection to the system and ensures data safety.
 Additionally, the restore_data method allows users to retrieve and restore data from these backups.
