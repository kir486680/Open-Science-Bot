import json
from enum import Enum
from typing import Dict, Type, Any
from pathlib import Path


class DeviceType(Enum):
    PRINTER = "printer"
    ARDUINO = "arduino"

class DeviceFactory:
    _devices: Dict[DeviceType, Type] = {}
    _config: Dict = {}
    
    @classmethod
    def load_config(cls, config_path: str | Path) -> None:
        """Load device configuration from a JSON file."""
        with open(config_path, 'r') as f:
            cls._config = json.load(f)
    
    @classmethod
    def register_device(cls, device_type: DeviceType, device_class: Type) -> None:
        cls._devices[device_type] = device_class
    
    @classmethod
    def create_device(cls, device_type: DeviceType, **kwargs) -> Any:
        if device_type not in cls._devices:
            raise ValueError(f"Unknown device type: {device_type}")
            
        # If no kwargs provided, try to get config from loaded JSON
        if not kwargs and device_type.value in cls._config:
            kwargs = cls._config[device_type.value]
            
        return cls._devices[device_type](**kwargs)