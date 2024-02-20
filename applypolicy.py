import subprocess
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_policy_value(policy, configuration_type):
    gpo_target = "LocalMachine" if configuration_type == 'ComputerConfiguration' else "CurrentUser"
    ps_script = f'''
    $value = Get-ItemProperty -Path "Registry::{policy['path']}" -Name PolicySetting -ErrorAction SilentlyContinue
    if ($value -ne $null) {{
        Write-Output $value.PolicySetting
    }} else {{
        Write-Output "Not Set"
    }}
    '''
    result = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)
    return result.stdout.strip()

def apply_policy(policy, configuration_type):
    logging.info(f"Applying policy: {policy['path']} with setting {policy['setting']} for {configuration_type}")

    # Read current policy value
    current_value = read_policy_value(policy, configuration_type)
    logging.info(f"Current policy value: {current_value}")
    
    # Form and execute the PowerShell script to apply the policy
    # Simplified for demonstration, replace with your actual policy application logic
    gpo_target = "LocalMachine" if configuration_type == 'ComputerConfiguration' else "CurrentUser"
    ps_script = f'''
    Import-Module GroupPolicy
    # Simplified policy application logic for demonstration
    Set-ItemProperty -Path "Registry::{policy['path']}" -Name PolicySetting -Value "{policy['setting']}"
    '''
    try:
        subprocess.run(["powershell", "-Command", ps_script], check=True, capture_output=True, text=True)
        logging.info("Policy applied successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error applying policy: {e.output}")
        return

    # Verify policy value after application
    new_value = read_policy_value(policy, configuration_type)
    logging.info(f"New policy value: {new_value}")
    if new_value == policy['setting']:
        logging.info("Policy verification successful.")
    else:
        logging.error("Policy verification failed.")

# Example usage with simplified policy details
policy_details = {
    'ComputerConfiguration': [{'path': 'HKLM\Software\MyPolicy', 'setting': 'Enabled'}],
    'UserConfiguration': [{'path': 'HKCU\Software\MyPolicy', 'setting': 'Enabled'}]
}

for policy in policy_details['ComputerConfiguration']:
    apply_policy(policy, 'ComputerConfiguration')

for policy in policy_details['UserConfiguration']:
    apply_policy(policy, 'UserConfiguration')
