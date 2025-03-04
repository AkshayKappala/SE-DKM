import oqs
import os
import numpy as np
from skimage import io
import matplotlib.pyplot as plt  # Import matplotlib

from selective_encryption_minimal import encrypt, encryption_times

kem = "ML-KEM-1024"
sha_key_str = 'Tuesday Evening'
folder_path = 'images/frames'
buffer_sizes = [640]  
base_image = None
shared_secret = None

def process_files(folder_path, buffer_sizes, sha_key_str, base_image, shared_secret):
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
            
    # Remove outliers using IQR method
    q1 = np.quantile(encryption_times, 0.25)
    q3 = np.quantile(encryption_times, 0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    filtered_encryption_times = [time for time in encryption_times if lower_bound <= time <= upper_bound]

    plot_encryption_times(filtered_encryption_times)

def plot_encryption_times(filtered_encryption_times):
    # Plotting the graph
    plt.bar(range(1, len(filtered_encryption_times) + 1), filtered_encryption_times, color='skyblue')
    plt.xlabel("")
    plt.ylabel("Encryption Time (ms)")
    plt.title("Encryption Time Plot")
    plt.grid(axis='y')
    
    # Calculate and display average encryption time
    average_time = np.mean(filtered_encryption_times)
    plt.axhline(average_time, color='red', linestyle='dashed', linewidth=1, label=f'Average: {average_time:.2f} ms')
    plt.legend()
    
    plt.savefig('plot_default.png')  # Save the plot to a file
    plt.show()  # Display the plot

if __name__ == "__main__":
    process_files(folder_path, buffer_sizes, sha_key_str, base_image, shared_secret)