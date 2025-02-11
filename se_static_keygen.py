import oqs
import os
import numpy as np
from skimage import io

from ID_MSE import compare_images
from selective_encryption_minimal import encrypt

kem = "ML-KEM-1024"
sha_key_str = 'Tuesday Evening'
folder_path = 'images'
buffer_sizes = [640]  
similarity_threshold = 0.9 
base_image = None
shared_secret = None

def process_files_dynamic_key(folder_path, buffer_sizes, sha_key_str, base_image, shared_secret):
    global public_key_receiver
            
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            file_path = os.path.join(folder_path, filename)
            current_image = io.imread(file_path)
            
            # Generate new keypair for every image
            print("New keypair generated")
            with oqs.KeyEncapsulation(kem) as receiver:
                with oqs.KeyEncapsulation(kem) as sender:
                    public_key_receiver = receiver.generate_keypair()
                    cipher, secret = sender.encap_secret(public_key_receiver)
                    shared_secret = secret
            
            print(f'File: {filename}')
            for buffer_size in buffer_sizes:
                #print(f'Buffer: {buffer_size}')
                encrypt(file_path=file_path,
                        sha_key_str=sha_key_str,
                        buffer=buffer_size,
                        aes_key=shared_secret,
                        save_data=False)
            print('----------------------')

if __name__ == "__main__":
    process_files_dynamic_key(folder_path, buffer_sizes, sha_key_str, base_image, shared_secret)