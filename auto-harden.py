
import subprocess
import re
def print_autoharden_banner():
	banner_text = "             _              _                   _            \n  __ _ _   _| |_ ___       | |__   __ _ _ __ __| | ___ _ __  \n / _` | | | | __/ _ \ _____| '_ \ / _` | '__/ _` |/ _ \ '_ \ \n| (_| | |_| | || (_) |_____| | | | (_| | | | (_| |  __/ | | |\n \__,_|\__,_|\__\___/      |_| |_|\__,_|_|  \__,_|\___|_| |_|"
	print(banner_text)
	print("===================================")
	print("      Automatic OS Hardening       ")
	print("===================================")
	print("          Author: Tim A            ")
	print("          Version: Beta            ")
	print("===================================")

def check_patterns(pattern, input_string):
	match = re.search(pattern, input_string)
	return bool(match)

def harden(vuln, patch):
	print(vuln)
	print("Hardening step:\n")
	print(patch)
	user_input = input("Execute hardening command? y/n").lower()
	if user_input == 'y':
		print("Hardening step executed. Make sure no disruptions on running services")

	else:
		print("Please enter 'y' for Yes or 'n' for No.")

def run_lynis_command():
	try:
		input("Auditing process will use RAM usage. Press Enter to continue to the next step...")
		print("Running Lynis OS Audit...")
		# Run Lynis command and capture output
		command = 'sudo ./lynis audit system --quick'
		#process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		#output, error = process.communicate()
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,bufsize=1)

		output = ""
		for line in process.stdout:
			print(line, end='')
			output += line


		process.wait()
		# Check for errors
		if process.returncode != 0:
			print("Error after running lynis")
			return None

		return output

	except Exception as e:
		print(f"An error occurred: {str(e)}")
		return None

if __name__ == "__main__":
	print_autoharden_banner()
	# Run Lynis command and capture output
	lynis_output = run_lynis_command()
	pattern = r"- Checking for empty ruleset\s+\[ WARNING \]"
	vulns = r"NETW - Empty ruleset found"
	patch = r"sudo ufw enable && sudo ufw allow ssh && sudo ufw default deny incoming"

	# Check if Lynis output is available
	if lynis_output:
		# Now you can use 'lynis_output' as a string variable and perform any further processing or analysis
		#print("Lynis Output:")
		#print(lynis_output)
		if check_patterns(pattern, lynis_output):
			print("Firewall empty ruleset found.")
			harden(vulns, patch)
	else:
		print("Failed to get Lynis output.")
