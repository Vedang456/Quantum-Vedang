import os
from typing import Dict, Any
import secrets

class Config:
    """Configuration for Quantum Intelligence API"""
    
    # API Settings
    API_VERSION = "1.0.quantum"
    DEFAULT_PORT = 7777
    HOST = "0.0.0.0"
    DEBUG = False
    
    # Security Settings
    JWT_SECRET_KEY = os.getenv('QUANTUM_API_JWT_SECRET_KEY', secrets.token_hex(32))
    TOKEN_EXPIRE_HOURS = 24
    CACHE_TIMEOUT = 3600  # 1 hour
    SECURITY_LEVEL = "high"
    
    # Quantum Parameters
    N_QUBITS = 4
    QUANTUM_DEPTH = 3
    ENTANGLEMENT_LAYERS = 2
    NOISE_THRESHOLD = 0.01
    
    # Neural Network Parameters
    INPUT_SHAPE = (128, 1)  # Changed to tuple
    HIDDEN_LAYERS = [256, 128, 64]
    BATCH_SIZE = 32
    LEARNING_RATE = 0.001
    
    # System Settings
    MAX_WORKERS = 4
    WORKER_TIMEOUT = 30
    MAX_REQUESTS_PER_WORKER = 1000
    LOG_LEVEL = "INFO"
    METRICS_INTERVAL = 60  # seconds
    LATENCY_THRESHOLD = 50  # ms
    MAX_PENDING_REQUESTS = 100
    
    def __init__(self):
        """Initialize configuration with environment variables"""
        self._config_dict = {}
        self._load_defaults()
        self._load_env_vars()
        self._validate_config()
        
    def _load_defaults(self):
        """Load default values into config dictionary"""
        for key in dir(self):
            if not key.startswith('_'):
                value = getattr(self, key)
                if isinstance(value, (int, float, str, list, bool, bytes, tuple)):
                    self._config_dict[key] = value

    def _load_env_vars(self):
        """Load configuration from environment variables"""
        for key in self._config_dict:
            env_value = os.getenv(f'QUANTUM_API_{key}')
            if env_value is not None:
                self._config_dict[key] = self._convert_type(env_value, self._config_dict[key])
    
    def _convert_type(self, value: str, reference: Any) -> Any:
        """Convert string value to reference type"""
        try:
            if isinstance(reference, bool):
                return value.lower() in ('true', '1', 'yes')
            elif isinstance(reference, int):
                return int(value)
            elif isinstance(reference, float):
                return float(value)
            elif isinstance(reference, list):
                ref_type = type(reference[0]) if reference else int
                return [ref_type(x) for x in value.split(',')]
            return value
        except Exception:
            return reference
    
    def _validate_config(self):
        """Validate configuration values"""
        assert isinstance(self._config_dict['INPUT_SHAPE'], tuple) and len(self._config_dict['INPUT_SHAPE']) == 2 and self._config_dict['INPUT_SHAPE'][0] > 0, "INPUT_SHAPE must be a tuple (length, features) with positive length"
        assert self._config_dict['QUANTUM_DEPTH'] > 0, "QUANTUM_DEPTH must be positive"
        assert self._config_dict['N_QUBITS'] > 0, "N_QUBITS must be positive"
        assert self._config_dict['MAX_WORKERS'] > 0, "MAX_WORKERS must be positive"
        assert self._config_dict['JWT_SECRET_KEY'], "JWT_SECRET_KEY must be set"
        assert self._config_dict['LATENCY_THRESHOLD'] > 0, "LATENCY_THRESHOLD must be positive"
        assert self._config_dict['MAX_PENDING_REQUESTS'] >= 0, "MAX_PENDING_REQUESTS must be non-negative"
    
    def __getitem__(self, key: str) -> Any:
        """Enable dictionary-style access to config values"""
        return self._config_dict.get(key)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value with default"""
        return self._config_dict.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return self._config_dict.copy()