import os
import shutil
import json
from datetime import datetime
import schedule
import time
# 设置原始数据目录
original_data_dir = 'data//Project'
# 设置备份目录
backup_dir = 'data//Backup_Project'

project_path = os.path.abspath(original_data_dir)
backup_project_path = os.path.abspath(backup_dir)

metadata = {
    'mark': "happy new year",
    'created_at': str(datetime.now()),
    'author': 'Aquman',
    'description': 'Sample data'
}

metadata_path = os.path.join(project_path, 'metadata.json')
with open(metadata_path, 'w') as f:
    json.dump(metadata, f)

# 备份整个项目目录到Backup_Project/
backup_project_path = backup_dir
shutil.copytree(project_path, backup_project_path, dirs_exist_ok=True)

print(f"Original data saved at: {project_path}")
print(f"Metadata saved at: {metadata_path}")
print("Project backed up to: ", backup_project_path)







