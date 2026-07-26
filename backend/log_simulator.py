import random
import time
import pandas as pd
from datetime import datetime

# Load real normal traffic samples (exported from actual NSL-KDD training data)
normal_pool = pd.read_csv('models/normal_traffic_sample.csv')

ATTACK_FLAGS = ['S0', 'REJ', 'RSTR']

def generate_normal_log():
    # Pick a random REAL normal row from the training data
    sample = normal_pool.sample(1).iloc[0]
    return {
        "timestamp": datetime.now().isoformat(),
        "src_ip": f"192.168.1.{random.randint(2, 254)}",
        "protocol_type": sample['protocol_type'],
        "service": sample['service'],
        "flag": sample['flag'],
        "src_bytes": int(sample['src_bytes']),
        "dst_bytes": int(sample['dst_bytes']),
        "num_failed_logins": int(sample['num_failed_logins']),
        "serror_rate": float(sample['serror_rate']),
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
        "service": random.choice(['http', 'private', 'domain_u', 'other']),
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