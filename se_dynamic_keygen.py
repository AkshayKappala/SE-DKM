import oqs
import os
import numpy as np
from skimage import io
import matplotlib.pyplot as plt  # Import matplotlib
from selective_encryption_minimal import encrypt, encryption_times # Import encryption_times

from ID_MSE import compare_images

kem = "ML-KEM-1024"
sha_key_str = 'Tuesday Evening'
folder_path = 'images/frames'
buffer_sizes = [640]  
similarity_threshold = 0.86 
base_image = None
shared_secret = None


def process_files_dynamic_key(folder_path, buffer_sizes, sha_key_str, base_image, shared_secret):
    global public_key_receiver
    with oqs.KeyEncapsulation(kem) as receiver:
        with oqs.KeyEncapsulation(kem) as sender:
            public_key_receiver = receiver.generate_keypair()
            cipher, secret = sender.encap_secret(public_key_receiver)
            shared_secret = secret
    image_index = 0  # Initialize image index
    key_change_indices = []  # Store indices where a new key is generated
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            file_path = os.path.join(folder_path, filename)
            current_image = io.imread(file_path)
            
            if base_image is None:
                # First image, generate keypair and encrypt
                print("New keypair generated")
                similarity = 0.0
                base_image = current_image
                key_change_indices.append(image_index)
                
            else:
                # Compare with base image
                similarity = compare_images(base_image, current_image)                
                # If dissimilar enough, generate new keypair
                if similarity < similarity_threshold:
                    print("New keypair generated")
                    with oqs.KeyEncapsulation(kem) as receiver:
                        with oqs.KeyEncapsulation(kem) as sender:
                            public_key_receiver = receiver.generate_keypair()
                            cipher, secret = sender.encap_secret(public_key_receiver)
                            shared_secret = secret
                    base_image = current_image  # Update base image
                    key_change_indices.append(image_index)
            
            print(f'File: {filename}, Similarity: {similarity:.2%}')
            for buffer_size in buffer_sizes:
                #print(f'Buffer: {buffer_size}')
                encrypt(file_path=file_path,
                        sha_key_str=sha_key_str,
                        buffer=buffer_size,
                        aes_key=shared_secret,
                        save_data=False)
            print('----------------------')
            image_index += 1  # Increment image index

    # Remove outliers using IQR method
    q1 = np.quantile(encryption_times, 0.25)
    q3 = np.quantile(encryption_times, 0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    filtered_encryption_times = [time for time in encryption_times if lower_bound <= time <= upper_bound]
    
    # Create a list of key change indices that are still within the filtered data
    filtered_key_change_indices = [i for i in key_change_indices if i < len(filtered_encryption_times)]

    plot_encryption_times(filtered_encryption_times, filtered_key_change_indices)

def plot_encryption_times(filtered_encryption_times, filtered_key_change_indices):
    # Calculate the average encryption time
    average_encryption_time = np.mean(filtered_encryption_times)
    
    # Plotting the graph
    bar_colors = ['orange' if i in filtered_key_change_indices else 'skyblue' for i in range(len(filtered_encryption_times))]
    plt.bar(range(1, len(filtered_encryption_times) + 1), filtered_encryption_times, color=bar_colors)
    plt.xlabel("")
    plt.ylabel("Encryption Time (ms)")
    plt.title("Encryption Time Plot with ID-MSE  ")
    plt.grid(axis='y')
    
    # Add a horizontal line for the average encryption time
    plt.axhline(y=average_encryption_time, color='r', linestyle='-', label=f'Average: {average_encryption_time:.2f} ms')
    plt.legend()  # Show the label
    
    plt.savefig('plot_id_mse.png')  # Save the plot to a file
    plt.show()  # Display the plot

if __name__ == "__main__":
    process_files_dynamic_key(folder_path, buffer_sizes, sha_key_str, base_image, shared_secret)