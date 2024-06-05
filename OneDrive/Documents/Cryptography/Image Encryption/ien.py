from PIL import Image
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad

RED = "\033[31m"
RESET = "\033[0m"
BLUE = "\033[34m"
ORANGE = "\033[33m" 
GREEN = "\033[32m"

print(GREEN+"##############################################################################################################\n\n"+RESET)
print(RED+"###### #          # ##########       ######## #    # ######### ########  #     # ######## ########"+RESET)
print(ORANGE+"  @@   @@        @@ @                @        @@   @ @         @      @   @   @  @      @    @"+RESET)
print(ORANGE+"  @@   @ @      @ @ @                @@@@@    @ @  @ @         @@@@@@@@     @    @      @    @"+RESET)
print(BLUE+"  @@   @  @    @  @ @    @@@@@       @@@@@    @  @ @ @         @ @          @    @@@@@@@@    @"+RESET)
print(BLUE+"  @@   @   @  @   @ @        @       @        @   @@ @         @  @         @    @           @"+RESET)
print(RED+"###### #    #     # ##########       ######## #    # @######## #   #        #    #           #"+RESET)
print(GREEN+"\n\n##############################################################################################################"+RESET)

# Image Loading
image_path = input("Enter the path of the image: ")
image = Image.open(image_path)

# Convert image to byte stream
image_to_byte = image.tobytes()

byte_length = len(image_to_byte)
print(f"Image byte length: {byte_length}")

# AES Setup
key = get_random_bytes(16)
IV = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC, IV)

# Encryption
encrypted_bytes = cipher.encrypt(image_to_byte)

# Save encrypted data to a .dat file
encrypted_data_path = f"encrypted_image_{image_path}.dat"
with open(encrypted_data_path, "wb") as f:
    f.write(IV)  # Write Initialization Vector first
    f.write(encrypted_bytes)

print(f"Encrypted image data saved to: {encrypted_data_path}")

encrypted_data_path = f"encrypted_image_{image_path}.dat"
decrypted_image_path = f"decrypted_image_{image_path}.png"

# Read encrypted data and IV from the file
with open(encrypted_data_path, "rb") as f:
    IV = f.read(16)  # Read the first 16 bytes as IV
    encrypted_bytes = f.read()

# Decryption
cipher = AES.new(key, AES.MODE_CBC, IV)
decrypted_bytes = cipher.decrypt(encrypted_bytes)

# Padding Removal (if necessary)
if byte_length % 16 != 0:
    decrypted_bytes = unpad(decrypted_bytes, block_size=16)

# Converting decrypted bytes to image data
decrypted_image = Image.frombytes("RGB", image.size, decrypted_bytes)

# Saving decrypted image
decrypted_image.save(decrypted_image_path)

print(f"Decrypted image saved to: {decrypted_image_path}")
