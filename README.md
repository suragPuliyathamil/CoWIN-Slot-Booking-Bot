# CowinBot

#### Python files which will track vaccine availability and book vaccine slot. OTP is recieved by UDP Command to your HOST IP. Use any third party service to setup UDP command on mobile. Make sure to enter you phone number and prefered Pincode in the script.

NOTE : 
* Co-WIN Public APIs allow any third-party application to access certain un-restricted information, that can be shared with its users.The extent of access will be limited and in case of any misuse impacting the performance of Co-WIN solution will result in blocking any such application and entities as per the policies of MoHFW and taking any other appropriate action in accordance with law. Further, these APIs are subject to a rate limit of 100 API calls per 5 minutes per IP. Please consider these points while using the APIs in your application. For further questions regarding API used in the scripts, please visit https://github.com/cowinapi/developer.cowin/issues. The scripts used here by default comply with the API call contraints that exists.

* The Above scripts use nohangup calls and runs the process as a background task until they are interrupted. These process must be killed using scripts(here kill_process.sh and instantBookKill.sh) which kills the exact process by taking the process ID stored (here save_pid.txt and save_instant_pid.txt)

* The scripts use traditional webscrapping method to navigate the webpage and book slot. The scripts select the first available slot based on the filters. By default it checks/books for Covishield Vaccine in both free and paid category for 18+ age category.

* bookVaccine.py - Instantly runs and books slot given that you have setup up the UDP command with same port number in both mobile and host.
* trackAndBook.py - keeps checking vaccine availability using public API available at https://apisetu.gov.in/public/marketplace/api/cowin in a particular pincode. If available books vaccine given that you have setup up the UDP command with same port number in both mobile and host.
* runme.sh - Calls trackAndBook.py continously as nohangup call in the background, and saves the process id in save_pid.txt and also creates a .txt file to keep track of log
* kill_process.sh - Kills the process from save_pid.txt
* instantBook.sh and instantBookKill.sh are alternatives of runme.sh and kill_process.sh which runs bookVaccine.py and creates intant.log 


MIT License
Copyright (c) 2021 Surag Puliyathamil

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
