import time
import matplotlib.pyplot as plt
from cryptography.hazmat.primitives.asymmetric import rsa, dsa, ec, padding
from cryptography.hazmat.primitives import hashes

security_to_key_size = {
    80: 1024,
    112: 2048,
    128: 3072,
    192: 7680,
    256: 15360
}

def benchmark_key_generation():
    # Security levels
    security_levels = [80, 112, 128, 192, 256]
    rsa_sizes = [1024, 2048, 3072, 7680, 15360]
    dsa_sizes = [1024, 2048, 3072]  
    ecc_curves = [ec.SECP192R1(), ec.SECP224R1(), ec.SECP256R1(), ec.SECP384R1(), ec.SECP521R1()]

    rsa_times = []
    dsa_times = []
    ecc_times = []

    for level, rsa_size, ecc_curve in zip(security_levels, rsa_sizes, ecc_curves):
        # RSA Key Generation
        rsa_key_times = []
        for _ in range(10):  # Perform 10 runs
            start = time.time()
            rsa.generate_private_key(public_exponent=65537, key_size=rsa_size)
            end = time.time()
            rsa_key_times.append(end - start)
        rsa_avg_time = sum(rsa_key_times[1:]) / (len(rsa_key_times) - 1)  # Exclude first run
        rsa_times.append((rsa_size, rsa_avg_time))

        # DSA Key Generation
        if rsa_size in dsa_sizes:
            dsa_key_times = []
            for _ in range(10):
                start = time.time()
                dsa.generate_private_key(key_size=rsa_size)
                end = time.time()
                dsa_key_times.append(end - start)
            dsa_avg_time = sum(dsa_key_times[1:]) / (len(dsa_key_times) - 1)
            dsa_times.append((rsa_size, dsa_avg_time))
        else:
            dsa_times.append((rsa_size, None))  

        # ECC Key Generation
        ecc_key_times = []
        for _ in range(10):
            start = time.time()
            ec.generate_private_key(ecc_curve)
            end = time.time()
            ecc_key_times.append(end - start)
        ecc_avg_time = sum(ecc_key_times[1:]) / (len(ecc_key_times) - 1)
        ecc_times.append((ecc_curve.name, ecc_avg_time))

    return rsa_times, dsa_times, ecc_times


def benchmark_rsa_encryption_for_security_levels():
    encryption_results = []
    plaintext = b"A" * 32  
    rsa_sizes = [1024, 2048, 3072, 7680, 15360]  #RSA sizes for encryption

    for security_level, key_size in zip(security_to_key_size.keys(), rsa_sizes):
        try:
            # RSA Key Generation
            rsa_private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size
            )
            rsa_public_key = rsa_private_key.public_key()
        except ValueError as e:
            print(f"Key generation failed for RSA-{key_size} due to: {e}")
            continue  # Skip

        encryption_times = []
        for _ in range(10):
            try:
                start = time.time()
                ciphertext = rsa_public_key.encrypt(
                    plaintext,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                end = time.time()
                encryption_times.append(end - start)
            except Exception as e:
                print(f"Encryption failed for RSA-{key_size} due to: {str(e)}")
                continue  # Skip

        if encryption_times:
            avg_time = sum(encryption_times[1:]) / (len(encryption_times) - 1)  # Exclude first run
            encryption_results.append((security_level, avg_time))
        else:
            encryption_results.append((security_level, None))  

    return encryption_results





def plot_key_generation_results(rsa_results, dsa_results, ecc_results):
    # Extract sizes and times for RSA and DSA
    rsa_sizes, rsa_times = zip(*rsa_results)
    dsa_sizes, dsa_times = zip(*dsa_results)

    # Extract ECC curve names and times
    ecc_labels, ecc_times = zip(*ecc_results)

    all_x_labels = list(map(str, rsa_sizes)) + list(map(str, dsa_sizes)) + list(ecc_labels)
    all_x_positions = range(len(all_x_labels))  # Assign unique x positions

    rsa_x = all_x_positions[:len(rsa_sizes)]
    dsa_x = all_x_positions[len(rsa_sizes):len(rsa_sizes) + len(dsa_sizes)]
    ecc_x = all_x_positions[len(rsa_sizes) + len(dsa_sizes):]

    # Plot
    plt.plot(rsa_x, rsa_times, label="RSA", marker="o")
    plt.plot(dsa_x, dsa_times, label="DSA", marker="x")
    plt.plot(ecc_x, ecc_times, label="ECC", marker="^")

    plt.xticks(all_x_positions, all_x_labels, rotation=45)  # Rotate for better readability

    plt.xlabel("Key Size / Curve")
    plt.ylabel("Time (s)")
    plt.title("Keypair Generation Benchmark")
    plt.legend()
    plt.grid()
    plt.tight_layout()  # Adjust layout for better fit
    plt.savefig("keypair_generation_plot_fixed.png")
    plt.show()


def plot_rsa_encryption_results(encryption_results):
    security_levels = [r[0] for r in encryption_results]  # Security levels (x-axis)
    encryption_times = [r[1] for r in encryption_results]  # Encryption times (y-axis)

    plt.figure(figsize=(12, 7))

    plt.plot(security_levels, encryption_times, label="RSA Encryption Time", marker="s", color="red", linestyle="-")
    for level in security_levels:
        plt.axvline(x=level, color="gray", linestyle="--", alpha=0.6)  # Vertical gray dashed lines

    
    plt.grid(axis='y', linestyle='-', color='gray', alpha=0.6)

    plt.xticks(ticks=security_levels, labels=[f"{level}-bit" for level in security_levels])  # Label x-axis with security levels

    plt.xlabel("Security Level (bits)")
    plt.ylabel("Time (seconds)")
    plt.title("RSA Encryption Time for Different Security Levels")
    plt.legend()
    plt.tight_layout()
    plt.show()

def benchmark_rsa_decryption_for_security_levels():
    decryption_results = []
    plaintext = b"A" * 32  
    rsa_sizes = [1024, 2048, 3072, 7680, 15360] #RSA sizes for encryption

    for security_level, key_size in zip(security_to_key_size.keys(), rsa_sizes):
        try:
            #Key Generation
            rsa_private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size
            )
            rsa_public_key = rsa_private_key.public_key()

            
            ciphertext = rsa_public_key.encrypt(
                plaintext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except ValueError as e:
            print(f"Key generation or encryption failed for RSA-{key_size} due to: {e}")
            continue

        # Decryption Timing
        decryption_times = []
        for _ in range(10):
            try:
                start = time.time()
                decrypted_text = rsa_private_key.decrypt(
                    ciphertext,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                end = time.time()
                decryption_times.append(end - start)
            except Exception as e:
                print(f"Decryption failed for RSA-{key_size} due to: {str(e)}")
                continue  # Skip to next decryption attempt if failure occurs

        if decryption_times:
            avg_time = sum(decryption_times[1:]) / (len(decryption_times) - 1)  # Exclude first run
            decryption_results.append((security_level, avg_time))
        else:
            decryption_results.append((security_level, None))

    return decryption_results
#results for RSA Decryption Times at Different Security Levels
def plot_rsa_decryption_results(decryption_results):
    security_levels = [r[0] for r in decryption_results]  # Security levels (x-axis)
    decryption_times = [r[1] for r in decryption_results]  # Decryption times (y-axis)

    plt.figure(figsize=(12, 7))

    # RSA Decryption Times
    plt.plot(security_levels, decryption_times, label="RSA Decryption Time", marker="s", color="blue", linestyle="-")

    for level in security_levels:
        plt.axvline(x=level, color="gray", linestyle="--", alpha=0.6)  # Vertical gray dashed lines

    plt.grid(axis='y', linestyle='-', color='gray', alpha=0.6)

    plt.xticks(ticks=security_levels, labels=[f"{level}-bit" for level in security_levels])  # Label x-axis with security levels

    plt.xlabel("Security Level (bits)")
    plt.ylabel("Time (seconds)")
    plt.title("RSA Decryption Time for Different Security Levels")
    plt.legend()
    plt.tight_layout()
    plt.show()

def benchmark_digital_signing():
    signing_results = {
        "RSA": [],
        "DSA": [],
        "ECC": []
    }
    rsa_sizes = [1024, 2048, 3072, 7680, 15360]
    dsa_sizes = [1024, 2048, 3072]
    ecc_curves = [ec.SECP192R1(), ec.SECP224R1(), ec.SECP256R1(), ec.SECP384R1(), ec.SECP521R1()]
    message = b"Digital signing benchmark message"  
    hash_algorithm = hashes.SHA256()

    # RSA Signing
    for key_size in rsa_sizes:
        signing_times = []
        try:
            #RSA key
            rsa_private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
            for _ in range(10):  # Perform 10 runs
                digest = hashes.Hash(hash_algorithm)
                digest.update(message)
                hashed_message = digest.finalize()
                start = time.time()
                rsa_private_key.sign(
                    data=hashed_message,
                    padding=padding.PSS(
                        mgf=padding.MGF1(algorithm=hash_algorithm),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    algorithm=hash_algorithm
                )
                end = time.time()
                signing_times.append(end - start)
        except Exception as e:
            print(f"Signing failed for RSA-{key_size} due to: {str(e)}")
            signing_results["RSA"].append((key_size, None))
            continue

        avg_time = sum(signing_times[1:]) / (len(signing_times) - 1) if len(signing_times) > 1 else None
        signing_results["RSA"].append((key_size, avg_time))

    # DSA Signing
    for key_size in dsa_sizes:
        signing_times = []
        try:
            # Generate DSA key
            dsa_private_key = dsa.generate_private_key(key_size=key_size)
            for _ in range(10):  # Perform 10 runs
                digest = hashes.Hash(hash_algorithm)
                digest.update(message)
                hashed_message = digest.finalize()
                start = time.time()
                dsa_private_key.sign(
                    data=hashed_message,
                    algorithm=hash_algorithm
                )
                end = time.time()
                signing_times.append(end - start)
        except Exception as e:
            print(f"Signing failed for DSA-{key_size} due to: {str(e)}")
            signing_results["DSA"].append((key_size, None))
            continue

        avg_time = sum(signing_times[1:]) / (len(signing_times) - 1) if len(signing_times) > 1 else None
        signing_results["DSA"].append((key_size, avg_time))

    #ECC Signing
    for curve in ecc_curves:
        signing_times = []
        try:
            # Generate ECC key
            ecc_private_key = ec.generate_private_key(curve)
            for _ in range(10):  # Perform 10 runs
                digest = hashes.Hash(hash_algorithm)
                digest.update(message)
                hashed_message = digest.finalize()
                start = time.time()
                ecc_private_key.sign(
                    data=hashed_message,
                    signature_algorithm=ec.ECDSA(hash_algorithm)
                )
                end = time.time()
                signing_times.append(end - start)
        except Exception as e:
            print(f"Signing failed for ECC-{curve.name} due to: {str(e)}")
            signing_results["ECC"].append((curve.name, None))
            continue

        avg_time = sum(signing_times[1:]) / (len(signing_times) - 1) if len(signing_times) > 1 else None
        signing_results["ECC"].append((curve.name, avg_time))

    return signing_results

# results for Digital Signing Benchmark
def plot_digital_signing_results(signing_results):
    plt.figure(figsize=(12, 7))

    # Plot RSA results
    if signing_results["RSA"]:
        rsa_keys, rsa_times = zip(*signing_results["RSA"])
        plt.plot(rsa_keys, rsa_times, label="RSA Signing Time", marker="o", linestyle="-", color="blue")
    else:
        print("No RSA signing results to plot.")

    # Plot DSA results
    if signing_results["DSA"]:
        dsa_keys, dsa_times = zip(*signing_results["DSA"])
        plt.plot(dsa_keys, dsa_times, label="DSA Signing Time", marker="x", linestyle="--", color="orange")
    else:
        print("No DSA signing results to plot.")

    # Plot ECC results
    if signing_results["ECC"]:
        ecc_keys, ecc_times = zip(*signing_results["ECC"])
        plt.plot(ecc_keys, ecc_times, label="ECC Signing Time", marker="^", linestyle=":", color="green")
    else:
        print("No ECC signing results to plot.")

    #labels, title, and legend
    plt.xlabel("Key Size / Curve")
    plt.ylabel("Time (seconds)")
    plt.title("Digital Signing Time for RSA, DSA, and ECC")                                     #
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# Function to benchmark Signature Verification
def benchmark_signature_verification():
    verification_results = {
        "RSA": [],
        "DSA": [],
        "ECC": []
    }
    rsa_sizes = [1024, 2048, 3072, 7680, 15360]
    dsa_sizes = [1024, 2048, 3072]
    ecc_curves = [ec.SECP192R1(), ec.SECP224R1(), ec.SECP256R1(), ec.SECP384R1(), ec.SECP521R1()]
    message = b"Digital signing benchmark message"
    hash_algorithm = hashes.SHA256()

    # RSA Verification
    for key_size in rsa_sizes:
        verification_times = []
        try:
            rsa_private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
            rsa_public_key = rsa_private_key.public_key()
            digest = hashes.Hash(hash_algorithm)
            digest.update(message)
            hashed_message = digest.finalize()
            signature = rsa_private_key.sign(
                data=hashed_message,
                padding=padding.PSS(
                    mgf=padding.MGF1(algorithm=hash_algorithm),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                algorithm=hash_algorithm
            )
            for _ in range(10):
                start = time.time()
                rsa_public_key.verify(
                    signature=signature,
                    data=hashed_message,
                    padding=padding.PSS(
                        mgf=padding.MGF1(algorithm=hash_algorithm),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    algorithm=hash_algorithm
                )
                end = time.time()
                verification_times.append(end - start)
        except InvalidSignature:
            print(f"RSA Verification failed for key size {key_size}: Invalid signature.")
            verification_results["RSA"].append((key_size, None))
            continue
        except Exception as e:
            print(f"RSA Verification failed for key size {key_size}: {str(e)}")
            verification_results["RSA"].append((key_size, None))
            continue

        avg_time = sum(verification_times[1:]) / (len(verification_times) - 1) if len(verification_times) > 1 else None
        verification_results["RSA"].append((key_size, avg_time))

    # DSA Verification
    for key_size in dsa_sizes:
        verification_times = []
        try:
            dsa_private_key = dsa.generate_private_key(key_size=key_size)
            dsa_public_key = dsa_private_key.public_key()
            digest = hashes.Hash(hash_algorithm)
            digest.update(message)
            hashed_message = digest.finalize()
            signature = dsa_private_key.sign(data=hashed_message, algorithm=hash_algorithm)
            for _ in range(10):
                start = time.time()
                dsa_public_key.verify(
                    signature=signature,
                    data=hashed_message,
                    algorithm=hash_algorithm
                )
                end = time.time()
                verification_times.append(end - start)
        except InvalidSignature:
            print(f"DSA Verification failed for key size {key_size}: Invalid signature.")
            verification_results["DSA"].append((key_size, None))
            continue
        except Exception as e:
            print(f"DSA Verification failed for key size {key_size}: {str(e)}")
            verification_results["DSA"].append((key_size, None))
            continue

        avg_time = sum(verification_times[1:]) / (len(verification_times) - 1) if len(verification_times) > 1 else None
        verification_results["DSA"].append((key_size, avg_time))

    # ECC Verification
    for curve in ecc_curves:
        verification_times = []
        try:
            ecc_private_key = ec.generate_private_key(curve)
            ecc_public_key = ecc_private_key.public_key()
            digest = hashes.Hash(hash_algorithm)
            digest.update(message)
            hashed_message = digest.finalize()
            signature = ecc_private_key.sign(data=hashed_message, signature_algorithm=ec.ECDSA(hash_algorithm))
            for _ in range(10):
                start = time.time()
                ecc_public_key.verify(
                    signature=signature,
                    data=hashed_message,
                    signature_algorithm=ec.ECDSA(hash_algorithm)
                )
                end = time.time()
                verification_times.append(end - start)
        except InvalidSignature:
            print(f"ECC Verification failed for curve {curve.name}: Invalid signature.")
            verification_results["ECC"].append((curve.name, None))
            continue
        except Exception as e:
            print(f"ECC Verification failed for curve {curve.name}: {str(e)}")
            verification_results["ECC"].append((curve.name, None))
            continue

        avg_time = sum(verification_times[1:]) / (len(verification_times) - 1) if len(verification_times) > 1 else None
        verification_results["ECC"].append((curve.name, avg_time))

    return verification_results

# Signature Verification Results
def plot_signature_verification_results(verification_results):
    plt.figure(figsize=(12, 7))

    
    if verification_results["RSA"]:
        rsa_keys, rsa_times = zip(*verification_results["RSA"])
        plt.plot(rsa_keys, rsa_times, label="RSA Verification Time", marker="o", linestyle="-", color="blue")

    
    if verification_results["DSA"]:
        dsa_keys, dsa_times = zip(*verification_results["DSA"])
        plt.plot(dsa_keys, dsa_times, label="DSA Verification Time", marker="x", linestyle="--", color="orange")

    
    if verification_results["ECC"]:
        ecc_keys, ecc_times = zip(*verification_results["ECC"])
        plt.plot(ecc_keys, ecc_times, label="ECC Verification Time", marker="^", linestyle=":", color="green")

    
    plt.xlabel("Key Size / Curve")
    plt.ylabel("Time (seconds)")
    plt.title("Signature Verification Time for RSA, DSA, and ECC")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# loading text
if __name__ == "__main__":
    print("Running Keypair Generation Benchmark for RSA, DSA, and ECC...")         #
    rsa_results, dsa_results, ecc_results = benchmark_key_generation()  
    plot_key_generation_results(rsa_results, dsa_results, ecc_results)  

    print("Running RSA Encryption Benchmark for Different Security Levels...")     #
    encryption_results = benchmark_rsa_encryption_for_security_levels()  
    plot_rsa_encryption_results(encryption_results)  

    print("Running RSA Decryption Benchmark for Different Security Levels...")     #
    decryption_results = benchmark_rsa_decryption_for_security_levels()  
    plot_rsa_decryption_results(decryption_results)  

    print("Running Digital Signing Benchmark for RSA, DSA, and ECC...")
    signing_results = benchmark_digital_signing()  
    plot_digital_signing_results(signing_results)  

    print("Running Signature Verification Benchmark for RSA, DSA, and ECC...")
    verification_results = benchmark_signature_verification()
    plot_signature_verification_results(verification_results)

    print("Benchmarking Complete!")
