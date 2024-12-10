import bcrypt
import hashlib
import itertools
import string
from tqdm import tqdm

# Load the external dictionary file
def load_dictionary(file_path: str) -> list:
    """
    Loads a dictionary file and returns a list of words.
    """
    with open(file_path, 'r') as file:
        return file.read().splitlines()

# Section 1: Password Hashing using bcrypt
def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def generate_sha256_hash(password: str) -> str:
    """
    Generates a SHA-256 hash of a password.
    """
    return hashlib.sha256(password.encode()).hexdigest()

# Section 2: Password Cracking
def brute_force_crack(target_hash: str, max_length: int) -> str:
    """
    Attempts to brute-force crack a SHA-256 hash.
    """
    chars = string.ascii_letters + string.digits
    for length in range(1, max_length + 1):
        total_attempts = len(chars) ** length
        with tqdm(total=total_attempts, desc=f"Length {length}", leave=True, dynamic_ncols=True) as pbar:
            for guess in itertools.product(chars, repeat=length):
                guess_password = ''.join(guess)
                guess_hash = generate_sha256_hash(guess_password)
                
                # Update the current combination in the progress bar description
                pbar.set_postfix_str(f"Testing: {guess_password}")
                
                if guess_hash == target_hash:
                    return guess_password
                
                pbar.update(1)
    return None

def dictionary_attack(target_hash: str, dictionary: list) -> str:
    """
    Attempts to crack a SHA-256 hash using a dictionary attack.
    """
    with tqdm(dictionary, desc="Dictionary attack", leave=True, dynamic_ncols=True) as pbar:
        for word in pbar:
            guess_hash = generate_sha256_hash(word)
            
            # Update the current combination in the progress bar description
            pbar.set_postfix_str(f"Testing: {word}")
            
            if guess_hash == target_hash:
                return word
    return None

# Section 3: Main Functionality
if __name__ == "__main__":
    print("=== Password Security Demonstration ===")
    
    # Step 1: Input the password
    plain_password = input("Enter a password to hash and crack: ")
    
    # Step 2: Hash the password using bcrypt
    hashed_password = hash_password(plain_password)
    print(f"bcrypt Hashed Password: {hashed_password.decode('utf-8', errors='ignore')}")
    
    # Step 3: Generate a SHA-256 hash for cracking demonstration
    sha256_hash = generate_sha256_hash(plain_password)
    print(f"SHA-256 Hash for Cracking: {sha256_hash}")

    # Step 4: Attempt to crack the hash using brute force
    print("\n=== Brute-Force Cracking ===")
    max_length = 5  # Limit brute force to shorter passwords for efficiency
    print("Attempting to crack the hash...")
    cracked_password = brute_force_crack(sha256_hash, max_length)
    if cracked_password:
        print(f"\nBrute-force cracked password: {cracked_password}")
    else:
        print("\nFailed to crack the password using brute force.")

    # Step 5: Attempt to crack the hash using the external dictionary
    print("\n=== Dictionary Attack ===")
    dictionary_file_path = 'C:/Users/grzan/auto sec/english.0'
    dictionary = load_dictionary(dictionary_file_path)
    cracked_password = dictionary_attack(sha256_hash, dictionary)
    if cracked_password:
        print(f"\nDictionary attack cracked password: {cracked_password}")
    else:
        print("\nFailed to crack the password using the dictionary.")

    print("\nDemonstration complete!")
