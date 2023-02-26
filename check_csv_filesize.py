import subprocess

ps = subprocess.run(['wc', '-l', 'csv_file.csv'], check=True, capture_output=True)
processNames = subprocess.run(['awk', '{print $1}'],
                              input=ps.stdout, capture_output=True)
print(processNames.stdout.decode('utf-8').strip())
