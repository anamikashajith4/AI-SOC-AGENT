import random
import time
from datetime import datetime

# Realistic value pools, inspired by NSL-KDD feature ranges
PROTOCOLS = ['tcp', 'udp', 'icmp']
SERVICES = ['http', 'ftp_data', 'private', 'smtp', 'domain_u', 'other']
NORMAL_FLAGS = ['SF']
ATTACK_FLAGS = ['S0', 'REJ', 'RSTR']

def generate_normal_log():
    return {
        "timestamp": datetime.now().isoformat(),
        "src_ip": f"192.168.1.{random.randint(2, 254)}",
        "protocol_type": random.choice(PROTOCOLS),
        "service": random.choice(SERVICES),
        "flag": random.choice(NORMAL_FLAGS),
        "src_bytes": random.randint(50, 2000),
        "dst_bytes": random.randint(0, 5000),
        "num_failed_logins": 0,
        "serror_rate": round(random.uniform(0, 0.1), 2),
        "is_attack_injected": False,
        "attack_type": None
    }

def generate_brute_force_log():
    return {
        "timestamp": datetime.now().isoformat(),
        "src_ip": f"45.33.{random.randint(1,255)}.{random.randint(1,255)}",
        "protocol_type": "tcp",
        "service": "private",
        "flag": random.choice(ATTACK_FLAGS),
        "src_bytes": random.randint(10, 100),
        "dst_bytes": 0,
        "num_failed_logins": random.randint(4, 10),
        "serror_rate": round(random.uniform(0.5, 1.0), 2),
        "is_attack_injected": True,
        "attack_type": "brute_force"
    }

def generate_port_scan_log():
    return {
        "timestamp": datetime.now().isoformat(),
        "src_ip": f"185.220.{random.randint(1,255)}.{random.randint(1,255)}",
        "protocol_type": "tcp",
        "service": random.choice(SERVICES),
        "flag": "S0",
        "src_bytes": random.randint(0, 20),
        "dst_bytes": 0,
        "num_failed_logins": 0,
        "serror_rate": round(random.uniform(0.7, 1.0), 2),
        "is_attack_injected": True,
        "attack_type": "port_scan"
    }

def generate_traffic_spike_log():
    return {
        "timestamp": datetime.now().isoformat(),
        "src_ip": f"192.168.1.{random.randint(2, 254)}",
        "protocol_type": "tcp",
        "service": "http",
        "flag": "SF",
        "src_bytes": random.randint(50000, 200000),
        "dst_bytes": random.randint(50000, 200000),
        "num_failed_logins": 0,
        "serror_rate": round(random.uniform(0, 0.2), 2),
        "is_attack_injected": True,
        "attack_type": "traffic_spike"
    }

def generate_log_entry():
    # 90% normal traffic, 10% attack (random type)
    roll = random.random()
    if roll < 0.90:
        return generate_normal_log()
    elif roll < 0.94:
        return generate_brute_force_log()
    elif roll < 0.97:
        return generate_port_scan_log()
    else:
        return generate_traffic_spike_log()

if __name__ == "__main__":
    print("Starting log simulator... (Press Ctrl+C to stop)\n")
    while True:
        log = generate_log_entry()
        tag = f"⚠️  ATTACK ({log['attack_type']})" if log['is_attack_injected'] else "✅ normal"
        print(f"[{log['timestamp']}] {tag} | src={log['src_ip']} | service={log['service']} | flag={log['flag']}")
        time.sleep(random.uniform(0.5, 2))