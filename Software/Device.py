import json
import enum
import os.path
from typing import Dict, Type, Any
from pathlib import Path


class DeviceType(enum.Enum):
    PRINTER = 1
    ARDUINO = 2
    POTENTIOSTAT = 3

class DeviceFactory:
    _devices = {}
    _config = None
    _config_loaded = False
    
    @classmethod
    def register_device(cls, device_type, device_class):
        cls._devices[device_type] = device_class
    
    @classmethod
    def load_config(cls, config_file='devices.json'):
        with open(config_file, 'r') as f:
            cls._config = json.load(f)
        cls._config_loaded = True
        return cls._config
    
    @classmethod
    def create_device(cls, device_type, **kwargs):
        # Auto-load config if not loaded already
        if not cls._config_loaded:
            try:
                cls.load_config()
            except Exception as e:
                print(f"Warning: Failed to auto-load device configuration: {e}")
        
        # If config is loaded, try to get device config
        if cls._config_loaded:
            if device_type == DeviceType.ARDUINO and 'arduino' in cls._config:
                # If port/baudrate not provided, use from config
                if 'port' not in kwargs and 'port' in cls._config['arduino']:
                    kwargs['port'] = cls._config['arduino']['port']
                if 'baudrate' not in kwargs and 'baudrate' in cls._config['arduino']:
                    kwargs['baudrate'] = cls._config['arduino']['baudrate']
                if 'calibration_params' not in kwargs and 'pump_calibration' in cls._config['arduino']:
                    kwargs['calibration_params'] = cls._config['arduino']['pump_calibration']
            
            # Similar for other device types
            elif device_type == DeviceType.PRINTER and 'printer' in cls._config:
                if 'port' not in kwargs and 'port' in cls._config['printer']:
                    kwargs['port'] = cls._config['printer']['port']
                if 'baudrate' not in kwargs and 'baudrate' in cls._config['printer']:
                    kwargs['baudrate'] = cls._config['printer']['baudrate']
            
            elif device_type == DeviceType.POTENTIOSTAT and 'potentiostat' in cls._config:
                if 'port' not in kwargs and 'port' in cls._config['potentiostat']:
                    kwargs['port'] = cls._config['potentiostat']['port']
        
        if device_type not in cls._devices:
            raise ValueError(f"No device registered for {device_type}")
            
        return cls._devices[device_type](**kwargs)