import hashlib, os

def keygen():
    private_key = os.urandom(32).hex()
    public_key = hashlib.sha256(private_key.encode()).hexdigest()
    return public_key, private_key

# public_key, private_key = keygen()
# Use fixed keypair (For demo/testing only. Use secure storage in production)
public_key = "a-fixed-demo-public-key-1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
private_key = "a-fixed-demo-private-key-abcdef1234567890abcdef1234567890abcdef1234567890abcdef"


def abks_encrypt(keyword, public_key):
    hash1 = hashlib.sha256(keyword.encode()).hexdigest()
    hash2 = hashlib.sha256((hash1 + public_key).encode()).hexdigest()
    return hash2

def generate_trapdoor(keyword, private_key):
    hash1 = hashlib.sha256(keyword.encode()).hexdigest()
    hash2 = hashlib.sha256(private_key.encode()).hexdigest()
    return hashlib.sha256((hash1 + hash2).encode()).hexdigest()

def abks_match(peks_kw, trapdoor, public_key, keyword_guess):
    test = abks_encrypt(keyword_guess, public_key)
    test_trap = generate_trapdoor(keyword_guess, private_key=None)  
    return test == peks_kw or test_trap == trapdoor


from cryptography.fernet import Fernet

file_key = Fernet.generate_key()

fernet = Fernet(file_key)


def encrypt_file_content(content):
    return fernet.encrypt(content.encode()).decode()

def decrypt_file_content(enc):
    return fernet.decrypt(enc.encode()).decode()



def split_data(data):
    part = len(data) // 3
    return data[:part], data[part:2*part], data[2*part:]

def merge_data(p1, p2, p3):
    return p1 + p2 + p3
