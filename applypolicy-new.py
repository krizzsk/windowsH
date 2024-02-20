import subprocess
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_policy_file(file_path):
    policy_details = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 4:
                policy_details.append({
                    'configuration_type': parts[0],
                    'path': parts[1],
                    'setting_name': parts[2],
                    'desired_value': parts[3]
                })
    return policy_details

def read_policy_value(policy):
    ps_script = f'''
    $value = Get-ItemProperty -Path "Registry::{policy['path']}" -Name {policy['setting_name']} -ErrorAction SilentlyContinue
    if ($value -ne $null) {{
        Write-Output $value.{policy['setting_name']}
    }} else {{
        Write-Output "Not Set"
    }}
    '''
    result = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)
    return result.stdout.strip()

def apply_policy(policy):
    logging.info(f"Applying policy: {policy['path']} with setting {policy['setting_name']} = {policy['desired_value']} for {policy['configuration_type']}")
    ps_script = f'''
    Set-ItemProperty -Path "Registry::{policy['path']}" -Name {policy['setting_name']} -Value "{policy['desired_value']}"
    '''
    subprocess.run(["powershell", "-Command", ps_script], check=True)
    logging.info("Policy applied successfully.")

def verify_policy(policy):
    new_value = read_policy_value(policy)
    if new_value == policy['desired_value']:
        logging.info("Policy verification successful.")
    else:
        logging.error(f"Policy verification failed. Expected: {policy['desired_value']}, Found: {new_value}")

file_path = 'path_to_your_policy_file.txt'
policies = read_policy_file(file_path)

for policy in policies:
    current_value = read_policy_value(policy)
    logging.info(f"Current policy value for {policy['setting_name']}: {current_value}")
    apply_policy(policy)
    verify_policy(policy)
