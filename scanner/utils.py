# scanner/utils.py
import subprocess
import uuid
import os
from django.conf import settings

def run_nmap(ip, scan_type):
    filename = f"scan_{uuid.uuid4().hex}.xml"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    # Select flags based on scan type
    if scan_type == "tcp":
        scan_command = ["nmap", "-sS", "-oX", filepath, ip]
    elif scan_type == "udp":
        scan_command = ["nmap", "-sU", "-oX", filepath, ip]
    elif scan_type == "full":
        scan_command = ["nmap", "-sS", "-sV", "-T4", "-A", "-oX", filepath, ip]
    else:
        return None, None

    try:
        result = subprocess.run(scan_command, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            return result.stdout, settings.MEDIA_URL + filename
        else:
            return result.stderr, None
    except subprocess.TimeoutExpired:
        return "Scan timed out.", None
    except Exception as e:
        return str(e), None
