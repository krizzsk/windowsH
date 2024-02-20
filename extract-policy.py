def parse_policy_file(file_path):
    policy_details = {'ComputerConfiguration': [], 'UserConfiguration': []}
    current_section = None
    
    with open(file_path, 'r', encoding='utf-8') as file:  # Specify the encoding here
        lines = file.readlines()
        for line in lines:
            if "Computer Configuration" in line:
                current_section = 'ComputerConfiguration'
            elif "User Configuration" in line:
                current_section = 'UserConfiguration'
            
            if line.startswith("Computer Configuration") or line.startswith("User Configuration"):
                policy_path = line.strip()
                policy_details[current_section].append({'path': policy_path, 'setting': 'Enabled'})  # Simplified example
    
    return policy_details

file_path = 'C:\\Users\\Joel\\Desktop\\apktest\\latestapks\\results.txt'
try:
    policy_details = parse_policy_file(file_path)
    print(policy_details)
except Exception as e:
    print(f"Error reading file: {e}")
