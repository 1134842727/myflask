
from app import app

import pdb
from uuid import uuid4
import os
MEDIA = app.config['MEDIA_ROOT'] 
def file_upload(file):  
    
    end_name = file.filename.rsplit('.')[-1]
    if end_name not in ['jpg', 'png', 'gif', 'jpeg']:
        return False
    filename = str(uuid4()) + '.' + end_name  
    file_path = os.path.join(MEDIA, filename)  
    file.save(file_path) 
    return file_path

def file_delete(file_path):  
    if os.path.exists(file_path):  
        os.remove(file_path)  
    return True