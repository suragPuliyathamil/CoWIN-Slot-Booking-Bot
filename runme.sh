nohup python3 test.py > process.log 2>&1 &
echo $! > save_pid.txt