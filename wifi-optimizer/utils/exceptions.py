"""Custom exceptions for Wi-Fi optimizer."""

class WiFiOptimizerError(Exception):
    """Base exception for Wi-Fi optimizer."""
    pass

class ScanError(WiFiOptimizerError):
    """Exception raised when Wi-Fi scanning fails."""
    pass

class ConnectionError(WiFiOptimizerError):
    """Exception raised when Wi-Fi connection fails."""
    pass

class NetworkNotFoundError(WiFiOptimizerError):
    """Exception raised when target network is not found."""
    pass

class PermissionError(WiFiOptimizerError):
    """Exception raised when insufficient permissions."""
    pass