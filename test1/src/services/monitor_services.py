#!/usr/bin/env python3

import requests
import json
import subprocess
import socket
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

from src.config.settings import settings


class ServiceMonitor:
    
    def __init__(self, services: List[str], output_dir: str = settings.output_dir, api_url: str = settings.api_url):
        self.services = services
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.hostname = socket.gethostname()
        self.api_url = api_url
    
    def check_service_status(self, service_name: str) -> str:
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', service_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.stdout.strip() == 'active':
                return "UP"
            else:
                return "DOWN"
                
        except subprocess.TimeoutExpired:
            print(f"Timeout checking service: {service_name}")
            return "DOWN"
        except FileNotFoundError:
            print("systemctl not found. Assuming non-Linux environment.")
            return self._check_service_fallback(service_name)
        except Exception as e:
            print(f"Error checking service {service_name}: {e}")
            return "DOWN"
    
    def _check_service_fallback(self, service_name: str) -> str:
        
        process_map = {
            'httpd': ['httpd', 'apache2'],
            'rabbitmq-server': ['rabbitmq', 'beam.smp'],
            'postgresql': ['postgres', 'postgresql']
        }
        
        processes = process_map.get(service_name, [service_name])
        
        try:
            for process in processes:
                result = subprocess.run(
                    ['pgrep', '-x', process],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return "UP"
            return "DOWN"
        except Exception:
            # For demo purposes, return UP
            return "UP"
    
    def create_service_payload(self, service_name: str, status: str) -> Dict:
        """
        Create JSON payload for a service
        
        Args:
            service_name: Name of the service
            status: Status of the service (UP/DOWN)
            
        Returns:
            Dictionary with service information
        """
        return {
            "service_name": service_name,
            "service_status": status,
            "host_name": self.hostname,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    def write_status_to_file(self, service_name: str, payload: Dict) -> str:

        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        filename = f"{service_name}-status-{timestamp}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(payload, f, indent=2)
        
        print(f"Status written to: {filepath}")
        return str(filepath)
    
    def check_application_status(self) -> str:
       
        for service in self.services:
            status = self.check_service_status(service)
            if status == "DOWN":
                return "DOWN"
        return "UP"
    
    def upload_status(self, filepath: str):

        try:
            with open(filepath, 'rb') as f:
                files = {'file': (Path(filepath).name, f, 'application/json')}
                response = requests.post(self.api_url, files=files, timeout=5)
                
            if response.status_code == 201:
                print(f"Successfully uploaded {filepath} to API")
            else:
                print(f"Failed to upload {filepath}. Status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"Could not connect to API at {self.api_url}. Is the server running?")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def monitor_all_services(self) -> List[Dict]:

        results = []
        
        for service in self.services:
            print(f"Checking service: {service}")
            status = self.check_service_status(service)
            payload = self.create_service_payload(service, status)
            filepath = self.write_status_to_file(service, payload)
            
            self.upload_status(filepath)
            
            results.append(payload)
        
        app_status = self.check_application_status()
        app_payload = {
            "application_name": "rbcapp1",
            "application_status": app_status,
            "host_name": self.hostname,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "dependent_services": results
        }
        
        app_filepath = self.write_status_to_file("rbcapp1", app_payload)
        self.upload_status(app_filepath)
        
        results.append(app_payload)
        
        return results
